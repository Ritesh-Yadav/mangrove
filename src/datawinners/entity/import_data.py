# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import os
from django.conf import settings
from datawinners.location.LocationTree import get_location_tree
from datawinners.main.utils import get_database_manager, include_of_type, exclude_of_type
from datawinners.entity.entity_exceptions import InvalidFileFormatException
from mangrove.datastore.entity import get_all_entities
from mangrove.errors.MangroveException import CSVParserInvalidHeaderFormatException, XlsParserInvalidHeaderFormatException
from mangrove.form_model.form_model import REPORTER, REPORTER_FORM_CODE
from mangrove.transport.player.parser import CsvParser, XlsParser
from mangrove.transport.player.player import FilePlayer, Channel
from mangrove.utils.types import sequence_to_str
from django.utils.translation import ugettext as _, ugettext_lazy
from mangrove.datastore.entity_type import get_all_entity_types

def tabulate_failures(rows):
    tabulated_data = []
    for row in rows:
        row[1].errors['row_num'] = row[0] + 2

        if isinstance(row[1].errors['error'], dict):
            errors = ''
            for key,value in row[1].errors['error'].items():
                if key == 'n' or key == 't':
                    code = value.split(' ')[3]
                    errors = errors + _('Answer for question %s is required')% (code, )
                if key == 's':
                    errors = errors + value
                if key == 'g':
                    if 'xx.xxxx yy.yyyy' in value:
                        errors = errors + _('Incorrect GPS format. The GPS coordinates must be in the following format: xx.xxxx yy.yyyy. Example -18.8665 47.5315')
                    else:
                        text = value.split(' ')[2]
                        low = value.split(' ')[6]
                        high = value.split(' ')[8]
                        errors = errors + _("The answer %s must be between %s and %s") % (text, low, high)
                if key == 'm':
                    if 'is required' in value:
                        code = value.split(' ')[3]
                        errors = errors + _('Answer for question %s is required')% (code, )
                    if 'longer' in value:
                        text = value.split(' ')[1]
                        errors = errors + _("Answer %s for question %s is longer than allowed.") % (text, key)
                    else:
                        errors = errors + _(value)
        else:
            errors = _(row[1].errors['error'])

        row[1].errors['error'] = errors
        tabulated_data.append(row[1].errors)
    return tabulated_data


def _format(value):
    return value if value is not None else "--"


def _tabulate_data(entity, fields):
    data = {'id': entity.id, 'short_code': entity.short_code, 'cols': []}
    for i in range(len(fields)):
        if fields[i] in entity.data.keys():
            data['cols'].append(_get_field_value(fields[i], entity))
        else:
            data['cols'].append(_get_field_default_value(fields[i], entity))
    return data


def _get_entity_type_from_row(row):
    type = row['doc']['aggregation_paths']['_type']
    return type


def load_subject_registration_data(manager,
                                   filter_entities=exclude_of_type,
                                   type=REPORTER, form_code=REPORTER_FORM_CODE, tabulate_function=_tabulate_data):
    
    form_model = manager.load_all_rows_in_view("questionnaire", key=form_code)
    fields, labels = _get_field_infos(form_model[0].value['json_fields'])
    entities = get_all_entities(dbm=manager)
    data = []
    for entity in entities:
        if filter_entities(entity, type):
            data.append(tabulate_function(entity, fields))
    return data, fields, labels


def load_all_subjects_of_type(manager, filter_entities=include_of_type, type=REPORTER, form_code=REPORTER_FORM_CODE):
    return load_subject_registration_data(manager, filter_entities, type, form_code)


def _handle_uploaded_file(file_name, file, manager):
    base_name, extension = os.path.splitext(file_name)
    if extension == '.csv':
        csv_player = FilePlayer(manager, CsvParser(), Channel.CSV, get_location_tree())
        response = csv_player.accept(file)
    elif extension == '.xls':
        xls_player = FilePlayer(manager, XlsParser(), Channel.XLS, get_location_tree())
        response = xls_player.accept(file)
    else:
        raise InvalidFileFormatException()
    return response


def _get_imported_entities(responses):
    imported_entities = {response.short_code: response.entity_type[0] for response in responses if response.success}
    return imported_entities


def _get_failed_responses(responses):
    return [i for i in enumerate(responses) if not i[1].success]


