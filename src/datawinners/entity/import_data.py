# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import os
from datawinners import settings
from datawinners.main.utils import get_database_manager, is_reporter
from datawinners.entity.entity_exceptions import InvalidFileFormatException
from mangrove.datastore.entity import get_all_entities
from mangrove.errors.MangroveException import CSVParserInvalidHeaderFormatException, XlsParserInvalidHeaderFormatException
from mangrove.form_model.form_model import NAME_FIELD, MOBILE_NUMBER_FIELD, DESCRIPTION_FIELD
from mangrove.transport.player.parser import CsvParser, XlsParser
from mangrove.transport.player.player import FilePlayer, Channel
from mangrove.utils.types import sequence_to_str

def tabulate_failures(rows):
    tabulated_data = []
    for row in rows:
        errors = ''
        row[1].errors['row_num'] = row[0] + 2
        if type(row[1].errors['error']) is list:
            for error in row[1].errors['error']:
                errors = errors + ' ' + error
            row[1].errors['error'] = errors
        tabulated_data.append(row[1].errors)
    return tabulated_data


def _format(value):
    return value if value else "--"


def _tabulate_data(entity):
    id = entity.id
    geocode = entity.geometry.get('coordinates')
    geocode_string = ", ".join([str(i) for i in geocode]) if geocode is not None else "--"
    location = _format(sequence_to_str(entity.location_path))
    name = _format(entity.value(NAME_FIELD))
    mobile_number = _format(entity.value(MOBILE_NUMBER_FIELD))
    description = _format(entity.value(DESCRIPTION_FIELD))
    return dict(id=id, name=name, short_name=entity.short_code, type=".".join(entity.type_path), geocode=geocode_string,
                location=location,
                description=description, mobile_number=mobile_number)


def _get_entity_type_from_row(row):
    type = row['doc']['aggregation_paths']['_type']
    return type


def _is_not_reporter(entity):
    return not is_reporter(entity)


def load_subject_registration_data(manager, filter_entities=_is_not_reporter):
    entities = get_all_entities(dbm=manager, include_docs=True)
    data = []
    for entity in entities:
        if filter_entities(entity):
            data.append(_tabulate_data(entity))
    return data


def load_all_subjects(request):
    manager = get_database_manager(request.user)
    return load_subject_registration_data(manager)


def load_all_subjects_of_type(manager, filter_entities=is_reporter):
    return load_subject_registration_data(manager, filter_entities)


def _handle_uploaded_file(file_name, file, manager):
    base_name, extension = os.path.splitext(file_name)
    if extension == '.csv':
        csv_player = FilePlayer(manager, CsvParser(), Channel.CSV)
        response = csv_player.accept(file)
    elif extension == '.xls':
        xls_player = FilePlayer(manager, XlsParser(), Channel.XLS)
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
        file_name = request.GET.get('qqfile')
        responses = _handle_uploaded_file(file_name=file_name, file=request.raw_post_data, manager=manager)
        imported_entities = _get_imported_entities(responses)
        successful_imports = len(imported_entities)
        total = len(responses)
        failures = _get_failed_responses(responses)
        failure_imports = tabulate_failures(failures)
        response_message = '%s of %s records uploaded' % (successful_imports, total)
    except CSVParserInvalidHeaderFormatException or XlsParserInvalidHeaderFormatException as e:
        error_message = e.message
    except InvalidFileFormatException:
        error_message = 'We could not import your data ! \
                        You are using a document format we canʼt import. Please use a Comma Separated Values (.csv) or a Excel (.xls) file!'
    except Exception:
        error_message = 'Some unexpected error happened. Please check the CSV file and import again.'
        if settings.DEBUG:
            raise
    return error_message, failure_imports, response_message, imported_entities
