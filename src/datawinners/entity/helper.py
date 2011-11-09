# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import re
from mangrove.errors.MangroveException import NumberNotRegisteredException, DataObjectNotFound
from mangrove.transport.reporter import  find_reporter_entity
from django.utils.encoding import smart_unicode
from mangrove.utils.types import is_empty, is_not_empty
from mangrove.form_model.validation import NumericRangeConstraint, TextLengthConstraint
from mangrove.datastore.datadict import create_datadict_type, get_datadict_type_by_slug
from mangrove.form_model.field import TextField, IntegerField, SelectField, DateField, GeoCodeField
from mangrove.utils.helpers import slugify

def remove_hyphens(telephone_number):
    return re.sub('[- \(\)+]', '', smart_unicode(telephone_number))

def unique(dbm, telephone_number):
    telephone_number = remove_hyphens(telephone_number)
    try:
        find_reporter_entity(dbm, telephone_number)
    except NumberNotRegisteredException:
        return True
    return False

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

def update_questionnaire_with_questions(form_model, question_set, dbm):
    form_model.delete_all_fields()
    for question in question_set:
        form_model.add_field(create_question(question, dbm))
    return form_model

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