def _get_success_status(successful_imports, total):
    return True if total == successful_imports else False


def import_data(request, manager):
    response_message = ''
    error_message = None
    failure_imports = None
    imported_entities = {}
    try:
        #IE sends the file in request.FILES['qqfile'] whereas all other browsers in request.GET['qqfile']. The following flow handles that flow.
        if 'qqfile' in request.GET:
            file_name = request.GET.get('qqfile')
            responses = _handle_uploaded_file(file_name=file_name, file=request.raw_post_data, manager=manager)
        else:
            file = request.FILES.get('qqfile')
            responses = _handle_uploaded_file(file_name=file.name, file=file.read(), manager=manager)

        imported_entities = _get_imported_entities(responses)
        successful_imports = len(imported_entities)
        total = len(responses)
        failures = _get_failed_responses(responses)
        failure_imports = tabulate_failures(failures)
        response_message = ugettext_lazy('%s of %s records uploaded') % (successful_imports, total)
    except CSVParserInvalidHeaderFormatException or XlsParserInvalidHeaderFormatException as e:
        error_message = e.message
    except InvalidFileFormatException:
        error_message = _(u"We could not import your data ! You are using a document format we canʼt import. Please use a Comma Separated Values (.csv) or a Excel (.xls) file!")
    except Exception:
        error_message = 'Some unexpected error happened. Please check the CSV file and import again.'
        if settings.DEBUG:
            raise
    return error_message, failure_imports, response_message, imported_entities

def _get_entity_types(manager):
    entity_types = get_all_entity_types(manager)
    entity_list = [entity[0] for entity in entity_types if entity[0] != 'reporter']
    entity_list.sort()
    return entity_list

def _get_registration_form_models(manager):
    subjects = {}
    form_models = manager.load_all_rows_in_view('questionnaire')
    for form_model in form_models:
        if form_model.value['flag_reg'] and form_model.value['name'] != 'Reporter':
            subjects[form_model.value['entity_type'][0]] = form_model
    return subjects


def _get_field_infos(fields):
    names = []
    labels = []
    for field in fields:
        names.append(field['name'])
        labels.append(field['label']['en'])
    return names, labels


def _get_entity_type_infos(entity, form_model):
    names, labels = _get_field_infos(form_model.value['json_fields'])

    subject = dict(entity = entity,
        code = form_model.value["form_code"],
        names = names,
        labels = labels,
        data = [],
    )
    return subject

def _get_field_value(key, entity):
    value = entity.value(key)
    if key == 'geo_code':
        if value is None:
            value = entity.geometry.get('coordinates')
            value = ", ".join([str(i) for i in value]) if value is not None else "--"
        else:
            value = ", ".join([str(i) for i in value])
    elif key == 'location':
        if value is None:
            value = _format(sequence_to_str(entity.location_path, u", ")) if value is not None else "--"
        else:
            value = _format(sequence_to_str(value, u", "))
    elif key == 'entity_type':
        value = _format(sequence_to_str(value, u", "))
    else:
        value = _format(value)
    return value

def _get_field_default_value(key, entity):
    if key == 'geo_code':
        value = entity.geometry.get('coordinates')
        value = ", ".join([str(i) for i in value]) if value is not None else "--"
    elif key == 'location':
        value = sequence_to_str(entity.location_path, u", ")
        value = _format(value) if value is not None else "--"
    elif key == 'short_code':
        value = entity.short_code
    else:
        value = "--"
    return value

def load_all_subjects(request):
    manager = get_database_manager(request.user)
    entity_types_names = _get_entity_types(manager)
    subjects = _get_registration_form_models(manager)

    subjects_list = {}
    for entity in entity_types_names:
        if entity in subjects.keys():
            form_model = subjects[entity]
        else:
            form_model = subjects['Registration']
        subjects_list[entity] = _get_entity_type_infos(entity, form_model)

    entities = get_all_entities(dbm=manager)
    for entity in entities:
        if exclude_of_type(entity, REPORTER):
            entity_type = entity.type_string
            if entity_type in subjects_list.keys():
                subjects_list[entity_type]['data'].append(_tabulate_data(entity, subjects_list[entity_type]['names']))

    data = [subjects_list[entity] for entity in entity_types_names]
    return data