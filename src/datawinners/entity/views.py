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
from mangrove.datastore.entity_type import get_all_entity_types, define_type
from datawinners.project import helper as project_helper, models
from mangrove.errors.MangroveException import EntityTypeAlreadyDefined, MangroveException, DataObjectAlreadyExists, QuestionCodeAlreadyExistsException, EntityQuestionAlreadyExistsException, DataObjectNotFound
from datawinners.entity.forms import EntityTypeForm, ReporterRegistrationForm, SubjectForm
from mangrove.form_model.form_model import get_form_model_by_code, REGISTRATION_FORM_CODE, MOBILE_NUMBER_FIELD_CODE, GEO_CODE, NAME_FIELD_CODE, LOCATION_TYPE_FIELD_CODE, ENTITY_TYPE_FIELD_CODE, REPORTER, create_reg_form_model, get_form_model_by_entity_type
from mangrove.transport.player import player
from datawinners.entity import import_data as import_module
from mangrove.utils.types import is_empty, sequence_to_str
from datawinners.entity.helper import update_questionnaire_with_questions
from mangrove.transport.player import player
from mangrove.transport.player.player import WebPlayer, Request, TransportInfo
from mangrove.form_model.form_model import get_default_questions
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
    #TODO need to refactor this code. The master dictionary should be maintained by the registration form  model
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
        json_string = request.POST['question-set']
        question_set = json.loads(json_string)
        form_model = get_form_model_by_code(manager, questionnaire_code)
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
            form_model.form_code = request.POST['questionnaire-code'].lower()
            form_model.save()
            return HttpResponse(json.dumps({"response": "ok"}))

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
    response = {}
    if form.is_valid():
        entity_name = form.cleaned_data["entity_type_regex"]
        entity_name = [entity_name.lower()]
        try:
            manager = get_database_manager(request.user)
            define_type(manager, entity_name)
            if request.POST["default_form_model"] == "false":
                form_model = _create_new_reg_form_model(manager,entity_name[0])
                response.update({"form_code": form_model.form_code})
            message = _("Entity definition successful")
            success = True
        except EntityTypeAlreadyDefined:
            message = _("%s already registered as a subject type. Please select %s from the drop down menu.") %  (entity_name[0], entity_name[0])
    else:
        message = form.fields['entity_type_regex'].error_messages['invalid']
    response.update({'success': success, 'message': _(message)})
    return HttpResponse(json.dumps(response))






def _get_entity_type_with_editable_registration_form(manager):
    form_models = manager.load_all_rows_in_view("questionnaire")
    entity_list = []
    for form_model in form_models:
        if form_model.value['flag_reg']:
            entity_list.append(form_model.value["entity_type"])
    return entity_list


def _get_entity_type_by_registration_type(manager):
    entity_types = get_all_entity_types(manager)
    project_helper.remove_reporter(entity_types)
    editable_entity_list = _get_entity_type_with_editable_registration_form(manager)
    default_entity_list = []
    for entity_type in entity_types:
        if entity_type not in editable_entity_list:
            default_entity_list.append(entity_type)
    return (default_entity_list, editable_entity_list)


@login_required(login_url='/login')
def create_subject(request, entity_type=""):
    db_manager = get_database_manager(request.user)
    entity_types = _get_entity_type_by_registration_type(db_manager)[0]
    subjectForm = SubjectForm()
    return render_to_response("entity/create_subject.html", {"post_url": reverse(submit),
                                                        "entity_types": entity_types, "form": subjectForm,
                                                        "expected_type": entity_type.lower()},
                              context_instance=RequestContext(request))

@csrf_view_exempt
@csrf_response_exempt
@login_required(login_url='/login')
@is_new_user
@is_datasender
def render_all_entities(request):
    manager = get_database_manager(request.user)
    if request.method == 'POST':
        error_message, failure_imports, success_message, imported_entities = import_module.import_data(request, manager)
        subjects_data = import_module.load_all_subjects(request)
        return HttpResponse(json.dumps({'success': error_message is None and is_empty(failure_imports), 'message': success_message, 'error_message': error_message,
                                        'failure_imports': failure_imports, 'all_data': subjects_data}))

    subjects_data = import_module.load_all_subjects(request)
    return render_to_response('entity/all_subjects.html', {'all_data': subjects_data, 'current_language': translation.get_language()},
                                  context_instance=RequestContext(request))

