# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from datastore.database import get_db_manager
from datastore.documents import SubmissionLogDocument
from datastore.entity import Entity
import entity
from utils import is_sequence, utcnow


def register(entity_type, data, location, source, aggregation_paths = None):

    manager = get_db_manager()
    e = Entity(manager, entity_type= entity_type, location= location, aggregation_paths = aggregation_paths)
    saved_entity_id = e.save()
    submit(entity_id=saved_entity_id, data=data, source=source)
    return e

def submit(entity_id,data,source):
    assert entity_id is not None
    assert is_sequence(data) and len(data) > 0

    # create and persist a submission doc.
    # source will have channel info ie. Web/SMS etc,,
    # source will also have the reporter info.

    manager = get_db_manager()
    e = entity.get(manager,entity_id)
    submission_log = SubmissionLogDocument(source = source)
    submission_log = manager.save(submission_log)
    data_record_id = e.add_data(data=data, event_time=utcnow(), submission_id=submission_log.id)
    return data_record_id, submission_log.id


