# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_view_exempt, csrf_response_exempt
from django.views.decorators.http import require_http_methods
from datawinners.main.utils import get_db_manager_for
from datawinners.submission.models import DatawinnerLog
from mangrove.errors.MangroveException import MangroveException, SMSParserInvalidFormatException, SubmissionParseException, DataObjectNotFound, FormModelDoesNotExistsException
from mangrove.transport.player.player import SMSPlayer, Request, TransportInfo
from mangrove.transport.submissions import SubmissionHandler
from datawinners.messageprovider.message_handler import get_exception_message_for, get_submission_error_message_for, \
    get_success_msg_for_submission_using, get_success_msg_for_registration_using

SMS = "sms"
WEB = "web"


@csrf_view_exempt
@csrf_response_exempt
@require_http_methods(['POST'])
def sms(request):
    _message = request.POST["message"]
    _from = request.POST["from_msisdn"]
    _to = request.POST["to_msisdn"]
    try:
        dbm=get_db_manager_for(_to)
        sms_player = SMSPlayer(dbm,SubmissionHandler(dbm))
        transportInfo = TransportInfo(transport=SMS,source=_from, destination=_to)
        response = sms_player.accept(Request(transportInfo=transportInfo, message=_message))
        if response.success:
            if response.short_code:
                message = get_success_msg_for_registration_using(response, "Subject", "sms")
            else:
                message = get_success_msg_for_submission_using(response)
        else:
            message = get_submission_error_message_for(response.errors)

    except (SubmissionParseException,FormModelDoesNotExistsException) as exception:
        message = get_exception_message_for(exception=exception, channel=SMS)
        log = DatawinnerLog(message = _message, from_number = _from, to_number = _to, form_code = exception.data[0])
        log.save()
    except MangroveException as exception:
        print type(exception)
        message = get_exception_message_for(exception=exception, channel=SMS)

    return HttpResponse(message)


