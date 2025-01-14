# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import logging
from django.utils.translation import ugettext
from datawinners.entity.import_data import load_all_subjects_of_type
from datawinners.scheduler.smsclient import SMSClient
from mangrove.datastore.datadict import create_datadict_type, get_datadict_type_by_slug
from mangrove.datastore.documents import attributes
from mangrove.errors.MangroveException import DataObjectNotFound, FormModelDoesNotExistsException
from mangrove.form_model.field import TextField, IntegerField, SelectField, DateField, GeoCodeField
from mangrove.form_model.form_model import FormModel, get_form_model_by_code, REPORTER
from mangrove.form_model.validation import NumericRangeConstraint, TextLengthConstraint
from mangrove.utils.helpers import slugify
from mangrove.utils.types import is_empty, is_sequence, is_not_empty, is_string, sequence_to_str
from mangrove.datastore import aggregrate as aggregate_module
import models
import xlwt
from datetime import datetime
from mangrove.transport.submissions import  Submission, get_submissions
from models import Reminder

NUMBER_TYPE_OPTIONS = ["Latest", "Sum", "Count", "Min", "Max", "Average"]
MULTI_CHOICE_TYPE_OPTIONS = ["Latest"]
DATE_TYPE_OPTIONS = ["Latest"]
GEO_TYPE_OPTIONS = ["Latest"]
TEXT_TYPE_OPTIONS = ["Latest"]
TEST_FLAG = 'TEST'
logger = logging.getLogger("datawinners.reminders")

def get_or_create_data_dict(dbm, name, slug, primitive_type, description=None):
    try:
        #  Check if is existing
        ddtype = get_datadict_type_by_slug(dbm, slug)
    except DataObjectNotFound:
        #  Create new one
        ddtype = create_datadict_type(dbm=dbm, name=name, slug=slug,
                                      primitive_type=primitive_type, description=description)
    return ddtype


def create_question(post_dict, dbm):
    options = post_dict.get('options')
    datadict_type = options.get('ddtype') if options is not None else None
    if is_not_empty(datadict_type):
        #  question already has a data dict type
        datadict_slug = datadict_type.get('slug')
    else:
        datadict_slug = str(slugify(unicode(post_dict.get('title'))))
    ddtype = get_or_create_data_dict(dbm=dbm, name=post_dict.get('code'), slug=datadict_slug,
                                     primitive_type=post_dict.get('type'), description=post_dict.get('title'))

    if post_dict["type"] == "text":
        return _create_text_question(post_dict, ddtype)
    if post_dict["type"] == "integer":
        return _create_integer_question(post_dict, ddtype)
    if post_dict["type"] == "geocode":
        return _create_geo_code_question(post_dict, ddtype)
    if post_dict["type"] == "select":
        return _create_select_question(post_dict, single_select_flag=False, ddtype=ddtype)
    if post_dict["type"] == "date":
        return _create_date_question(post_dict, ddtype)
    if post_dict["type"] == "select1":
        return _create_select_question(post_dict, single_select_flag=True, ddtype=ddtype)


def _create_entity_id_question(dbm, entity_id_question_code):
    entity_data_dict_type = get_or_create_data_dict(dbm=dbm, name="eid", slug="entity_id", primitive_type="string",
                                                    description="Entity ID")
    name = ugettext("Which subject are you reporting on?")
    entity_id_question = TextField(name=name, code=entity_id_question_code,
                                   label="Entity being reported on",
                                   entity_question_flag=True, ddtype=entity_data_dict_type,
                                   constraints=[TextLengthConstraint(min=1, max=12)],
                                   instruction=(ugettext('Answer must be a word or phrase %d characters maximum') % 12))
    return entity_id_question


