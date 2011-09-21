# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from datetime import datetime
from pytz import UTC
from mangrove.datastore.datadict import DataDictType
from mangrove.datastore.entity import Entity, get_by_short_code, create_entity, get_all_entities, DataRecord
from mangrove.datastore.entity_type import define_type
from mangrove.datastore.tests.test_data import TestData
from mangrove.errors.MangroveException import  DataObjectAlreadyExists, EntityTypeDoesNotExistsException, DataObjectNotFound
from mangrove.utils.test_utils.mangrove_test_case import MangroveTestCase


class TestEntity(MangroveTestCase):
    def test_create_entity(self):
        e = Entity(self.manager, entity_type="clinic", location=["India", "MH", "Pune"])
        uuid = e.save()
        self.assertTrue(uuid)
        self.manager.delete(e)

    def test_create_entity_with_id(self):
        e = Entity(self.manager, entity_type="clinic", location=["India", "MH", "Pune"], id="-1000")
        uuid = e.save()
        self.assertEqual(uuid, "-1000")
        self.manager.delete(e)

    def test_get_entity(self):
        test_data = TestData(self.manager)
        e = get(self.manager, test_data.entity1.id)
        self.assertTrue(e.id)
        print e.type_string
        self.assertTrue(e.type_string == test_data.entity_type_string)

    def test_should_add_location_hierarchy_on_create(self):
        e = Entity(self.manager, entity_type="clinic", location=["India", "MH", "Pune"])
        uuid = e.save()
        saved = get(self.manager, uuid)
        self.assertEqual(saved.location_path, ["India", "MH", "Pune"])

    def test_should_return_empty_list_if_location_path_is_not_stored(self):
        e = Entity(self.manager, entity_type="clinic")
        uuid = e.save()
        saved = get(self.manager, uuid)
        self.assertEqual(saved.location_path, [])

    def test_should_create_entity_with_short_code(self):
        with self.assertRaises(AssertionError):
            entity = create_entity(self.manager, entity_type=["reporter"], short_code=None)

        with self.assertRaises(AssertionError):
            entity = create_entity(self.manager, entity_type=["reporter"], short_code="")

        with self.assertRaises(AssertionError):
            entity = create_entity(self.manager, entity_type="Reporter", short_code="BLAH")
        with self.assertRaises(AssertionError):
            entity = create_entity(self.manager, entity_type=[], short_code="BLAH")
        with self.assertRaises(AssertionError):
            entity = create_entity(self.manager, entity_type=("reporter"), short_code="BLAH")

        define_type(self.manager, ["reporter"])
        entity = create_entity(self.manager, entity_type=["reporter"], short_code="ABC")
        saved_entity = get_by_short_code(self.manager, short_code="ABC", entity_type=["reporter"])
        self.assertEqual(saved_entity.id, entity.id)

        with self.assertRaises(DataObjectAlreadyExists):
            create_entity(self.manager, entity_type=["reporter"], short_code="ABC")

        with self.assertRaises(EntityTypeDoesNotExistsException):
            create_entity(self.manager, entity_type=["Dog"], short_code="ABC")


    def test_should_get_entity_by_short_code(self):
        reporter = Entity(self.manager, entity_type=["Reporter"], location=["Pune", "India"], short_code="repx")
        reporter.save()

        entity = get_by_short_code(self.manager, short_code="repx", entity_type=["Reporter"])
        self.assertTrue(entity is not None)
        self.assertEqual("repx", entity.short_code)

        with self.assertRaises(DataObjectNotFound):
            entity = get_by_short_code(self.manager, short_code="ABC", entity_type=["Waterpoint"])

    def test_should_get_all_entities(self):
        test_data = TestData(self.manager)
        entities = get_all_entities(self.manager)
        self.assertEqual(3, len(entities))
        self.assertEqual(test_data.entity1.short_code, entities[0].short_code)
        self.assertEqual(test_data.entity2.short_code, entities[1].short_code)
        self.assertEqual(test_data.entity3.short_code, entities[2].short_code)

    def test_hierarchy_addition(self):
        test_data = TestData(self.manager)
        e = get(self.manager, test_data.entity1.id)
        org_hierarchy = ["TWGlobal", "TW-India", "TW-Pune"]
        e.set_aggregation_path("org", org_hierarchy)
        e.save()
        saved = get(self.manager, test_data.entity1.id)
        self.assertTrue(saved.aggregation_paths["org"] == ["TWGlobal", "TW-India", "TW-Pune"])

    def test_hierarchy_addition_should_clone_tree(self):
        test_data = TestData(self.manager)
        e = get(self.manager, test_data.entity1.id)
        org_hierarchy = ["TW", "PS", "IS"]
        e.set_aggregation_path("org", org_hierarchy)
        org_hierarchy[0] = ["NewValue"]
        e.save()
        saved = get(self.manager, test_data.entity1.id)
        self.assertTrue(saved.aggregation_paths["org"] == ["TW", "PS", "IS"])

    def test_save_aggregation_path_only_via_api(self):
        test_data = TestData(self.manager)
        e = get(self.manager, test_data.entity1.id)
        e.location_path[0] = "US"
        e.save()
        saved = get(self.manager, test_data.entity1.id)
        self.assertTrue(saved.location_path == [u'India', u'MH', u'Pune'])  # Hierarchy has not changed.

    def test_should_save_hierarchy_tree_only_through_api(self):
        test_data = TestData(self.manager)
        e = get(self.manager, test_data.entity1.id)
        org_hierarchy = ["TW", "PS", "IS"]
        e.set_aggregation_path("org", org_hierarchy)
        e.save()
        e.aggregation_paths['org'][0] = "XYZ"
        e.save()
        saved = get(self.manager, test_data.entity1.id)
        self.assertEqual(saved.aggregation_paths["org"], ["TW", "PS", "IS"])

    def test_get_entities(self):
        test_data = TestData(self.manager)
        e2 = Entity(self.manager, "hospital", ["India", "TN", "Chennai"])
        id2 = e2.save()
        entities = get_entities(self.manager, [test_data.entity1.id, id2])
        self.assertEqual(len(entities), 2)
        saved = dict([(e.id, e) for e in entities])
        self.assertEqual(saved[id2].type_string, "hospital")
        self.assertEqual(saved[test_data.entity1.id].type_string, test_data.entity_type_string)
        self.manager.delete(e2)

    def test_should_add_passed_in_hierarchy_path_on_create(self):
        e = Entity(self.manager, entity_type=["HealthFacility", "Clinic"], location=["India", "MH", "Pune"],
                   aggregation_paths={"org": ["TW_Global", "TW_India", "TW_Pune"],
                                      "levels": ["Lead Consultant", "Sr. Consultant", "Consultant"]})
        uuid = e.save()
        saved = get(self.manager, uuid)
        hpath = saved._doc.aggregation_paths
        self.assertEqual(hpath["org"], ["TW_Global", "TW_India", "TW_Pune"])
        self.assertEqual(hpath["levels"], ["Lead Consultant", "Sr. Consultant", "Consultant"])

    def test_should_add_entity_type_on_create(self):
        e = Entity(self.manager, entity_type=["healthfacility", "clinic"])
        uuid = e.save()
        saved = get(self.manager, uuid)
        self.assertEqual(saved.type_path, ["healthfacility", "clinic"])

    def test_should_add_entity_type_on_create_as_aggregation_tree(self):
        e = Entity(self.manager, entity_type="health_facility")
        uuid = e.save()
        saved = get(self.manager, uuid)
        self.assertEqual(saved.type_path, ["health_facility"])

    def test_should_add_passed_in_hierarchy_path_on_create(self):
        e = Entity(self.manager, entity_type=["HealthFacility", "Clinic"], location=["India", "MH", "Pune"],
                   aggregation_paths={"org": ["TW_Global", "TW_India", "TW_Pune"],
                                      "levels": ["Lead Consultant", "Sr. Consultant", "Consultant"]})
        uuid = e.save()
        saved = get(self.manager, uuid)
        hpath = saved._doc.aggregation_paths
        self.assertEqual(hpath["org"], ["TW_Global", "TW_India", "TW_Pune"])
        self.assertEqual(hpath["levels"], ["Lead Consultant", "Sr. Consultant", "Consultant"])

    def test_should_create_entity_from_document(self):
        test_data = TestData(self.manager)
        existing = self.manager.get(test_data.entity1.id, Entity)
        e = Entity.new_from_doc(self.manager, existing._doc)
        self.assertTrue(e._doc is not None)
        self.assertEqual(e.id, existing.id)
        self.assertEqual(e.type_path, existing.type_path)

    def test_latest_value_are_stored_in_entity(self):
        test_data = TestData(self.manager)
        data_record = [('meds', 30, test_data.dd_types['meds']),
            ('doc', "asif", test_data.dd_types['doctors']),
            ('facility', 'clinic', test_data.dd_types['facility']),
            ('opened_on', datetime(2011, 01, 02, tzinfo=UTC), test_data.dd_types['facility'])]
        data_record_id = test_data.entity1.add_data(data=data_record,
                                                    event_time=datetime(2011, 01, 02, tzinfo=UTC),
                                                    submission=dict(submission_id="123456"))
        self.assertTrue(data_record_id is not None)
        updated_clinic_entity = get_by_short_code(dbm=self.manager, short_code=test_data.entity1.short_code,
                                                  entity_type=test_data.ENTITY_TYPE)
        self.assertEqual(30, updated_clinic_entity.data['meds']['value'])
        self.assertEqual('asif', updated_clinic_entity.data['doc']['value'])
        self.assertEqual('clinic', updated_clinic_entity.data['facility']['value'])

    def test_invalidate_data(self):
        test_data = TestData(self.manager)
        data_record_id = test_data.entity1.add_data([('arv', 20, test_data.dd_types['meds'])])
        valid_doc = DataRecord.get(self.manager, data_record_id)
        self.assertFalse(valid_doc.voided)
        test_data.entity1.invalidate_data(data_record_id)
        invalid_doc = DataRecord.get(self.manager, data_record_id)
        self.assertTrue(invalid_doc.voided)

    def test_all_data_record_are_invalidated_when_entity_is_invalidated(self):
        e = Entity(self.manager, entity_type='store', location=['nyc'])
        e.save()
        self.assertFalse(e._doc.void)
        apple_type = DataDictType(self.manager, name='Apples', slug='apples', primitive_type='number')
        orange_type = DataDictType(self.manager, name='Oranges', slug='oranges', primitive_type='number')
        apple_type.save()
        orange_type.save()
        data = [
            [('apples', 20, apple_type), ('oranges', 30, orange_type)],
            [('apples', 10, apple_type), ('oranges', 20, orange_type)]
        ]
        data_ids = []
        for d in data:
            id = e.add_data(d)
            self.assertFalse(self.manager._load_document(id).void)
            data_ids.append(id)
        e.invalidate()
        self.assertTrue(e._doc.void)
        for id in data_ids:
            self.assertTrue(self.manager._load_document(id).void)

    def test_should_return_data_types(self):
        med_type = DataDictType(self.manager,
                                name='Medicines',
                                slug='meds',
                                primitive_type='number',
                                description='Number of medications',
                                tags=['med'])
        med_type.save()
        doctor_type = DataDictType(self.manager,
                                   name='Doctor',
                                   slug='doc',
                                   primitive_type='string',
                                   description='Name of doctor',
                                   tags=['doctor', 'med'])
        doctor_type.save()
        facility_type = DataDictType(self.manager,
                                     name='Facility',
                                     slug='facility',
                                     primitive_type='string',
                                     description='Name of facility')
        facility_type.save()
        e = Entity(self.manager, entity_type='foo')
        e.save()
        data_record = [('meds', 20, med_type),
            ('doc', "aroj", doctor_type),
            ('facility', 'clinic', facility_type)]
        e.add_data(data_record)
        # med (tag in list)
        types = [typ.slug for typ in e.data_types(['med'])]
        self.assertTrue(med_type.slug in types)
        self.assertTrue(doctor_type.slug in types)
        self.assertTrue(facility_type.slug not in types)
        # doctor (tag as string)
        types = [typ.slug for typ in e.data_types('doctor')]
        self.assertTrue(doctor_type.slug in types)
        self.assertTrue(med_type.slug not in types)
        self.assertTrue(facility_type.slug not in types)
        # med and doctor (more than one tag)
        types = [typ.slug for typ in e.data_types(['med', 'doctor'])]
        self.assertTrue(doctor_type.slug in types)
        self.assertTrue(med_type.slug not in types)
        self.assertTrue(facility_type.slug not in types)
        # no tags
        types = [typ.slug for typ in e.data_types()]
        self.assertTrue(med_type.slug in types)
        self.assertTrue(doctor_type.slug in types)
        self.assertTrue(facility_type.slug in types)


def get_entities(dbm, ids):
    return dbm.get_many(ids, Entity)

# Adaptor methods to old api
def get(dbm, id):
    return dbm.get(id, Entity)
