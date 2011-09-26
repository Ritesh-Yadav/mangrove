# vim: ai ts=4 sts=4 et sw= encoding=utf-8
from datetime import timedelta, date
from couchdb.mapping import  TextField, ListField, DictField
from django.db.models.fields import IntegerField, CharField, BooleanField
from django.db.models.fields.related import ForeignKey
from datawinners.accountmanagement.models import Organization
from datawinners.entity.import_data import load_all_subjects_of_type
from datawinners.scheduler.deadline import Deadline, Month, Week
from mangrove.datastore.database import  DatabaseManager, DataObject
from mangrove.datastore.documents import DocumentBase, TZAwareDateTimeField
from mangrove.errors.MangroveException import DataObjectAlreadyExists
from mangrove.form_model.form_model import FormModel
from mangrove.transport.reporter import get_reporters_who_submitted_data_for_frequency_period
from mangrove.utils.types import  is_string
from django.db import models

class ReminderMode(object):
    BEFORE_DEADLINE = 'before_deadline'
    ON_DEADLINE = 'on_deadline'
    AFTER_DEADLINE = 'after_deadline'

class RemindTo(object):
    ALL_DATASENDERS = 'all_datasenders'
    DATASENDERS_WITHOUT_SUBMISSIONS = 'datasenders_without_submissions'

class Reminder(models.Model):
    project_id = CharField(null=False, blank=False, max_length=264)
    day = IntegerField(null=True, blank=True)
    message = CharField(max_length=160)
    reminder_mode = CharField(null=False, blank=False, max_length=20, default=ReminderMode.BEFORE_DEADLINE)
    organization = ForeignKey(Organization)
    voided = BooleanField(default=False)
    remind_to = CharField(null=False, blank=False, max_length=50, default=RemindTo.ALL_DATASENDERS)

    def to_dict(self):
        return {'day': self.day, 'message': self.message, 'reminder_mode': self.reminder_mode, 'remind_to': self.remind_to}

    def void(self, void = True):
        self.voided = void
        self.save()

    def should_be_send_on(self,deadline,on_date):
        assert isinstance(on_date,date)
        deadline_date = self._get_applicapable_deadline_date(deadline, on_date)
        return on_date == deadline_date + timedelta(days=self._delta())

    def get_sender_list(self,project,on_date,dbm):
        if self.remind_to == RemindTo.DATASENDERS_WITHOUT_SUBMISSIONS:
            deadline_date = self._get_applicapable_deadline_date(project.deadline(), on_date)
            return project.get_data_senders_without_submissions_for(deadline_date,dbm)
        return project.get_data_senders(dbm)

    def _delta(self):
        if self.reminder_mode == ReminderMode.ON_DEADLINE:
            return 0
        if self.reminder_mode == ReminderMode.BEFORE_DEADLINE:
            return -self.day
        if self.reminder_mode == ReminderMode.AFTER_DEADLINE:
            return self.day

    def _get_applicapable_deadline_date(self, deadline, on_date):
        if self.reminder_mode == ReminderMode.BEFORE_DEADLINE:
            return deadline.next_deadline(on_date)
        else:
            return deadline.current_deadline(on_date)

    def log(self, dbm, project_name, date, sent_status='sent', number_of_sms=0):
        log = ReminderLog(dbm=dbm, reminder=self, project_name=project_name, date=date, sent_status=sent_status,
                    number_of_sms=number_of_sms)
        log.save()
        return log


class ReminderLogDocument(DocumentBase):
    reminder_id = TextField()
    project_name = TextField()
    sent_status = TextField()
    number_of_sms = TextField()
    date = TZAwareDateTimeField()
    message = TextField()
    remind_to = TextField()
    reminder_mode = TextField()

    def __init__(self, id=None, reminder_id=None, project_name=None, sent_status=None, number_of_sms=None, date=None, message=None, remind_to=None, reminder_mode=None):
        DocumentBase.__init__(self,id=id, document_type='ReminderLog')
        self.reminder_id =reminder_id
        self.project_name = project_name
        self.sent_status = sent_status
        self.number_of_sms = number_of_sms
        self.date = date
        self.message = message
        self.remind_to = remind_to
        self.reminder_mode = reminder_mode

class ReminderLog(DataObject):
    __document_class__ = ReminderLogDocument

    def __init__(self, dbm, reminder=None, sent_status=None, number_of_sms=None, date=None, project_name=None):
        DataObject.__init__(self, dbm)
        if reminder is not None:
            if reminder.reminder_mode == ReminderMode.ON_DEADLINE:
                reminder_mode = reminder.reminder_mode
            else:
                reminder_mode = str(reminder.day) + ' days ' + reminder.reminder_mode
            doc = ReminderLogDocument(reminder_id=reminder.id, project_name=project_name, sent_status=sent_status,
                                      number_of_sms=number_of_sms, date=date, message=reminder.message,
                                      remind_to=reminder.remind_to, reminder_mode=reminder_mode)
            DataObject._set_document(self, doc)

class ProjectState(object):
    INACTIVE = 'Inactive'
    ACTIVE = 'Active'
    TEST = 'Test'

