# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

import copy
from datetime import datetime
from documents import EntityDocument, DataRecordDocument

from utils import is_not_empty, is_sequence, is_string, is_number
from database import get_db_manager

_view_names = { "latest" : "by_values" }

def get(uuid):
    entity_doc = get_db_manager().load(uuid, EntityDocument)
    e = Entity(_document = entity_doc)
    return e

def get_entities(uuids):
    return [ get(i) for i in uuids ]

def entities_for_attributes(attrs):
    '''
    retrieve entities with datarecords with the given
    named attributes. Can be used to search for entities
    by identifying info like a phone number

    Include 'type' as an attr to restrict to a given entity type

    returns a sequence of 0, 1 or more matches

    ex:
    attrs = { 'type':'clinic', 'name': 'HIV Clinic' }
    print entities_for_attributes(attrs)

    '''

    pass

# geo aggregation specific calls
def entities_near(geocode, radius=1, attrs=None):
    '''
    Retrieve an entity within the given radius (in kilometers) of
    the given geocode that matches the given attrs

    Include 'type' as an attr to restrict to a given entity type

    returns a sequence

    '''
    pass

def entities_in(geoname, attrs=None):
    '''
    Retrieve an entity within the given fully-qualified geographic
    placename.

    Include 'type' as an attr to restrict to a given entity type

    returns a sequence

    ex.
    found = entities_in(
    [us,ca,sanfrancisco],
    {'type':'patient', 'phone':'4155551212'}
    )

    '''
    pass


#
# Constants
#

# use 'classes' to group constants
class attribute_names(object):
    MODIFIED = 'modified'
    CREATED = 'created'
    EVENT_TIME = 'event_time'
    ENTITY_ID = 'entity_id'
    SUBMISSION_ID = 'submission_id'
    AGG_PATHS = 'aggregation_paths'
    GEO_PATH = '_geo'
    TYPE_PATH = '_type'
    DATA = 'data'




# Entity class is main way of interacting with Entities AND datarecords.
# Datarecords are always submitted/retrieved from an Entity