def _create_questionnaire(dbm, post,entity_type,entity_id_question_code, activity_report_question_code):
    entity_id_question = _create_entity_id_question(dbm, entity_id_question_code)

    reporting_period_dict_type = get_or_create_data_dict(dbm=dbm, name="rpd", slug="reporting_period",
                                                         primitive_type="date",
                                                         description="activity reporting period")
    activity_report_question = DateField(name=ugettext("What is the reporting period for the activity?"), code=activity_report_question_code,
                                         label="Period being reported on", ddtype=reporting_period_dict_type,
                                         date_format="dd.mm.yyyy", event_time_field_flag=True)

    fields = [entity_id_question, activity_report_question]
    return FormModel(dbm, entity_type=entity_type, name=post["name"], fields=fields,
                     form_code=generate_questionnaire_code(dbm), type='survey', state=attributes.INACTIVE_STATE,
                     language=post['language'])


def _create_activity_report_questionnaire(dbm, post, entity_type):
    return _create_questionnaire(dbm,post,entity_type,'eid','q1')

def _create_subject_questionnaire(dbm, post, entity_type):
    return _create_questionnaire(dbm,post,entity_type,'q1','q2')


def create_questionnaire(post, dbm):
    entity_type = [post["entity_type"]] if is_string(post["entity_type"]) else post["entity_type"]
    if entity_type == [REPORTER]:
        return _create_activity_report_questionnaire(dbm,post,entity_type)
    return _create_subject_questionnaire(dbm, post, entity_type)


def _create_entity_id_question_for_activity_report(dbm):
    entity_data_dict_type = get_or_create_data_dict(dbm=dbm, name="eid", slug="entity_id", primitive_type="string",
                                                    description="Entity ID")
    name = ugettext("I am submitting this data on behalf of")
    entity_id_question = TextField(name=name, code='eid',
                                   label="Entity being reported on",
                                   entity_question_flag=True, ddtype=entity_data_dict_type,
                                   constraints=[TextLengthConstraint(min=1, max=12)],
                                   instruction= ugettext("Enter the ID number of the Data Sender. Click on 'Data Senders' at the top of this page to find these ID numbers. Example: rep10"))
    return entity_id_question



def update_questionnaire_with_questions(form_model, question_set, dbm):
    form_model.delete_all_fields()

    if form_model.entity_defaults_to_reporter():
        form_model.add_field(_create_entity_id_question_for_activity_report(dbm))

    for question in question_set:
        form_model.add_field(create_question(question, dbm))
    return form_model


def hide_entity_question(fields):
    return [each for each in fields if not each.is_entity_field]

def _create_text_question(post_dict, ddtype):
    max_length_from_post = post_dict.get("max_length")
    min_length_from_post = post_dict.get("min_length")
    max_length = max_length_from_post if not is_empty(max_length_from_post) else None
    min_length = min_length_from_post if not is_empty(min_length_from_post) else None
    constraints = []
    if not (max_length is None and min_length is None):
        constraints.append(TextLengthConstraint(min=min_length, max=max_length))
    return TextField(name=post_dict["title"], code=post_dict["code"].strip(), label="default",
                     entity_question_flag=post_dict.get("is_entity_question"), constraints=constraints, ddtype=ddtype,
                     instruction=post_dict.get("instruction"),required=post_dict.get("required"))


def _create_integer_question(post_dict, ddtype):
    max_range_from_post = post_dict.get("range_max")
    min_range_from_post = post_dict.get("range_min")
    max_range = max_range_from_post if not is_empty(max_range_from_post) else None
    min_range = min_range_from_post if not is_empty(min_range_from_post) else None
    range = NumericRangeConstraint(min=min_range, max=max_range)
    return IntegerField(name=post_dict["title"], code=post_dict["code"].strip(), label="default",
                        constraints=[range], ddtype=ddtype, instruction=post_dict.get("instruction"),required=post_dict.get("required"))


def _create_date_question(post_dict, ddtype):
    return DateField(name=post_dict["title"], code=post_dict["code"].strip(), label="default",
                     date_format=post_dict.get('date_format'), ddtype=ddtype, instruction=post_dict.get("instruction"),required=post_dict.get("required"), event_time_field_flag=post_dict.get('event_time_field_flag', False))


