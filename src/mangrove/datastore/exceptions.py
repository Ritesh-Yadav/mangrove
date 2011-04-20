# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

class EntityTypeAlreadyDefined(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message