# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from collections import defaultdict
import json
from django.forms.forms import Form
from django import forms
from mangrove.form_model.field import SelectField, field_to_json
from django.forms.widgets import HiddenInput
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_view_exempt, csrf_response_exempt
from django.views.decorators.http import require_http_methods
from django.utils.translation import ugettext as _
from datawinners.accountmanagement.models import NGOUserProfile, DataSenderOnTrialAccount,Organization
from datawinners.accountmanagement.views import is_datasender, is_new_user
from datawinners.entity import helper
from datawinners.location.LocationTree import get_location_tree
from datawinners.main.utils import get_database_manager
from datawinners.messageprovider.message_handler import get_success_msg_for_registration_using, get_submission_error_message_for, get_exception_message_for
from datawinners.project.models import Project
from mangrove.datastore.entity_type import define_type, get_all_entity_types
from datawinners.project import helper as project_helper, models
from mangrove.errors.MangroveException import EntityTypeAlreadyDefined, MangroveException, DataObjectAlreadyExists, QuestionCodeAlreadyExistsException, EntityQuestionAlreadyExistsException, DataObjectNotFound
from datawinners.entity.forms import EntityTypeForm, ReporterRegistrationForm, SubjectForm
from mangrove.form_model.form_model import get_form_model_by_code, REGISTRATION_FORM_CODE, MOBILE_NUMBER_FIELD_CODE, GEO_CODE, NAME_FIELD_CODE, LOCATION_TYPE_FIELD_CODE, ENTITY_TYPE_FIELD_CODE, REPORTER, create_reg_form_model, get_form_model_by_entity_type
from datawinners.entity import import_data as import_module
from mangrove.utils.types import is_empty, sequence_to_str
from datawinners.entity.helper import update_questionnaire_with_questions
from mangrove.transport.player import player
from mangrove.transport.player.player import WebPlayer, Request, TransportInfo
from datawinners.utils import get_excel_sheet
import logging

logger = logging.getLogger("django")

COUNTRY = ',MADAGASCAR'

def _associate_data_sender_to_project(dbm, project_id, response):
    project = Project.load(dbm.database, project_id)
    project.data_senders.append(response.short_code)
    project.save(dbm)


def _add_data_sender_to_trial_organization(telephone_number, org_id):
    data_sender = DataSenderOnTrialAccount.objects.model(mobile_number=telephone_number,
                                                         organization=Organization.objects.get(org_id=org_id))
    data_sender.save()


def _process_form(dbm, form, org_id):
    message = None
    if form.is_valid():
        telephone_number = form.cleaned_data["telephone_number"]
        if not helper.unique(dbm, telephone_number):
            form._errors['telephone_number'] = form.error_class([(u"Sorry, the telephone number %s has already been registered") % (telephone_number,)])
            return message

        organization = Organization.objects.get(org_id=org_id)
        if organization.in_trial_mode:
            if DataSenderOnTrialAccount.objects.filter(mobile_number=telephone_number).exists():
                form._errors['telephone_number'] = form.error_class([(u"Sorry, this number has already been used for a different DataWinners trial account.")])
                return message
            else:
                _add_data_sender_to_trial_organization(telephone_number,org_id)


        try:
            web_player = WebPlayer(dbm, get_location_tree())
            response = web_player.accept(Request(message=_get_data(form.cleaned_data),
                                                 transportInfo=TransportInfo(transport='web', source='web', destination='mangrove')))
            message = get_success_msg_for_registration_using(response, "web")
            project_id = form.cleaned_data["project_id"]
            if not is_empty(project_id):
                _associate_data_sender_to_project(dbm, project_id, response)
        except MangroveException as exception:
            message = exception.message

    return message


def _get_data(form_data):
    #TODO need to refactor this code. The master dictionary should be maintained by the registration form model
    mapper = {'telephone_number': MOBILE_NUMBER_FIELD_CODE, 'geo_code': GEO_CODE, 'Name': NAME_FIELD_CODE,
              'location': LOCATION_TYPE_FIELD_CODE}
    data = dict()
    data[mapper['telephone_number']] = form_data.get('telephone_number')
    data[mapper['location']] = form_data.get('location') + COUNTRY if form_data.get('location') is not None else None
    data[mapper['geo_code']] = form_data.get('geo_code')
    data[mapper['Name']] = form_data.get('first_name')
    data['form_code'] = REGISTRATION_FORM_CODE
    data[ENTITY_TYPE_FIELD_CODE] = 'Reporter'
    return data

