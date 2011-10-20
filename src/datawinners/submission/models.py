from django.db import models
from datawinners.messageprovider.message_handler import _get_response_message

class DatawinnerLog(models.Model):
    message = models.TextField()
    from_number = models.CharField(max_length=15)
    to_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    form_code = models.TextField(default="") #Because if there is grabage sms which doesnt have any whitespace before 20 chars this would break
    error = models.TextField()


#TODO: Move all message templating for responses here.
class SMSResponse(object):
    def __init__(self,response):
        self.response = response

    def text(self):
        return _get_response_message(self.response)