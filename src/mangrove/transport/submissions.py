# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from mangrove.datastore.database import DatabaseManager
from mangrove.datastore.documents import SubmissionLogDocument
from mangrove.form_model.form_model import get_form_model_by_code
from mangrove.errors.MangroveException import  NoQuestionsSubmittedException, InactiveFormModelException
from mangrove.utils.types import is_string, sequence_to_str
from mangrove.transport import reporter

ENTITY_QUESTION_DISPLAY_CODE = "eid"

class SubmissionRequest(object):
    def __init__(self, form_code, submission, transport, source, destination):
        assert form_code is not None
        assert submission is not None
        assert transport is not None
        assert source is not None
        assert destination is not None

        self.form_code = form_code
        self.submission = submission
        self.transport = transport
        self.source = source
        self.destination = destination


class SubmissionResponse(object):
    def __init__(self, success, submission_id, errors=None, datarecord_id=None, short_code=None, processed_data=None):
        assert success is not None
        assert submission_id is not None

        self.success = success
        self.submission_id = submission_id
        self.errors = {} if errors is None else errors
        self.datarecord_id = datarecord_id
        self.short_code = short_code
        self.processed_data = processed_data


class SubmissionHandler(object):
    def __init__(self, dbm):
        assert isinstance(dbm, DatabaseManager)
        self.dbm = dbm
        self.logger = SubmissionLogger(self.dbm)


    def save_data(self, entity, form_submission, form):
        submission_information = dict(form_code=form.form_code)
        data_record_id = entity.add_data(data=form_submission.values, submission=submission_information)
        return data_record_id

    def _should_accept_submission(self, form):
        return form.is_inactive()

    def _reject_submission_for_inactive_forms(self, form):
        if self._should_accept_submission(form):
            raise InactiveFormModelException(form.form_code)

    def accept(self, request):
        assert isinstance(request, SubmissionRequest)
        form_code = request.form_code
        values = request.submission

        submission_id = self.logger.create_submission_log(request)

        form = get_form_model_by_code(self.dbm, form_code)

        if form.entity_defaults_to_reporter():
            short_code = reporter.get_short_code_from_reporter_number(self.dbm, request.source)
            values[ENTITY_QUESTION_DISPLAY_CODE] = short_code

        try:
            cleaned_data, data_record_id, short_code, status, errors = self.submit(form, values)
        except InactiveFormModelException:
            self.logger.update_submission_log(submission_id, False, 'Inactive form_model')
            raise

        self.logger.update_submission_log(submission_id=submission_id, data_record_id=data_record_id,
                                          status=status, errors=errors, in_test_mode=form.is_in_test_mode())

        return SubmissionResponse(status, submission_id, errors, data_record_id, short_code=short_code,
                                  processed_data=cleaned_data)

    def get_entity(self, form, form_submission):
        should_create_entity = form.is_registration_form()
        e = form_submission.to_entity(self.dbm, create=should_create_entity)
        return e

    def submit(self, form, values):
        self._reject_submission_for_inactive_forms(form)

        form_submission = form.validate_submission(values)

        data_record_id = None
        _errors = None
        status = False

        if form_submission.is_valid:
            if len(form_submission.values) == 1:
                raise NoQuestionsSubmittedException()
            entity = self.get_entity(form, form_submission)
            data_record_id = self.save_data(entity, form_submission, form)
            status = True
        else:
            _errors = form_submission.errors

        return form_submission.cleaned_data, data_record_id, form_submission.short_code, status, _errors


class SubmissionLogger(object):
    def __init__(self, dbm):
        assert isinstance(dbm, DatabaseManager)
        self.dbm = dbm

    def void_data_record(self, submission_id):
        submission_log = self.dbm._load_document(submission_id, SubmissionLogDocument)
        submission_log.data_record_id = None
        submission_log.voided = True
        self.dbm._save_document(submission_log)

    def _to_string(self, errors):
        if is_string(errors):
            return errors
        if isinstance(errors, dict):
            return sequence_to_str(errors.values())
        return sequence_to_str(errors)

    def update_submission_log(self, submission_id, status, errors, data_record_id=None, in_test_mode=False):
        log = self.dbm._load_document(submission_id, SubmissionLogDocument)
        log.status = status
        log.voided = not status
        log.data_record_id = data_record_id
        log.error_message += self._to_string(errors)
        log.test = in_test_mode
        self.dbm._save_document(log)

    def create_submission_log(self, request):
        return self.dbm._save_document(SubmissionLogDocument(channel=request.transport, source=request.source,
                                                             destination=request.destination,
                                                             form_code=request.form_code,
                                                             values=request.submission, status=False,
                                                             error_message="", voided=True, test=False))


def _get_row_count(rows):
    if rows is None:
        return None
    result = rows[0].value
    return result.get('count') if result else None


def get_submission_count_for_form(dbm, form_code, start_time, end_time):
    assert is_string(form_code)
    rows = dbm.load_all_rows_in_view('submissionlog', startkey=[form_code, start_time], endkey=[form_code, end_time,
            {}]
                                     ,
                                     group=True, group_level=1, reduce=True)
    count = _get_row_count(rows) if rows else 0
    return count


def get_submissions_made_for_form(dbm, form_code, start_time, end_time, page_number=0, page_size=20):
    assert is_string(form_code)
    if page_size is None:
        rows = dbm.load_all_rows_in_view('submissionlog', reduce=False, descending=True,
                                         startkey=[form_code, end_time, {}],
                                         endkey=[form_code, start_time])
    else:
        rows = dbm.load_all_rows_in_view('submissionlog', reduce=False, descending=True,
                                         startkey=[form_code, end_time, {}],
                                         endkey=[form_code, start_time], skip=page_number * page_size, limit=page_size)
    answers, ids = list(), list()
    for each in rows:
        answers.append(each.value)
        ids.append(each.value["data_record_id"])
    return answers, ids