#TODO This method has to be moved into a proper place since this is used for registering entities.
@csrf_view_exempt
@csrf_response_exempt
@require_http_methods(['POST'])
@login_required(login_url='/login')
def submit(request):
    dbm = get_database_manager(request.user)
    post = json.loads(request.POST['data'])
    success = True
    try:
        web_player = WebPlayer(dbm, get_location_tree())
        message = post['message']
        if message.get(LOCATION_TYPE_FIELD_CODE) is not None:
            message[LOCATION_TYPE_FIELD_CODE] += COUNTRY
        request = Request(message=message,
                          transportInfo=TransportInfo(transport=post.get('transport'), source=post.get('source'),
                                                      destination=post.get('destination')))
        response = web_player.accept(request)
        if response.success:
            message = get_success_msg_for_registration_using(response, "web")
        else:
            message = get_submission_error_message_for(response.errors)
        entity_id = response.datarecord_id
    except DataObjectAlreadyExists as exception:
        message = _("Entity with Unique Identification Number (ID) = %s already exists.") % exception.data[1]
        success, entity_id = False, None
    except MangroveException as exception:
        message = get_exception_message_for(exception=exception, channel="web")
        message = _("Please add subject type and then add a subject") if message == "t should be present" else message
        success = False
        entity_id = None
    return HttpResponse(json.dumps({'success': success, 'message': message, 'entity_id': entity_id}))

@login_required(login_url='/login')
def save_questionnaire(request):
    manager = get_database_manager(request.user)
    if request.method == 'POST':
        questionnaire_code = request.POST['saved-questionnaire-code']
        if questionnaire_code == "":
            form_model = _create_new_reg_form_model(manager, request.POST["entity-type"])
            questionnaire_code = form_model.form_code
        else:
            form_model = get_form_model_by_code(manager, questionnaire_code)
        json_string = request.POST['question-set']
        question_set = json.loads(json_string)
        try:
            form_model = update_questionnaire_with_questions(form_model, question_set, manager)
        except QuestionCodeAlreadyExistsException as e:
            return HttpResponseServerError(e)
        except EntityQuestionAlreadyExistsException as e:
            return HttpResponseServerError(e.message)
        else:
            try:
                form_model.form_code = questionnaire_code.lower()
            except DataObjectAlreadyExists as e:
                if e.message.find("Form") >= 0:
                    return HttpResponseServerError("Questionnaire with this code already exists")
                return HttpResponseServerError(e.message)
            if request.POST['questionnaire-code'] != 'reg':
                form_model.form_code = request.POST['questionnaire-code'].lower()
            form_model.save()
            return HttpResponse(json.dumps({"response": "ok", 'form_code': form_model.form_code}))