def _create_geo_code_question(post_dict, ddtype):
    return GeoCodeField(name=post_dict["title"], code=post_dict["code"].strip(), label="default", ddtype=ddtype,
                        instruction=post_dict.get("instruction"),required=post_dict.get("required"))


def _create_select_question(post_dict, single_select_flag, ddtype):
    options = [(choice.get("text"), choice.get("val")) for choice in post_dict["choices"]]
    return SelectField(name=post_dict["title"], code=post_dict["code"].strip(), label="default",
                       options=options, single_select_flag=single_select_flag, ddtype=ddtype,
                       instruction=post_dict.get("instruction"),required=post_dict.get("required"))

def adapt_submissions_for_template(questions, submissions):
    assert is_sequence(questions)
    assert is_sequence(submissions)
    for s in submissions:
        assert type(s) is Submission and s._doc is not None
    formatted_list = []
    for each in submissions:
        case_insensitive_dict = {key.lower():value for key,value in each.values.items()}
        formatted_list.append(
            [each.uuid, each.destination, each.source, each.created, each.errors, each.status]+
            [each.data_record.is_void() if each.data_record is not None else True] + [case_insensitive_dict.get(q.code.lower(), '--') for q in questions])

    return [tuple(each) for each in formatted_list]


def generate_questionnaire_code(dbm):
    all_projects_count = models.count_projects(dbm)
    code = all_projects_count + 1
    code = "%03d" % (code,)
    while True:
        try:
            get_form_model_by_code(dbm, code)
            code = int(code) + 1
            code = "%03d" % (code,)
        except FormModelDoesNotExistsException:
            break
    return code


def get_aggregation_options_for_all_fields(fields):
    type_dictionary = dict(IntegerField=NUMBER_TYPE_OPTIONS, TextField=TEXT_TYPE_OPTIONS, DateField=DATE_TYPE_OPTIONS,
                           GeoCodeField=GEO_TYPE_OPTIONS, SelectField=MULTI_CHOICE_TYPE_OPTIONS)
    type_list = []
    for field in fields:
        field_type = field.__class__.__name__
        #TODO- Future functionality. Removing for beta-release. Uncomment this when aggregations for multiple choice field are added.
        #        if field_type == "SelectField":
        #            choice_type = copy(MULTI_CHOICE_TYPE_OPTIONS)
        #            choice_type.extend(["sum(" + choice.get("text").get(field.language) + ")"for choice in
        #                                field.options])
        #            choice_type.extend(["percent(" + choice.get("text").get(field.language) + ")" for choice in
        #                                field.options])
        #            type_list.append(choice_type)
        #        else:
        type_list.append(type_dictionary.get(field_type))
    return type_list


def get_headers(form_model):
    return [form_model.entity_type[0] + " Code"] + [field.name for field in form_model.fields[1:]]


def _to_str(value):
    if value is None:
        return u"--"
    if is_sequence(value):
        return sequence_to_str(value)
    return value


def _to_value_list(first_element, header_list, value_dict):
    return [first_element] + [_to_str(value_dict.get(header)) for header in header_list[1:]]


def get_all_values(data_dictionary, header_list, entity_question_description):
    """
       data_dictionary = {'Clinic/cid002': {'What is age of father?': 55, 'What is your name?': 'shweta', 'What is associated entity?': 'cid002'}, 'Clinic/cid001': {'What is age of father?': 35, 'What is your name?': 'asif', 'What is associated entity?': 'cid001'}}
       header_list = ["What is associated entity", "What is your name", "What is age of father?"]
       expected_list = [ ['cid002',''shweta', 55 ],['cid001','asif', 35]]
    """
    grand_totals_dict = data_dictionary.pop('GrandTotals') if 'GrandTotals' in data_dictionary else {}
    grand_totals = _to_value_list("Grand Total", header_list, grand_totals_dict)
    return [_to_value_list(value_dict.get(entity_question_description), header_list, value_dict) for value_dict in data_dictionary.values()], grand_totals