class Entity(object):
    """
        Entity class is main way of interacting with Entities AND datarecords.
    """

    def __init__(self, entity_type = None,location=None, aggregation_paths = None, _document = None):
        '''Construct a new entity.

        Note: _couch_document is used for 'protected' factory methods and
        should not be passed in standard construction.

        If _couch_document is passed, the other args are ignored

        entity_type may be a string (flat type) or sequence (hierarchical type)
        '''
        assert _document is not None or entity_type is None or is_sequence(entity_type) or is_string(entity_type)
        assert _document is not None or location is None or is_sequence(location)
        assert _document is not None or aggregation_paths is None or isinstance(aggregation_paths, dict)
        assert _document is None or isinstance(_document, EntityDocument)

        # Are we being constructed from an existing doc?
        if _document is not None:
            self._doc = _document
            return

        # Not made from existing doc, so create a new one
        self._doc = EntityDocument()

        # add aggregation paths
        if entity_type is not None:
            if is_string(entity_type):
                entity_type=[entity_type]
            self.set_aggregation_path(attribute_names.TYPE_PATH, entity_type)

        if location is not None:
            self.set_aggregation_path(attribute_names.GEO_PATH, location)

        if aggregation_paths is not None:
            reserved_names = (attribute_names.TYPE_PATH, attribute_names.GEO_PATH)
            for name in aggregation_paths.keys():
                if name in reserved_names:
                    raise ValueError('Attempted to add an aggregation path with a reserved name')
                self.set_aggregation_path(name, aggregation_paths[name])

        # Set 'entity_type' as it is still used in map/reduces
        # TODO: Remove when we remove entity_type
        if entity_type is not None:
            self._doc['entity_type'] = ('' if entity_type is None else
                                        '_'.join([unicode(i) for i in entity_type]))


        # TODO: why should Entities just be saved on init??



    def save(self):
        return get_db_manager().save(self._doc).id

    @property
    def id(self):
        return self._doc.id

    @property
    def aggregation_paths(self):
        return copy.deepcopy(self._doc.aggregation_paths)

    @property
    def entity_type(self):
        et = None
        try:
            et = self._doc['entity_type']
        except:
            pass
        return et

    def set_aggregation_path(self, name, path):
        assert self._doc is not None
        assert is_string(name) and is_not_empty(name)
        assert is_sequence(path) and is_not_empty(path)

        assert isinstance(self._doc[attribute_names.AGG_PATHS], dict)
        self._doc[attribute_names.AGG_PATHS][name]=list(path)

        # TODO: Depending on implementation we will need to update aggregation paths
        # on data records--in which case we need to set a dirty flag and handle this
        # in save

    def add_data(self, data = (), submission_id = None, reported_on = None):
        '''Add a new datarecord to this Entity and return a UUID for the datarecord.

        Arguments:
        data -- a sequence of n-tuples in form of (key, value, <optional type>)
                e.g. [('name','bob','string'), ('age',20,'numeric')]
        submission_id -- an id to a 'submission' document in the submission log from which
                        this data came
        event_time -- the time at which the event occured rather than when it was reported

        This is stored in couch as:
            submission_id = "..."
            event_time = "..."
            attributes: {
                            'name': {
                                'value': 'bob',
                                'type': 'string'
                            },
                            'age': {
                                'value': '20',
                                'type': 'numeric'
                            },
                        }
        '''
        assert is_sequence(data)
        assert self.id is not None # should never be none, even if haven't been saved, should have a UUID
        # TODO: should we have a flag that says that this has been saved at least once to avoid adding data
        # records for an Entity that may never be saved? Should docs just be saved on init?

        data_dict = {}
        for d in data:
            if len(d)<2 or len(d)>3:
                raise ValueError('data for a data record must be tuple of (name, value) or triple of (name,value,type)')

            name = d[0]
            value = d[1]
            # figure out type. Warning, nasty if chain!
            # TODO: make types enums
            # TODO: Should we have a 'coordinate' or geocode type?
            typ = 'unknown'
            if len(d)==3:
                typ = d[2]
            elif is_number(value):
                typ = 'numeric'
            elif isinstance(value, bool):
                typ = 'boolean'
            elif isinstance(value, datetime):
                typ = 'datetime'
            elif is_string(value):
                typ = 'text'

            data_dict[name] = { 'value': value, 'type': typ }

        data_record_doc = DataRecordDocument(entity_doc = self._doc, reported_on = reported_on, attributes = data_dict)
        return get_db_manager().save(data_record_doc).id

    # Note: The below has not been implemented yet.

    def update_datarecord(self,uid,record_dict):
        '''
        Invalidates the record identified by the passed 'uid'
  	 	
        and creates a new one using the record_dict.
  	 	
  	 	
        This can be used to _correct_ bad submissions.
  	 	
  	 	
        Returns uid of new corrected record

  	 	
        '''
  	 	
        self.invalidate_datarecord(uid)
        return self.submit_data_record(record_dict)
  	 	
  	 	
    def invalidate_datarecord(self,uid):
  	 	
        '''
  	 	
        Mark datarecord identified by uid as 'invalid'
  	 	
  	 	
        Can be used to mark a submitted record as 'bad' so that

  	 	
        it will be ignored in reporting. This is because we

  	 	
        don't want to delete submitted data, even if it is

  	 	
        erroneous.
  	 	
        '''
  	 	
        pass


    def values(self, aggregation_rules, asof = None):
        """
        returns the aggregated value for the given fields using the aggregation function specified for data collected till a point in time.
         Eg: data_records_func = {'arv':'latest', 'num_patients':'sum'} will return latest value for ARV and sum of number of patients
        """
        asof = asof or datetime.now()
        result = {}
        
        for field,aggregate_fn in aggregation_rules.items():
            view_name = self._translate(aggregate_fn)
            result[field] = self._get_aggregate_value(field,view_name,asof)
        return result


    def _get_aggregate_value(self, field, aggregate_fn,date):
        entity_id = self._doc.id
        rows = get_db_manager().load_all_rows_in_view('mangrove_views/'+aggregate_fn, group_level=2,descending=False,
                                                     startkey=[self.entity_type, entity_id],
                                                     endkey=[self.entity_type, entity_id, date.year, date.month, date.day, {}])
        # The above will return rows in the format described:
        # Row key=['clinic', 'e4540e0ae93042f4b583b54b6fa7d77a'],
        #   value={'beds': {'timestamp_for_view': 1420070400000, 'value': '15'},
        #           'entity_id': {'value': 'e4540e0ae93042f4b583b54b6fa7d77a'}, 'document_type': {'value': 'Entity'},
        #           'arv': {'timestamp_for_view': 1420070400000, 'value': '100'}, 'entity_type': {'value': 'clinic'}
        #           }
        #  The aggregation map-reduce view will return only one row for an entity-id
        # From this we return the field we are interested in.
        return rows[0]['value'][field]['value'] if len(rows) else None

    def _translate(self, aggregate_fn):
        return _view_names.get(aggregate_fn) or aggregate_fn





    




    