@login_required(login_url='/login')
def create_datasender(request):
    if request.method == 'GET':
        form = ReporterRegistrationForm()
        return render_to_response('entity/create_datasender.html', {'form': form},
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        dbm = get_database_manager(request.user)
        form = ReporterRegistrationForm(request.POST)
        org_id = request.user.get_profile().org_id
        message= _process_form(dbm, form, org_id)
        if message is not None:
            form = ReporterRegistrationForm(initial={'project_id':form.cleaned_data['project_id']})
        return render_to_response('datasender_form.html',
                {'form': form, 'message': message},
                                      context_instance=RequestContext(request))


@login_required(login_url='/login')
def create_type(request):
    success = False
    form = EntityTypeForm(request.POST)
    if form.is_valid():
        entity_name = form.cleaned_data["entity_type_regex"]
        entity_name = [entity_name.lower()]
        try:
            manager = get_database_manager(request.user)
            define_type(manager, entity_name)
            message = _("Entity definition successful")
            success = True
        except EntityTypeAlreadyDefined:
            message = _("%s already registered as a subject type. Please select %s from the drop down menu.") % (entity_name[0], entity_name[0])
    else:
        message = form.fields['entity_type_regex'].error_messages['invalid']
    return HttpResponse(json.dumps({'success': success, 'message': _(message)}))

def _get_entity_types(manager):
    entity_types = get_all_entity_types(manager)
    entity_list = [entity[0] for entity in entity_types if entity[0] != 'reporter']
    entity_list.sort()
    return entity_list


def _get_entity_types_with_form(manager):
    form_models = manager.load_all_rows_in_view("questionnaire")
    entity_list = []
    for form_model in form_models:
        entity = form_model.value['entity_type'][0]
        if form_model.value['flag_reg'] and entity != 'reporter':
            entity_list.append(entity)

    entity_list.sort()
    return entity_list


def _get_entity_types_without_form(manager):
    entity_types = _get_entity_types(manager)
    entity_types = set(entity_types)
    entity_with_form = _get_entity_types_with_form(manager)
    entity_with_form = set(entity_with_form)
    entity_without_form = set.difference(entity_types, entity_with_form)
    entity_without_form = list(entity_without_form)

    entity_without_form.sort()
    return entity_without_form

@csrf_view_exempt
@csrf_response_exempt
@login_required(login_url='/login')
@is_new_user
@is_datasender
def all_subjects(request):
    manager = get_database_manager(request.user)
    all_data = import_module.load_all_subjects(request)

    if request.method == 'POST':
        error_message, failure_imports, success_message, imported_entities = import_module.import_data(request, manager)
        return HttpResponse(json.dumps({'success': error_message is None and is_empty(failure_imports), 'message': success_message, 'error_message': error_message,
                                        'failure_imports': failure_imports, 'all_data': all_data}))

    return render_to_response('entity/all_subjects.html', {'all_data': all_data, 'current_language': translation.get_language()},
                                  context_instance=RequestContext(request))


def _get_project_association(projects):
    project_association = defaultdict(list)
    for project in projects:
        for datasender in project['value']['data_senders']:
            project_association[datasender].append(project['value']['name'])
    return project_association


def _get_all_datasenders(manager, projects, user):
    all_data_senders = import_module.load_all_subjects_of_type(manager)
    project_association = _get_project_association(projects)
    for datasender in all_data_senders:
        org_id = NGOUserProfile.objects.get(user=user).org_id
        user_profile = NGOUserProfile.objects.filter(reporter_id=datasender['short_name'], org_id = org_id)
        datasender['email'] = user_profile[0].user.email if len(user_profile) > 0 else "--"
        association = project_association.get(datasender['short_name'])
        datasender['projects'] = ' ,'.join(association) if association is not None else '--'
    return all_data_senders

@login_required(login_url='/login')
@csrf_view_exempt
def create_web_users(request):
    org_id = request.user.get_profile().org_id
    if request.method == 'POST':
        errors = []
        post_data = json.loads(request.POST['post_data'])
        for data in post_data:
            users = User.objects.filter(email=data['email'])
            if len(users) > 0:
                errors.append("User with email %s already exists" % data['email'])
        if len(errors) > 0:
            return HttpResponse(json.dumps({'success':False, 'errors': errors}))

        for data in post_data:
            user = User.objects.create_user(data['email'], data['email'], 'test123')
            user.first_name = user.email
            group = Group.objects.filter(name="Data Senders")[0]
            user.groups.add(group)
            user.save()
            profile = NGOUserProfile(user=user, org_id=org_id, title="Mr", reporter_id=data['reporter_id'])
            profile.save()
            reset_form = PasswordResetForm({"email": user.email})
            reset_form.is_valid()
            reset_form.save()

        return HttpResponse(json.dumps({'success':True, 'message':"Users has been created"}))


def _get_field_code(fields):
    codes = []
    for field in fields:
        if field['name'] == 'short_code':
            field_name = 'short_name'
        elif field['name'] == 'geo_code':
            field_name = 'geocode'
        elif field['name'] == 'entity_type':
            field_name = 'type'
        else:
            field_name = field['name']
        codes.append(field_name)
    return codes


@csrf_view_exempt
@csrf_response_exempt
@login_required(login_url='/login')
@is_new_user
@is_datasender
def all_datasenders(request):
    manager = get_database_manager(request.user)
    projects = models.get_all_projects(manager)
    grant_web_access = False
    if request.method == 'GET' and int(request.GET.get('web', '0')):
        grant_web_access = True
    if request.method == 'POST':
        error_message, failure_imports, success_message, imported_entities = import_module.import_data(request, manager)
        all_data_senders = _get_all_datasenders(manager, projects, request.user)
        return HttpResponse(json.dumps({'success': error_message is None and is_empty(failure_imports), 'message': success_message, 'error_message': error_message,
                                        'failure_imports': failure_imports, 'all_data': all_data_senders}))

    data_senders, fields, labels = import_module.load_all_subjects_of_type(manager)
    return render_to_response('entity/all_datasenders.html', {'all_data': data_senders, 'labels': labels, 'fields': fields, 'projects':projects, 'grant_web_access':grant_web_access,
                                                              'current_language': translation.get_language()},
                              context_instance=RequestContext(request))

@csrf_view_exempt
@csrf_response_exempt
@login_required(login_url='/login')
@is_new_user
def disassociate_datasenders(request):
    manager = get_database_manager(request.user)
    projects = [Project.load(manager.database, project_id) for project_id in request.POST.get('project_id').split(';')]
    for project in projects:
        [project.data_senders.remove(id) for id in request.POST['ids'].split(';') if id in project.data_senders]
        project.save(manager)
    return HttpResponse(reverse(all_datasenders))

@csrf_view_exempt
@csrf_response_exempt
@login_required(login_url='/login')
@is_new_user
def associate_datasenders(request):
    manager = get_database_manager(request.user)
    projects = [Project.load(manager.database, project_id) for project_id in request.POST.get('project_id').split(';')]
    for project in projects:
        project.data_senders.extend([id for id in request.POST['ids'].split(';') if not id in project.data_senders])
        project.save(manager)
    return HttpResponse(reverse(all_datasenders))

def _associate_data_senders_to_project(imported_entities, manager, project_id):
    project = Project.load(manager.database, project_id)
    project.data_senders.extend([k for k, v in imported_entities.items() if v == REPORTER])
    project.save(manager)


@csrf_view_exempt
@csrf_response_exempt
@require_http_methods(['POST'])
@login_required(login_url='/login')
def import_subjects_from_project_wizard(request):
    manager = get_database_manager(request.user)
    project_id = request.GET.get('project_id')
    error_message, failure_imports, success_message, imported_entities = import_module.import_data(request, manager)
    if project_id is not None:
        _associate_data_senders_to_project(imported_entities, manager, project_id)
    return HttpResponse(json.dumps({'success': error_message is None and is_empty(failure_imports), 'message': success_message, 'error_message': error_message,
                                    'failure_imports': failure_imports}))


def _get_cleaned_data(fields, subject):
    row = {}
    for i in range(len(fields)):
        if fields[i] in subject:
            row.update({fields[i]: subject[fields[i]]})
        else:
            row.update({fields[i]:''})
    row.update({'id': subject.get("id")})
    return row

def _get_response(request, questionnaire_form, entity):
    return render_to_response('entity/create_subject_with_form.html',
                              {'questionnaire_form': questionnaire_form, 'entity': entity },
                              context_instance=RequestContext(request))


def _get_default_response(manager, request, entity_type=''):
    entity_types = _get_entity_types_without_form(manager)
    subjectForm = SubjectForm()
    return render_to_response("entity/create_subject.html", {"post_url": reverse(submit),
                                                        "entity_types": entity_types, "form": subjectForm,
                                                        "expected_type": entity_type.lower()},
                              context_instance=RequestContext(request))


def _create_request(questionnaire_form, username):
    return Request(message=questionnaire_form.cleaned_data,
                   transportInfo=
                   TransportInfo(transport="web",
                                 source=username,
                                 destination=""
                   ))

def _create_select_field(field, choices):
    if field.single_select_flag:
        return forms.ChoiceField(choices=choices, required=field.is_required(), label=field.name, initial=field.value, help_text=field.instruction)
    return forms.MultipleChoiceField(label=field.name, widget=forms.CheckboxSelectMultiple, choices=choices,
                                  initial=field.value, required=field.is_required(), help_text=field.instruction)


def _get_django_field(field):
    if isinstance(field, SelectField):
        return _create_select_field(field, _create_choices(field))
    display_field = forms.CharField(label=field.label['en'], initial=field.value, required=field.is_required(), help_text=field.instruction)
    display_field.widget.attrs["watermark"] = field.get_constraint_text()
    display_field.widget.attrs['style'] = 'padding-top: 7px;'
    return display_field

def _create_django_form(form_model):
    properties = {field.code: _get_django_field(field) for field in form_model.fields}
    properties.update({'form_code': forms.CharField(widget=HiddenInput, initial=form_model.form_code)})
    return type('QuestionnaireForm', (Form, ), properties)


def _to_list(errors, fields):
    error_dict = dict()
    for key, value in errors.items():
        error_dict.update({key: [value] if not isinstance(value, list) else value})
    return translate_messages(error_dict, fields)

def translate_messages(error_dict, fields):
    errors = dict()

    for field in fields:
        if field.code in error_dict:
            error = error_dict[field.code][0]
            if type(field) == TextField:
                text, code = error.split(' ')[1], field.code
                errors[code] = [_("Answer %s for question %s is longer than allowed.") % (text, code)]
            if type(field) == IntegerField:
                number, error_context = error.split(' ')[1], error.split(' ')[6]
                errors[field.code] = [_("Answer %s for question %s is %s than allowed.") % (number, field.code, _(error_context),)]
            if type(field) == GeoCodeField:
                errors[field.code] = [_("Incorrect GPS format. The GPS coordinates must be in the following format: xx.xxxx yy.yyyy. Example -18.8665 47.5315")]
            if type(field) == DateField:
                answer, format = error.split(' ')[1], field.date_format
                errors[field.code] = [_("Answer %s for question %s is invalid. Expected date in %s format") % (answer, field.code, format)]

    return errors


@login_required(login_url='/login')
def create_subject(request, entity_type=None):
    manager = get_database_manager(request.user)
    if entity_type is not None:
        form_model = get_form_model_by_entity_type(manager, entity_type.lower())
        if form_model is None:
            return _get_default_response(manager, request, entity_type)
    else:
        return _get_default_response(manager, request)

    QuestionnaireForm = _create_django_form(form_model)
    if request.method == 'GET':
        questionnaire_form = QuestionnaireForm()
        return _get_response(request, questionnaire_form, entity_type)

    if request.method == 'POST':
        questionnaire_form = QuestionnaireForm(request.POST)
        if not questionnaire_form.is_valid():
            return _get_response(request, questionnaire_form, entity_type)

        success_message = None
        error_message = None
        try:
            response = WebPlayer(manager, get_location_tree()).accept(_create_request(questionnaire_form, request.user.username))
            if response.success:
                success_message = _("Successfully submitted")
                questionnaire_form = QuestionnaireForm()
            else:
                questionnaire_form._errors = _to_list(response.errors, form_model.fields)
                return _get_response(request, questionnaire_form, entity_type)

        except DataObjectNotFound as exception:
            message = exception_messages.get(DataObjectNotFound).get(WEB)
            error_message = _(message) % (form_model.entity_type[0], form_model.entity_type[0])
        except Exception as exception:
            logger.exception('Web Submission failure:-')
            error_message = _(get_exception_message_for(exception=exception, channel=player.Channel.WEB))

        return render_to_response('entity/create_subject_with_form.html',
                {'questionnaire_form': questionnaire_form, 'entity': entity_type,
                 'success_message': success_message, 'error_message': error_message},
                                  context_instance=RequestContext(request))


def _check_form_code_exists(manager, name, num=''):
    form_code = "%s%s" % (name, num)
    rows = manager.load_all_rows_in_view("questionnaire", key=form_code)
    if len(rows) > 0:
        num = 1 if num == '' else num + 1
        form_code = _check_form_code_exists(manager, name, num)
    return form_code

def _create_new_reg_form_model(manager, entity_name):
    form_code = entity_name.split()
    form_code = form_code[0]
    form_code = _check_form_code_exists(manager, form_code)
    return create_reg_form_model(manager, entity_name, form_code, [entity_name])

@login_required(login_url='/login')
def edit_subject(request, entity_type=None):
    manager = get_database_manager(request.user)
    form_model = None
    if entity_type is not None:
        form_model = get_form_model_by_entity_type(manager, entity_type.lower())
        if form_model is None:
            entity_list = _get_entity_types_without_form(manager)
            if entity_type in entity_list:
                form_model = get_form_model_by_code(manager, 'reg')

    if form_model is None:
        return HttpResponseRedirect(reverse(all_subjects))

    fields = form_model.fields
    existing_questions = json.dumps(fields, default=field_to_json)
    return render_to_response('entity/edit_form.html',
            {'existing_questions': repr(existing_questions),
             'questionnaire_code': form_model.form_code,
             'entity_type': entity_type},
             context_instance=RequestContext(request))


@login_required(login_url='/login')
def create_entity_type(request):
    manager = get_database_manager(request.user)

    form_model = get_form_model_by_code(manager, 'reg')
    fields = form_model.fields
    existing_questions = json.dumps(fields, default=field_to_json)

    return render_to_response('entity/create_entity_type.html',
            {'existing_questions': repr(existing_questions),
             'questionnaire_code': 'reg'},
             context_instance=RequestContext(request))

@login_required(login_url='/login')
def export_subject(request):
    subject = request.POST.get("entity_type")
    all_data = import_module.load_all_subjects(request)
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="%s.xls"' % (subject)

    raw_data = []
    for data in all_data[0].get("data"):
        row = data[1:]
        row.insert(0, form_code)
        raw_data.append(row)
    wb = get_excel_sheet(raw_data, subject)
    wb.save(response)
    return response
