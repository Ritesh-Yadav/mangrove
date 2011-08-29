# vim: ai ts=4 sts=4 et sw= encoding=utf-8

import copy
from datetime import datetime
from time import mktime
from collections import defaultdict
from documents import attributes
from datadict import DataDictType, get_datadict_types
from mangrove.datastore import settings
import mangrove.datastore.aggregationtree as atree
from mangrove.errors.MangroveException import EntityTypeAlreadyDefined, DataObjectAlreadyExists, EntityTypeDoesNotExistsException, DataObjectNotFound, EntityNotFoundException
from mangrove.utils.types import is_empty
from mangrove.utils.types import is_not_empty, is_sequence, is_string
from mangrove.utils.dates import utcnow
from database import DatabaseManager, DataObject
from uuid import uuid4

ENTITY_TYPE_TREE = u'entity_type_tree'


def _check_if_exists(dbm, entity_type, short_code):
    try:
        get_by_short_code(dbm, short_code, entity_type)
        return True
    except DataObjectNotFound:
        return False


def create_entity(dbm, entity_type, short_code, location=None, aggregation_paths=None, geometry=None):
    """
    Initialize and save an entity to the database. Return the entity
    created unless the short code used is not unique or this entity
    type has not been defined yet.
    """
    assert is_string(short_code) and not is_empty(short_code)
    assert type(entity_type) is list and not is_empty(entity_type)
    type_hierarchy = [e_type for e_type in entity_type]
    if not entity_type_already_defined(dbm, type_hierarchy):
        raise EntityTypeDoesNotExistsException(entity_type)
    if _check_if_exists(dbm, type_hierarchy, short_code):
        raise DataObjectAlreadyExists("Entity", "Unique Identification Number (ID)", short_code)
    e = Entity(dbm, entity_type=type_hierarchy, location=location,
               aggregation_paths=aggregation_paths, short_code=short_code, geometry=geometry)
    e.save()
    return e


def _get_entity_type_tree(dbm):
    """
    Return the AggregationTree object with id equal to
    'entity_type_tree'.
    """
    assert isinstance(dbm, DatabaseManager)
    return dbm.get(ENTITY_TYPE_TREE, atree.AggregationTree, get_or_create=True)


def get_all_entity_types(dbm):
    """
    Return a list of all entity types. If we think of all entity types
    organized in a hierarchical tree, an entity type is a node in this
    tree and the node is represented by a list containing the node
    names in the path to this node.
    """
    return _get_entity_type_tree(dbm).get_paths()


def entity_type_already_defined(dbm, entity_type):
    all_entities = get_all_entity_types(dbm)
    if all_entities:
        all_entities_lower_case = [[x.lower() for x in each] for each in all_entities]
        entity_type_lower_case = [each.lower() for each in entity_type]
        if entity_type_lower_case in all_entities_lower_case:
            return True
    return False


def define_type(dbm, entity_type):
    """
    Add this entity type to the tree of all entity types and save it
    to the database. entity_type may be a string or a list of
    strings.
    """
    assert is_not_empty(entity_type)
    assert is_sequence(entity_type)
    type_path = ([entity_type] if is_string(entity_type) else entity_type)
    type_path = [item.strip() for item in type_path]
    if entity_type_already_defined(dbm, type_path):
        raise EntityTypeAlreadyDefined(u"Type: %s is already defined" % u'.'.join(entity_type))
        # now make the new one
    entity_tree = _get_entity_type_tree(dbm)
    entity_tree.add_path([atree.AggregationTree.root_id] + entity_type)
    entity_tree.save()


def generate_short_code(dbm, entity_type):
    # todo: couchdb cannot guarantee uniqueness, so short codes should
    # be assigned from an application using the mangrove
    # library. ideally, we would put a short code onto an entity using
    # the add_data method and then there should be a view that can
    # easily find all entities with a particular short code.
    assert is_sequence(entity_type)
    count = get_entity_count_for_type(dbm, entity_type=entity_type)
    assert count >= 0
    return _make_short_code(entity_type, count + 1)


def get_entity_count_for_type(dbm, entity_type):
    rows = dbm.load_all_rows_in_view(u"by_short_codes", descending=True,
                                     startkey=[[entity_type], {}], endkey=[[entity_type]], group_level=1)
    return rows[0][u"value"] if len(rows) else 0


def get_by_short_code(dbm, short_code, entity_type):
    assert is_string(short_code)
    assert is_sequence(entity_type)
    rows = dbm.load_all_rows_in_view("by_short_codes", key=[entity_type, short_code], reduce=False)
    if is_empty(rows):
        raise DataObjectNotFound("Entity", "Unique Identification Number (ID)", short_code)
    doc_id = rows[0].id
    return Entity.get(dbm, doc_id)


