# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from django.conf.urls.defaults import patterns
from datawinners.entity.views import create_datasender, disassociate_datasenders, associate_datasenders, create_web_users, create_entity_type
from datawinners.entity.views import create_subject
from datawinners.entity.views import create_type
from datawinners.entity.views import submit
from datawinners.entity.views import all_subjects
from datawinners.entity.views import all_datasenders
from datawinners.entity.views import import_subjects_from_project_wizard
from datawinners.entity.views import save_questionnaire
from datawinners.entity.views import edit_subject
from datawinners.entity.views import export_subject

urlpatterns = patterns('',
    (r'^entity/datasender/create', create_subject, {'entity_type': 'reporter'}),
    (r'^entity/datasender/create', create_datasender),
    (r'^entity/webuser/create', create_web_users),
    (r'^entity/subject/create/(?P<entity_type>.+?)/$', create_subject),
    (r'^entity/subject/create', create_subject),
    (r'^entity/subject/edit/(?P<entity_type>.+?)/$', edit_subject),
    (r'^entity/subject/edit/$', edit_subject),
    (r'^entity/subject/import/$', import_subjects_from_project_wizard),
    (r'^entity/subjects/$', all_subjects),
    (r'^entity/entity-type/create', create_entity_type),
    (r'^entity/type/create', create_type),
    (r'^entity/datasenders/$', all_datasenders),
    (r'^entity/disassociate/$', disassociate_datasenders),
    (r'^entity/associate/$', associate_datasenders),
    (r'^entity/subject/import/$', import_subjects_from_project_wizard),
    (r'^entity/questionnaire/save$', save_questionnaire),
    (r'^submit$', submit),
    (r'^entity/subject/edit/(?P<entity_type>.+?)/$', edit_subject),
    (r'^entity/subject/edit/$', edit_subject),
    (r'^entity/subject/export/', export_subject)
)