class Project(DocumentBase):
    name = TextField()
    goals = TextField()
    project_type = TextField()
    entity_type = TextField()
    activity_report = TextField()
    devices = ListField(TextField())
    qid = TextField()
    state = TextField()
    sender_group = TextField()
    reminder_and_deadline = DictField()
    data_senders = ListField(TextField())
    reminders=ListField(DictField())

    def __init__(self, id=None, name=None, goals=None, project_type=None, entity_type=None, devices=None, state=ProjectState.INACTIVE, activity_report=None, sender_group=None, reminder_and_deadline=None):
        assert entity_type is None or is_string(entity_type), "Entity type %s should be a string." % (entity_type,)
        DocumentBase.__init__(self, id=id, document_type='Project')
        self.devices = []
        self.name = name.lower() if name is not None else None
        self.goals = goals
        self.project_type = project_type
        self.entity_type = entity_type
        self.devices = devices
        self.state = state
        self.activity_report = activity_report
        self.sender_group = sender_group
        self.reminder_and_deadline = reminder_and_deadline if reminder_and_deadline is not None else {}

    def get_data_senders(self,dbm):
        all_data = load_all_subjects_of_type(dbm)
        return [data for data in all_data if data['short_name'] in self.data_senders]

    def get_data_senders_without_submissions_for(self,deadline_date,dbm):
        start_date,end_date = self.deadline().get_applicable_frequency_period_for(deadline_date)
        return get_reporters_who_submitted_data_for_frequency_period(dbm,self.qid, start_date,end_date)

    def deadline(self):
        return Deadline(self._frequency(), self._deadline_type())

    def _frequency(self):
        if self.reminder_and_deadline.get('frequency_period') == 'month':
            return Month(int(self.reminder_and_deadline.get('deadline_month')))
        if self.reminder_and_deadline.get('frequency_period') == 'week':
            return Week(int(self.reminder_and_deadline.get('deadline_week')))


    def has_deadline(self):
        return self.reminder_and_deadline.get('has_deadline') == 'True'

    def frequency_enabled(self):
        return self.reminder_and_deadline.get('frequency_enabled') == 'True'

    def reminders_enabled(self):
        return self.reminder_and_deadline.get('reminders_enabled') == 'True'

    def _deadline_type(self):
        if self.frequency_enabled():
            return self.reminder_and_deadline.get('deadline_type')

    def _frequency_period(self):
        return self.reminder_and_deadline.get('frequency_period')

    def get_deadline_day(self):
        if self.reminder_and_deadline.get('frequency_period') == 'month':
            return int(self.reminder_and_deadline.get('deadline_month'))

    def is_reminder_enabled(self):
        return self.reminder_and_deadline.get('reminders_enabled') == "True"

    def should_send_reminders(self, as_of, days_relative_to_deadline):
        next_deadline_day = self.deadline().current(as_of)
        if next_deadline_day is not None:
            if as_of == next_deadline_day + timedelta(days = days_relative_to_deadline):
                return True
        return False

    def _check_if_project_name_unique(self, dbm):
        rows = dbm.load_all_rows_in_view('project_names', key=self.name)
        if len(rows) and rows[0]['value'] != self.id:
            raise DataObjectAlreadyExists('Project', "Name", "'%s'" % self.name)

    def save(self, dbm):
        assert isinstance(dbm, DatabaseManager)
        self._check_if_project_name_unique(dbm)
        return dbm._save_document(self)

    def update(self, value_dict):
        attribute_list = [item[0] for item in (self.items())]
        for key in value_dict:
            if key in attribute_list:
                setattr(self, key, value_dict.get(key).lower()) if key == 'name' else setattr(self, key,
                                                                                              value_dict.get(key))

    def update_questionnaire(self, dbm):
        form_model = dbm.get(self.qid, FormModel)
        form_model.name = self.name
        form_model.entity_type =  [self.entity_type] if is_string(self.entity_type) else self.entity_type
        form_model.save()

    def activate(self, dbm):
        form_model = dbm.get(self.qid, FormModel)
        form_model.activate()
        form_model.save()
        self.state = ProjectState.ACTIVE
        self.save(dbm)

    def deactivate(self, dbm):
        form_model = dbm.get(self.qid, FormModel)
        form_model.deactivate()
        form_model.save()
        self.state = ProjectState.INACTIVE
        self.save(dbm)

    def to_test_mode(self, dbm):
        form_model = dbm.get(self.qid, FormModel)
        form_model.set_test_mode()
        form_model.save()
        self.state = ProjectState.TEST
        self.save(dbm)

    def delete(self, dbm):
        dbm.database.delete(self)

    #The method name sucks but until we make Project DataObject we can't make the method name 'void'
    def set_void(self, dbm, void = True):
        self.void = void
        self.save(dbm)

def get_project(pid, dbm):
    return dbm._load_document(pid, Project)


def get_all_projects(dbm, data_sender_id = None):
    if data_sender_id:
        return dbm.load_all_rows_in_view('projects_by_datasenders', startkey=data_sender_id, endkey=data_sender_id)
    return dbm.load_all_rows_in_view('all_projects')