def _generate_new_code(entity_type, count):
    # todo: remove
    short_code = _make_short_code(entity_type, count + 1)
    return _make_doc_id(entity_type, short_code)


def _make_doc_id(entity_type, short_code):
    # todo: remove
    ENTITY_ID_FORMAT = "%s/%s"
    _entity_type = ".".join(entity_type)
    return ENTITY_ID_FORMAT % (_entity_type, short_code)


def _make_short_code(entity_type, num):
    # todo: remove
    SHORT_CODE_FORMAT = "%s%s"
    entity_prefix = entity_type[-1].upper()[:3]
    return   SHORT_CODE_FORMAT % (entity_prefix, num)


def _make_short_code(entity_type, num):
    # todo: remove
    SHORT_CODE_FORMAT = "%s%s"
    entity_prefix = entity_type[-1].lower()[:3]
    return   SHORT_CODE_FORMAT % (entity_prefix, num)


def get_entities_by_type(dbm, entity_type):
    """
    Return a list of all entities with this type.
    """
    # TODO: change this?  for now it assumes _type is
    # non-heirarchical. Might also benefit from using get_many.
    assert isinstance(dbm, DatabaseManager)
    assert is_string(entity_type)

    rows = dbm.load_all_rows_in_view(u'by_type', key=entity_type)
    entities = dbm.get_many([row.id for row in rows], Entity)

    return entities


def get_entities_by_value(dbm, label, value, as_of=None):
    assert isinstance(dbm, DatabaseManager)
    assert isinstance(label, DataDictType) or is_string(label)
    assert as_of is None or isinstance(as_of, datetime)
    if isinstance(label, DataDictType):
        label = label.slug

    rows = dbm.load_all_rows_in_view(u'by_label_value', key=[label, value])
    entities = dbm.get_many([row[u'value'] for row in rows], Entity)

    return [e for e in entities if e.values({label: u'latest'}, asof=as_of) == {label: value}]


def get_entities_in(dbm, geo_path, type_path=None):
    """
    Retrieve an entity within the given fully-qualified geographic placename.
    """
    assert isinstance(dbm, DatabaseManager)
    assert is_string(geo_path) or isinstance(geo_path, list)
    assert is_string(type_path) or isinstance(type_path, list) or type_path is None

    if is_string(geo_path):
        geo_path = [geo_path]
    if is_string(type_path):
        type_path = [type_path]

    entities = []

    # if type is unspecified, then return all entities
    if type_path is not None:
        # TODO: is the type field necessarily a heirarchy?
        # if not, then this needs to perform a query for each type and then take the intersection
        # of the result sets
        rows = dbm.load_all_rows_in_view(u'by_type_geo', key=(type_path + geo_path))
        entities = dbm.get_many([row.id for row in rows], Entity)

    # otherwise, filter by type
    if type_path is None:
        rows = dbm.load_all_rows_in_view(u'by_geo', key=geo_path)
        entities = dbm.get_many([row.id for row in rows], Entity)

    return entities


def get_all_entities(dbm, include_docs=False):
    rows = dbm.load_all_rows_in_view("by_short_codes", reduce=False, include_docs=include_docs)
    return [_from_row_to_entity(dbm, row) for row in rows]


def _from_row_to_entity(dbm, row):
    pass
#    return Entity.new_from_doc(dbm=dbm, doc=Entity.__document_class__.wrap(row.get('doc')))

#TODO Implement a method in database which hits db only once.
def get_entities(dbm, list_of_uuids):
    assert type(list_of_uuids) is list
    return [get_by_uuid(dbm,uuid) for uuid in list_of_uuids]

def get_by_uuid(dbm, uuid):
    assert type(uuid) is str or type(uuid) is unicode
    doc = dbm.get_entity(uuid)
    if doc is not None:
        return Entity(dbm, doc['entity_type'], doc['location'], doc['aggregation_paths'],
                 doc['geometry'], doc['centroid'], doc['gr_id'], doc['uuid'], doc['short_code'])
    raise EntityNotFoundException("Entity not found for uuid: %s" % uuid)

