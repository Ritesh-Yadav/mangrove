import datetime as d
from time import sleep
from mock import  patch
from services.repository.repository import RepositoryForTests
from services.repository.connection import Connection
from services.entity_management.entity_management_service import EntityManagementService
from services.entity_management.models import Entity
from uuid import uuid4
from services.data_record.data_record_service import DataRecordService
from services.data_record.models import DataRecord


class TestDataRecordApi(object):

    test_data_record_id = ''

    def setup(self):
        self.repository = RepositoryForTests(Connection())

    def teardown(self):
#        pass
        self.repository.delete_database()

    def create_clinic(self,id,location,name):

        entity_service = EntityManagementService(self.repository)
        clinic= Entity(id=id,entity_type = 'clinic',name=name,aggregation_trees={"location":location})
        clinic = entity_service.create_entity(clinic)
        return clinic

    def create_reporter(self,id,name,org_chart,age):
        entity_service = EntityManagementService(self.repository)
        reporter= Entity(id=id,entity_type = 'reporter',name=name,aggregation_trees={"org_chart":org_chart},age=age)
        reporter = entity_service.create_entity(reporter)
        return reporter

    def create_clinic_records(self):
        entity_management_service = EntityManagementService(self.repository)
        entity_management_service.create_views()
        now = d.datetime.now()

        data_service = DataRecordService(self.repository)
        reporter =self.create_reporter(uuid4().hex,"reporter1",["Country Manager","Field Manager","Field Agent"],25)
        clinic = self.create_clinic(uuid4().hex, ["India","Maharashtra","Pune"], "Clinic 1")

        data_record = DataRecord(entity=clinic,reporter=reporter,source = {"phone":'1234',"report":'hn1.2424'},beds = {'value' : 10},arv = {'value' : 100},event_time=now)
        data_service.create_data_record(data_record)
        clinic = self.create_clinic(uuid4().hex, ["India","Karnataka","Bangalore"], "Clinic 2")
        data_record = DataRecord(entity=clinic,reporter=reporter, source = {"phone":'1234',"report":'hn1.2424'}, beds= {'value' : 100}, arv={'value' : 200}, event_time=now)
        data_service.create_data_record(data_record)
        clinic = self.create_clinic(uuid4().hex, ["India","Maharashtra","Mumbai"], "Clinic 3")
        data_record = DataRecord(entity=clinic, reporter=reporter,source = {"phone":'1234',"report":'hn1.2424'}, beds= {'value' : 150}, arv={'value' : 150}, event_time=now)
        data_service.create_data_record(data_record)
        clinic = self.create_clinic(uuid4().hex, ["India","Maharashtra","Pune"], "Clinic 4")
        data_record=DataRecord(clinic, reporter=reporter,source = {"phone":'1234',"report":'hn1.2424'}, beds= {'value' :250}, arv={'value' : 50}, event_time=now)
        data_service.create_data_record(data_record)
        clinic = self.create_clinic(uuid4().hex, ["India","Karnataka","Bangalore"], "Clinic 5")
        data_record = DataRecord(clinic, reporter=reporter,source = {"phone":'1234',"report":'hn1.2424'}, beds= {'value' : 150}, arv={'value' : 150}, event_time=now)
        data_service.create_data_record(data_record)
        clinic = self.create_clinic(uuid4().hex, ["India","Maharashtra","Pune"], "Clinic 6")
        data_record = DataRecord(clinic, reporter=reporter,source = {"phone":'1234',"report":'hn1.2424'}, beds= {'value' : 10}, arv={'value' : 15}, event_time=now)
        data_service.create_data_record(data_record)

    def test_total_num_beds_across_clinics(self):
        #create clinics
        self.create_clinic_records()
        beds = self.fetch_total_num_of_beds()
        assert beds == 670

    def fetch_total_num_of_beds(self):
        rows = self.repository.load_all_rows_in_view('mangrove_views/by_location',group=True, group_level=3)
        for i in rows:
            if i.key == ['clinic', 'beds', 'location']:
                return i.value['sum']
        return 0

    def test_should_get_current_values_for_entity(self):
        entity_management_service = EntityManagementService(self.repository)
        entity_management_service.create_views()
        now = d.datetime.now()
        data_service = DataRecordService(self.repository)
        reporter =self.create_reporter(uuid4().hex,"reporter1",["Country Manager","Field Manager","Field Agent"],25)
        clinic = self.create_clinic(uuid4().hex, ["India","Maharashtra","Pune"], "Clinic 1")
        data_record = DataRecord(entity=clinic,reporter=reporter,source = {"phone":'1234',"report":'hn1.2424'},beds = {'value' : 10},arv = {'value' : 100},event_time=now)
        data_service.create_data_record(data_record)
        sleep(1)
        data_record = DataRecord(entity=clinic,reporter=reporter,source = {"phone":'1234',"report":'hn1.2424'},beds = {'value' : 15},arv = {'value' : 100},event_time=now + d.timedelta(days=30))
        data_service.create_data_record(data_record)

        current_value = entity_management_service.load_attributes_for_entity(clinic.id)
        assert current_value['beds']['value'] == '15'

    def test_should_get_current_values_for_entity_as_on_date(self):
        entity_management_service = EntityManagementService(self.repository)
        entity_management_service.create_views()

        clinic = {}
        data_service = DataRecordService(self.repository)
        reporter =self.create_reporter(uuid4().hex,"reporter1",["Country Manager","Field Manager","Field Agent"],25)

        with patch('services.repository.DocumentBase.DateTime') as dt:
            dt.now.return_value = d.datetime(2005,1,1)
            clinic = self.create_clinic(uuid4().hex, ["India","Maharashtra","Pune"], "Clinic 1")

            data_record = DataRecord(entity=clinic,reporter=reporter,source = {"phone":'1234',"report":'hn1.2424'},beds = {'value' : 10},arv = {'value' : 100})
            data_service.create_data_record(data_record)

        with patch('services.repository.DocumentBase.DateTime') as dt:
            dt.now.return_value = d.datetime(2005,1,1)
            data_record = DataRecord(entity=clinic,reporter=reporter,source = {"phone":'1234',"report":'hn1.2424'},beds = {'value' : 15},arv = {'value' : 100})
            data_service.create_data_record(data_record)

        entity_as_on_date = entity_management_service.load_attributes_for_entity_as_on(clinic.id, d.datetime(2005,3,1))
        assert entity_as_on_date['beds']['value'] == "10"