@csrf_view_exempt
@csrf_response_exempt
@login_required(login_url='/login')
@is_new_user
@is_datasender
def all_subjects(request):
    manager = get_database_manager(request.user)
    form_models = manager.load_all_rows_in_view("questionnaire")
    subjects_data = {}
    for form_model in form_models:
        if form_model.value['flag_reg'] and form_model.value['name'] != 'Reporter':
            entity_name = form_model.value["entity_type"][0]
            field_code = []
            for field in form_model.value["json_fields"]:
                if field['name'] == 'short_code':
                    field_name = 'short_name'
                elif field['name'] == 'geo_code':
                    field_name = 'geocode'
                elif field['name'] == 'entity_type':
                    field_name = 'type'
                else:
                    field_name = field['name']
                field_code.append(field_name)

            if entity_name == "Registration":
                registration_fields = field_code
            else:
                subjects_data[entity_name.capitalize()] = {"name": form_model.value['name'],
                                          "code": form_model.value["form_code"], "fields": field_code, "data": []}

    subjects = import_module.load_all_subjects(request)
    for subject in subjects:
        entity = subject['type'].capitalize()
        if entity not in subjects_data:
            fields = registration_fields
            subjects_data[entity] = dict(data=[], name=entity, code="registration", fields=registration_fields)
        else:
            fields = subjects_data[entity]['fields']

        row = []
        for i in range(len(fields)):
            if fields[i] in subject:
                row.append(subject[fields[i]])
            else:
                row.append('')
        subjects_data[entity]['data'].append(row)

    if request.method == 'POST':
        error_message, failure_imports, success_message, imported_entities = import_module.import_data(request, manager)
        subjects_data = import_module.load_all_subjects(request)
        return HttpResponse(json.dumps({'success': error_message is None and is_empty(failure_imports), 'message': success_message, 'error_message': error_message,
                                        'failure_imports': failure_imports, 'all_data': subjects_data}))
    
    sorted_keys = sorted(subjects_data.iterkeys())

    return render_to_response('entity/all_subjects.html', {'all_data': subjects_data,'keys':sorted_keys, 'current_language': translation.get_language()},
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
            users  = User.objects.filter(email=data['email'])
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
    
    form_model = manager.load_all_rows_in_view("questionnaire", key="rep")

    fields = _get_cleaned_fields(form_model[0]["value"]["json_fields"])
    all_data_senders = import_module.load_subject_registration_data(manager, type="reporter", filter_entities=import_module.include_of_type,tabulate_function=_tabulate, fields=fields)
    
    data_senders = []
    for data_sender in all_data_senders:
        data_senders.append(_get_cleaned_data(fields, data_sender))
        
    return render_to_response('entity/all_datasenders.html', {'all_data': data_senders, 'projects':projects, 'fields': fields, 'grant_web_access':grant_web_access,
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


def _get_submissions(request, type):
    dbm = get_database_manager(request.user)
    if type != "Registration":
        submissions = import_module.load_all_subjects_of_type(dbm, type=type)
    else:
        submissions = import_module.load_all_subjects(request)
    return submissions

def _create_select_field(field, choices):
    if field.single_select_flag:
        return forms.ChoiceField(choices=choices, required=field.is_required(), label=field.name, initial=field.value, help_text=field.instruction)
    return forms.MultipleChoiceField(label=field.name, widget=forms.CheckboxSelectMultiple, choices=choices,
                                  initial=field.value, required=field.is_required(), help_text=field.instruction)


def _get_django_field(field):
    if isinstance(field, SelectField):
        return  _create_select_field(field, _create_choices(field))
    display_field = forms.CharField(label=field.name, initial=field.value, required=field.is_required(), help_text=field.instruction)
    display_field.widget.attrs["watermark"] = field.get_constraint_text()
    display_field.widget.attrs['style'] = 'padding-top: 7px;'
    #    display_field.widget.attrs["watermark"] = "18 - 1"
    return display_field

def _create_django_form_from_form_model(form_model):
    properties = {field.code: _get_django_field(field) for field in form_model.fields}
    properties.update({'form_code': forms.CharField(widget=HiddenInput, initial=form_model.form_code)})
    return type('QuestionnaireForm', (Form, ), properties)


def _get_fields_name_and_submissions_by_form_code(request, form_code):
    dbm = get_database_manager(request.user)
    form_model = get_form_model_by_code(dbm, form_code)
    fields = form_model.fields
    if form_model.entity_defaults_to_reporter():
        fields = project_helper.hide_entity_question(fields)

def _get_cleaned_fields(fields):
    field_list = []
    for field in fields:
        if field['name'] == 'short_code':
            field_name = 'short_name'
        elif field['name'] == 'geo_code':
            field_name = 'geocode'
        elif field['name'] == 'entity_type':
            field_name = 'type'
        else:
            field_name = field['name']
        field_list.append(field_name)
    return field_list

def _get_cleaned_data(fields, subject):
    row = {}
    for i in range(len(fields)):
        if fields[i] in subject:
            row.update({fields[i]: subject[fields[i]]})
        else:
            row.update({fields[i]:''})
    row.update({'id': subject.get("id")})
    return row

def _tabulate(entity,fields):
    tabulated = {}
    for field in fields:
        value = entity.value(field) if entity.value(field) is not None else "-"
        tabulated.update({field: value})

    geocode = entity.geometry.get('coordinates')
    geocode_string = ", ".join([str(i) for i in geocode]) if geocode is not None else "--"
    location = sequence_to_str(entity.location_path, u", ")
    tabulated.update({'geocode': geocode_string})
    tabulated.update({'type': ".".join(entity.type_path)})
    tabulated.update({'short_name': entity.short_code})
    tabulated.update({'location': location})
    tabulated.update({'id': entity.id})
    return tabulated

def _get_response(questionnaire_form, subject_list, entity, request, default_type=None):
    return render_to_response('entity/web_questionnaire.html',
                              {'questionnaire_form': questionnaire_form,
                                'subjects': subject_list, 'entity': entity, "default_type": default_type
                              },
                              context_instance=RequestContext(request))


def _create_request(questionnaire_form, username):
    return Request(message=questionnaire_form.cleaned_data,
                   transportInfo=
                   TransportInfo(transport="web",
                                 source=username,
                                 destination=""
                   ))

def _create_subjects_list(manager):
    form_models = manager.load_all_rows_in_view("questionnaire")
    subject_list = []
    for form_model in form_models:
        if form_model.value['flag_reg'] and form_model.value['entity_type'][0] != 'Registration' and form_model.value['entity_type'][0] != 'reporter':
            subject = dict(url=reverse(subject_questionnaire, args=[form_model.value['entity_type'][0]]),
                name=form_model.value['name'], entity_type=form_model.value['entity_type'][0])
            subject_list.append(subject)
    return subject_list

@login_required(login_url='/login')
def subject_questionnaire(request, entity_type=None):
    manager = get_database_manager(request.user)
    subject_list = _create_subjects_list(manager)
    if len(subject_list) == 0:
        return HttpResponseRedirect(reverse(create_subject))
    else:
        entity_type = entity_type.lower() if entity_type is not None else None
        if entity_type is None or entity_type not in [ subject["entity_type"] for subject in subject_list]:
            entity_type = "Registration"

    form_model = get_form_model_by_entity_type(manager, entity_type)
    QuestionnaireForm = _create_django_form_from_form_model(form_model)

    if request.method == 'GET':
        questionnaire_form = QuestionnaireForm()
        return _get_response(questionnaire_form, subject_list, entity_type, request)

    if request.method == 'POST':
        questionnaire_form = QuestionnaireForm(request.POST)
        if not questionnaire_form.is_valid():
            return _get_response(questionnaire_form, subject_list, entity_type, request)

        success_message = None
        error_message = None
        try:
            response = WebPlayer(manager, get_location_tree()).accept(_create_request(questionnaire_form, request.user.username))
            if response.success:
                success_message = _("Successfully submitted")
                questionnaire_form = QuestionnaireForm()
            else:
                questionnaire_form._errors = _to_list(response.errors, form_model.fields)
                return _get_response(questionnaire_form, subject_list, entity_type, request)

        except DataObjectNotFound as exception:
            message = exception_messages.get(DataObjectNotFound).get(WEB)
            error_message = _(message) % (form_model.entity_type[0], form_model.entity_type[0])
        except Exception as exception:
            logger.exception('Web Submission failure:-')
            error_message = _(get_exception_message_for(exception=exception, channel=player.Channel.WEB))

        return render_to_response('entity/web_questionnaire.html',
                {'questionnaire_form': questionnaire_form, 'success_message': success_message, 'error_message': error_message,
                 'subjects': subject_list},
                                  context_instance=RequestContext(request))

@login_required(login_url='/login')
def edit_form_model(request, form_code=None):
    manager = get_database_manager(request.user)
    if form_code is None:
        fields = get_default_questions(manager)
        form_code = ""
    else:
        form_model = get_form_model_by_code(manager, form_code)
        fields = form_model.fields

    existing_questions = json.dumps(fields, default=field_to_json)
    return render_to_response('entity/edit_form.html',
            {"existing_questions": repr(existing_questions),
             'questionnaire_code': form_code},
             context_instance=RequestContext(request))

def _create_new_reg_form_model(manager, entity_name):
    form_code = entity_name.split(" ")[0]
    i = 1
    exists = manager.load_all_rows_in_view("questionnaire", key=form_code)
    while exists:
        form_code += "%s" % i
        exists = manager.load_all_rows_in_view("questionnaire", key=form_code)
        i += 1
    return create_reg_form_model(manager, entity_name, form_code, [entity_name])