class Entity(DataObject):
    """
    The Entity class is the primary way for a developer to add save
    data to the database.
    """

    __collection__ = settings.ENTITY_COLLECTION

    def __init__(self, dbm, entity_type=None, location=None, aggregation_paths=None,
                 geometry=None, centroid=None, gr_id=None, uuid=None, short_code=None):
        """
        Construct a new entity.

        Note: _couch_document is used for 'protected' factory methods and
        should not be passed in standard construction.

        If _couch_document is passed, the other args are ignored

        entity_type may be a string (flat type) or sequence (hierarchical type)
        """
        assert isinstance(dbm, DatabaseManager)
        assert entity_type is None or is_sequence(entity_type) or is_string(entity_type)
        assert location is None or is_sequence(location)
        assert aggregation_paths is None or isinstance(aggregation_paths, dict)
        assert geometry is None or isinstance(geometry, dict)
        assert centroid is None or isinstance(centroid, list)
        assert gr_id is None or is_string(gr_id)
        DataObject.__init__(self, dbm)

        # Are we being constructed from an existing doc, in which case all the work is
        # in _set_document?
        if entity_type is None:
            return

        # add aggregation paths
        if is_string(entity_type):
            entity_type = [entity_type]
        self._data['entity_type'] = self.entity_type = entity_type

        self._data['location'] = self.location = location

        self._data['geometry'] = self.geometry = geometry

        self._data['centroid'] = self.centroid = centroid

        self._data['gr_id'] = self.gr_id = gr_id

        self._data['short_code'] = self.short_code = short_code

        self._data['aggregation_paths'] = {}
        if aggregation_paths is not None:
            reserved_names = (attributes.TYPE_PATH, attributes.GEO_PATH)
            for name in aggregation_paths.keys():
                if name in reserved_names:
                    raise ValueError(u'Attempted to add an aggregation path with a reserved name')
                self.set_aggregation_path(name, aggregation_paths[name])

        self._data['uuid'] = self.uuid = uuid if uuid is not None else str(uuid4())

    @property
    def aggregation_paths(self):
        """
        Returns a copy of the dict
        """
        return copy.deepcopy(self._data['aggregation_paths'])


    @property
    def type_path(self):
        """
        Returns a copy of the path
        """
        return list(self.entity_type)

    @property
    def location_path(self):
        """
        Returns a copy of the path
        """
        return list(self.location) if self.location is not None else []


    @property
    def type_string(self):
        """
        An Entity's type is a list of strings. Return this Entity's
        type list joined with a period. If there are no types in the
        list return an empty string.

        """
        p = self.type_path
        return u'' if p is None else u'.'.join(p)

    @property
    def location_string(self):
        """
        An Entity's location is a list of strings. Return this
        Entity's location list joined with a period. If the location
        list is empty return the empty string.
        """
        p = self.location_path
        return u'' if p is None else u'.'.join(p)

    def set_aggregation_path(self, name, path):
        assert is_string(name) and is_not_empty(name)
        assert is_sequence(path) and is_not_empty(path)

        assert isinstance(self._data[attributes.AGG_PATHS], dict)
        self._data[attributes.AGG_PATHS][name] = list(path)
        print self._data

        # TODO: Depending on implementation we will need to update
        # aggregation paths on data records, in which case we need to
        # set a dirty flag and handle this in save.

    def add_data(self, data=(), event_time=None, submission=None, multiple_records=False):
        """
        Add a new datarecord to this Entity and return a UUID for the datarecord.
        Arguments:
            data: a sequence of ordered tuples, (label, value, type)
                where type is a DataDictType
            event_time: the time at which the event occured rather than
                when it was reported
            submission_id: an id to a 'submission' document in the
                submission log from which this data came
        """
        assert is_sequence(data)
        assert event_time is None or isinstance(event_time, datetime)
        assert self.uuid is not None, u"id should never be none, even if haven't been saved,an entity should have a UUID."
        # TODO: should we have a flag that says that this has been
        # saved at least once to avoid adding data records for an
        # Entity that may never be saved? Should docs just be saved on
        # init?
        if event_time is None:
            event_time = utcnow()
        for (label, value, dd_type) in data:
            if not isinstance(dd_type, DataDictType) or is_empty(label):
                raise ValueError(u'Data must be of the form (label, value, DataDictType).')
        #self.update_latest_data(data=data) #Optimization to cache the latest value submitted in entity
        if multiple_records:
            data_list = []
            for (label, value, dd_type) in data:
                data_record = DataRecordDocument(
                    entity_doc=self._doc,
                    event_time=event_time,
                    data=[(label, value, dd_type)],
                    submission=submission
                )   
                data_list.append(data_record)
            return self._dbm._save_documents(data_list)
        else:
            data_record_doc = DataRecordDocument(
                entity_doc=self._doc,
                event_time=event_time,
                data=data,
                submission=submission
            )
            return self._dbm._save_document(data_record_doc)

    def update_latest_data(self, data):
        for (label, value, dd_type) in data:
            self.data[label] = {'value': value, 'type': dd_type._doc.unwrap()}
        self.save()

    def invalidate_data(self, uid):
        """
        Mark datarecord identified by uid as 'invalid'.

        Can be used to mark a submitted record as 'bad' so that
        it will be ignored in reporting. This is because we
        don't want to delete submitted data, even if it is
        erroneous
        """
        self._dbm.invalidate(uid)

    def invalidate(self):
        """
        Mark the entity as invalid.
        This will also mark all associated data records as invalid.
        """
        self.void = True
        self.save()
        for id in self._get_data_ids():
            self.invalidate_data(id)

    def _get_data_ids(self):
        """
        Returns a list of all data documents ids for this entity.
        This should only be used internally to perform update actions on data records as necessary.
        """
        rows = self._get_rows()
        return [row.id for row in rows]

    def _get_rows(self):
        """
        Return a list of all the data records associated with this
        entity.
        """
        return self._dbm.load_all_rows_in_view(u'entity_data', key=self.uuid)

    def get_all_data(self):
        """
        Return a dict where the first level of keys is the event time,
        the second level is the data dict type slug, and the third
        contains the value.
        """
        rows = self._dbm.load_all_rows_in_view(u'id_time_slug_value', key=self.uuid)
        result = defaultdict(dict)
        for row in rows:
            row = row[u'value']
            result[row[u'event_time']][row['slug']] = row['value']
        return result

    def data_types(self, tags=None):
        """
        Returns a list of each type of data that is stored on this entity
        """
        assert tags is None or isinstance(tags, list) or is_string(tags)
        if tags is None or is_empty(tags):
            rows = self._dbm.load_all_rows_in_view(u'entity_datatypes', key=self.uuid)
            result = get_datadict_types(self._dbm, [row[u'value'] for row in rows])
        else:
            if is_string(tags):
                tags = [tags]
            keys = []
            for tag in tags:
                rows = self._dbm.load_all_rows_in_view(u'entity_datatypes_by_tag', key=[self.uuid, tag])
                keys.append([row[u'value'] for row in rows])
            ids_with_all_tags = list(set.intersection(*map(set, keys)))
            result = get_datadict_types(self._dbm, ids_with_all_tags)
        return result

    def state(self):
        """
        Returns a dictionary containing the current state of the entity.
        Contains the latest value of each type of data stored on the entity.
        """
        return dict([(dd_type.slug, self.value(dd_type.slug)) for dd_type in self.data_types()])


    def value(self, label):
        """
            Returns the latest value for the given label.
        """
        assert isinstance(label, DataDictType) or is_string(label)
        if isinstance(label, DataDictType):
            label = label.slug
        field = self.data.get(label)
        return field.get('value') if field is not None else None

    def values(self, aggregation_rules, asof=None):
        """
        Return a dictionary of aggregated values. The keys are the
        attribute label, each value is the aggregated value for the
        given fields using the aggregation function specified for data
        collected till a point in time.
        Eg: aggregation_rules={'arv':'latest', 'num_patients':'sum'}
        will return latest value for arv and sum the number of
        patients.
        """
        # todo: I think we need to simplify this method a bit and
        # expose some of the ViewResults goodness.
        asof = asof or utcnow()
        result = {}
        for field, aggregate_fn in aggregation_rules.items():
            view_name = self._translate(aggregate_fn)
            result[field] = self._get_aggregate_value(field, view_name, asof)
        return result

    def _get_aggregate_value(self, field, aggregate_fn, date):
        entity_id = self.uuid
        time_since_epoch_of_date = int(mktime(date.timetuple())) * 1000
        rows = self._dbm.load_all_rows_in_view(aggregate_fn, group_level=3, descending=False,
                                               startkey=[self.type_path, entity_id, field],
                                               endkey=[self.type_path, entity_id, field, time_since_epoch_of_date])
        # The above will return rows in the format described:
        # Row key=['clinic', 'e4540e0ae93042f4b583b54b6fa7d77a'],
        #   value={'beds': {'timestamp_for_view': 1420070400000, 'value': '15'},
        #           'entity_id': {'value': 'e4540e0ae93042f4b583b54b6fa7d77a'}, 'document_type': {'value': 'Entity'},
        #           'arv': {'timestamp_for_view': 1420070400000, 'value': '100'}, 'entity_type': {'value': 'clinic'}
        #           }
        #  The aggregation map-reduce view will return only one row for an entity-id
        # From this we return the field we are interested in.
        # TODO: Hardcoding to 'latest' for now. Generalize to any aggregation function.
        return rows[0][u'value'][u'latest'] if len(rows) else None

    def _translate(self, aggregate_fn):
        view_names = {u"latest": u"by_values_latest_by_time"}
        return view_names[aggregate_fn] if aggregate_fn in view_names else aggregate_fn