def get_aggregate_dictionary(header_list, post_data):
    aggregates = {}
    #    my_dictionary =
    for index, key in enumerate(header_list):
        aggregates[key] = post_data[index].strip().lower()
    return aggregates


def get_aggregate_list(fields, post_data):
    aggregates = []
    for index, field in enumerate(fields):
        aggregates.append(aggregate_module.aggregation_factory(post_data[index].strip().lower(), field.name))
    return aggregates


def get_formatted_time_string(time_val):
    try:
        time_val = datetime.strptime(time_val, '%d-%m-%Y %H:%M:%S')
    except Exception:
        return None
    return time_val.strftime('%d-%m-%Y %H:%M:%S')


def get_excel_sheet(raw_data, sheet_name):
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheet_name)
    for row_number, row  in enumerate(raw_data):
        for col_number, val in enumerate(row):
            ws.write(row_number, col_number, val)
    return wb


def remove_reporter(entity_type_list):
    removable = None
    for each in entity_type_list:
        if each[0].lower() == 'reporter':
            removable = each
    entity_type_list.remove(removable)
    entity_type_list.sort()
    return entity_type_list


def get_preview_for_field(field):
    return {"description": field.name, "code": field.code, "type": field.type,
            "constraints": field.get_constraint_text(), "instruction": field.instruction}


def _add_to_dict(dict, post_dict,key):
    if post_dict.get(key):
        dict[key] = post_dict.get(key)

def get_project_data_senders(manager, project):
    all_data = load_all_subjects_of_type(manager)
    return [data for data in all_data if data['short_name'] in project.data_senders]

def delete_project(manager, project, void = True):
    project_id, qid = project.id, project.qid
    [reminder.void(void) for reminder in (Reminder.objects.filter(project_id=project_id))]
    questionnaire = FormModel.get(manager, qid)
    [submission.void(void) for submission in get_submissions(manager, questionnaire.form_code, None, None)]
    questionnaire.void(void)
    project.set_void(manager, void)

def get_activity_report_questions(dbm):
    reporting_period_dict_type = get_or_create_data_dict(dbm=dbm, name="rpd", slug="reporting_period",
                                                         primitive_type="date",
                                                         description="activity reporting period")
    activity_report_question = DateField(name=ugettext("What is the reporting period for the activity?"), code='q1',
                                         label="Period being reported on", ddtype=reporting_period_dict_type,
                                         date_format="dd.mm.yyyy", event_time_field_flag=True)

    return [activity_report_question]

def get_subject_report_questions(dbm):
    entity_id_question = _create_entity_id_question(dbm, 'q1')
    reporting_period_dict_type = get_or_create_data_dict(dbm=dbm, name="rpd", slug="reporting_period",
                                                         primitive_type="date",
                                                         description="activity reporting period")
    activity_report_question = DateField(name=ugettext("What is the reporting period for the activity?"), code='q2',
                                         label="Period being reported on", ddtype=reporting_period_dict_type,
                                         date_format="dd.mm.yyyy", event_time_field_flag=True)
    return [entity_id_question, activity_report_question]


def broadcast_message(data_senders, message, organization_tel_number, other_numbers, message_tracker):
    sms_client = SMSClient()
    for data_sender in data_senders:
        phone_number = data_sender.get('mobile_number') #This should not be a dictionary but the API in import_data should be fixed to return entity
        if phone_number is not None:
            logger.info(("Sending broadcast message to %s from %s") % (phone_number, organization_tel_number))
            message_tracker.increment_outgoing_message_count()
            sms_client.send_sms(organization_tel_number, phone_number, message)

    for number in other_numbers:
        number = number.strip()
        logger.info(("Sending broadcast message to %s from %s") % (number, organization_tel_number))
        message_tracker.increment_outgoing_message_count()
        sms_client.send_sms(organization_tel_number, number, message)