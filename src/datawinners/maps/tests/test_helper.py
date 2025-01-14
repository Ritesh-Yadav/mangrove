# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import unittest
from unittest.case import SkipTest
from mock import Mock
from datawinners.maps import helper
from mangrove.datastore.database import DatabaseManager
from mangrove.datastore.entity import Entity


class TestHelper(unittest.TestCase):
    def setUp(self):
        self.dbm = Mock(spec=DatabaseManager)

    def test_should_create_location_geojson(self):
        expected_geojson = '{"type": "FeatureCollection", "features": [{"geometry": {"type": "Point", "coordinates": [2, 1]}, "type": "Feature"}, {"geometry": {"type": "Point", "coordinates": [3, 1]}, "type": "Feature"}]}'
        entity1 = Entity(self.dbm, entity_type="Water Point", location=["India", "MH", "Pune"], short_code="WP002",
                         geometry={'type': 'Point', 'coordinates': [1, 2]})
        entity2 = Entity(self.dbm, entity_type="Water Point", location=["India", "MH", "Pune"], short_code="WP002",
                         geometry={'type': 'Point', 'coordinates': [1, 3]})
        entity_list = [entity1, entity2]
        self.assertEqual(expected_geojson, helper.create_location_geojson(entity_list))

    def test_should_create_location_geojson_for_unknown_location(self):
        expected_geojson = '{"type": "FeatureCollection", "features": []}'
        entity1 = Entity(self.dbm, entity_type="Water Point", location=["India", "MH", "Pune"], short_code="WP002")
        entity_list = [entity1]
        self.assertEqual(expected_geojson, helper.create_location_geojson(entity_list))

    @SkipTest
    #fixed this when centriod is implemented for the new shape files
    def test_should_resolve_location_to_centriod(self):
        expected_geojson = '{"type": "FeatureCollection", "features": [{"geometry": {"type": "Point", "coordinates": [48.41586788688786, -17.814011993472985]}, "type": "Feature"}, {"geometry": {"type": "Point", "coordinates": [3, 1]}, "type": "Feature"}]}'
        entity1 = Entity(self.dbm, entity_type="Water Point",
                         location=['Madagascar', 'TOAMASINA', 'ALAOTRA MANGORO', 'AMBATONDRAZAKA', 'AMBATONDRAZAKA'],
                         short_code="WP002",
                         geometry={})
        entity2 = Entity(self.dbm, entity_type="Water Point", location=["India", "MH", "Pune"], short_code="WP002",
                         geometry={'type': 'Point', 'coordinates': [1, 3]})
        entity_list = [entity1, entity2]
        self.assertEqual(expected_geojson, helper.create_location_geojson(entity_list))

    def test_should_not_raise_exception_if_no_location_or_geo_code_specified(self):
        entity = Entity(self.dbm, entity_type="Water Point", short_code="WP002")
        helper.create_location_geojson(entity_list=[entity])
