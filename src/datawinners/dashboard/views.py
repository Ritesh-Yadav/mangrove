# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import json
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from datawinners.accountmanagement.models import NGOUserProfile, Organization
from datawinners.accountmanagement.views import is_datasender

from datawinners.main.utils import get_database_manager
from datawinners.project.models import ProjectState, Project
from datawinners.project.wizard_view import edit_project
from mangrove.form_model.form_model import FormModel
from mangrove.transport.player import player
from mangrove.transport.reporter import find_reporter

def _find_reporter_name(dbm, row):
    channel = row.value.get("channel")
    if channel == player.Channel.SMS:
        reporters = dbm.load_all_rows_in_view('reporters_by_number_and_name',key=(row.value["source"]))
        reporter = reporters[0].value
    else:
        reporter = ""
    return reporter


def _make_message(row):
    if row.value["status"]:
        message = " ".join(["%s: %s" % (k, v) for k, v in row.value["values"].items()])
    else:
        message = row.value["error_message"]
    return message

@login_required(login_url='/login')
@csrf_exempt
def get_submission(request, project_id):
    dbm = get_database_manager(request.user)
    project = Project.load(dbm.database, project_id)
    form_model = FormModel.get(dbm, project.qid)
    rows = dbm.load_all_rows_in_view('submissionlog', startkey=[form_model.form_code], endkey=[form_model.form_code, {}],
                                     group=True, group_level=1, reduce=True)
    submission_success,submission_errors = 0, 0
    for row in rows:
        submission_success = row["value"]["success"]
        submission_errors = row["value"]["count"] - row["value"]["success"]
    response = json.dumps([submission_success, submission_errors])
    return HttpResponse(response)

def _get_submission_breakup(dbm, form_code):
    submission_success = 0
    submission_errors = 0
    rows = dbm.load_all_rows_in_view('submissionlog', startkey=[form_code], endkey=[form_code, {}],
                                     group=True, group_level=1, reduce=True)
    for row in rows:
        submission_success = row["value"]["success"]
        submission_errors = row["value"]["count"] - row["value"]["success"]
    return submission_errors, submission_success


def get_submissions(dbm, form_code):
    rows = dbm.load_all_rows_in_view('submissionlog', reduce=False, descending=True, startkey=[form_code, {}],
                                     endkey=[form_code], limit=7)
    if not rows:
        return [], 0, 0

    submission_list = []
    for row in rows:
        reporter = _find_reporter_name(dbm, row)
        message = _make_message(row)
        submission = dict(message=message, created=row.value["submitted_on"], reporter=reporter,
                          status=row.value["status"])
        submission_list.append(submission)
    submission_errors, submission_success = _get_submission_breakup(dbm, form_code)
    return submission_list, submission_success, submission_errors


def is_project_inactive(row):
    return row['value']['state'] == ProjectState.INACTIVE


@login_required(login_url='/login')
@is_datasender
def dashboard(request):
    manager = get_database_manager(request.user)
    user_profile = NGOUserProfile.objects.get(user=request.user)
    organization = Organization.objects.get(org_id=user_profile.org_id)
    project_list = []
    rows = manager.load_all_rows_in_view('all_projects', descending=True, limit=4)
    for row in rows:
        link = reverse("project-overview", args=(row['value']['_id'],))
        if row['value']['state'] == ProjectState.INACTIVE:
            link = reverse(edit_project,args=(row['value']['_id'],))

        form_model = manager.get(row['value']['qid'], FormModel)
        submissions, success, errors = get_submissions(manager, form_model.form_code)

        project = dict(name=row['value']['name'], link=link, submissions=submissions, success=success, errors=errors,
                       inactive=is_project_inactive(row), id=row['value']['_id'])
        project_list.append(project)

    return render_to_response('dashboard/home.html',
            {"projects": project_list, 'trial_account': organization.in_trial_mode}, context_instance=RequestContext(request))


@login_required(login_url='/login')
def start(request):
    text_dict = {'project': _('Projects'), 'datasenders': _('Data Senders'),
                 'subjects': _('Subjects'), 'alldata': _('Data Records')}

    tabs_dict = {'project': 'projects', 'datasenders': 'data_senders',
                 'subjects': 'subjects', 'alldata': 'all_data'}
    page = request.GET['page']
    page = page.split('/')
    url_tokens = [each for each in page if each != '']
    text = text_dict[url_tokens[-1]]
    return render_to_response('dashboard/start.html',
            {'text': text, 'title': text, 'active_tab': tabs_dict[url_tokens[-1]]},
                              context_instance=RequestContext(request))
