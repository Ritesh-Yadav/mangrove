# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from _collections import defaultdict
from datetime import datetime
from mangrove.errors.MangroveException import AnswerTooBigException, AnswerTooSmallException, AnswerTooLongException, AnswerTooShortException, AnswerWrongType, IncorrectDate
from mangrove.form_model.validation import IntegerConstraint, ConstraintAttributes, TextConstraint, ChoiceConstraint
from validate import VdtValueTooBigError, VdtValueTooSmallError, VdtValueTooLongError, VdtValueTooShortError, VdtTypeError


def field_to_json(object):
    assert isinstance(object, Field)
    return object._to_json()


class field_attributes(object):
    '''Constants for referencing standard attributes in questionnaire.'''
    LANGUAGE = "language"
    FIELD_CODE = "question_code"
    INTEGER_FIELD = "integer"
    TEXT_FIELD = "text"
    SELECT_FIELD = 'select1'
    DATE_FIELD = 'date'
    MULTISELECT_FIELD = 'select'
    DEFAULT_LANGUAGE = "eng"
    ENTITY_QUESTION_FLAG = 'entity_question_flag'
    NAME = "name"


class Field(object):
    NAME = "name"
    LABEL = "label"
    TYPE = "type"
    QUESTION_CODE = "question_code"

    _DEFAULT_VALUES = {
        NAME: "",
        TYPE: "",
        QUESTION_CODE: "",
        }

    _DEFAULT_LANGUAGE_SPECIFIC_VALUES = {
        LABEL: {},
        }

    def __init__(self, **kwargs):
        self._dict = defaultdict(dict)
        for k, default_value in self._DEFAULT_VALUES.items():
            self._dict[k] = kwargs.get(k, default_value)

        for k, default_langauge_specific_value in self._DEFAULT_LANGUAGE_SPECIFIC_VALUES.items():
            a = kwargs.get(field_attributes.LANGUAGE, field_attributes.DEFAULT_LANGUAGE)
            language_dict = {a: kwargs.get(k)}
            self._dict[k] = language_dict

    @property
    def name(self):
        return self._dict.get(self.NAME)

    @property
    def label(self):
        return self._dict.get(self.LABEL)

    @property
    def type(self):
        return self._dict.get(self.TYPE)

    @property
    def question_code(self):
        return self._dict.get(self.QUESTION_CODE)

    @property
    def is_entity_field(self):
        return False

    def _to_json(self):
        return self._dict

    def add_or_edit_label(self, label, language=None):
        language_to_add = language if language is not None else field_attributes.DEFAULT_LANGUAGE
        self._dict[self.LABEL][language_to_add] = label


class IntegerField(Field):
    RANGE = "range"

    def __init__(self, name, question_code, label, range=None, language=field_attributes.DEFAULT_LANGUAGE):
        Field.__init__(self, type=field_attributes.INTEGER_FIELD, name=name, question_code=question_code,
                       label=label, language=language)

        self.constraint = range if range is not None else IntegerConstraint()
        self._dict[self.RANGE] = self.constraint._to_json()

    def validate(self, value):
        try:
            return self.constraint.validate(value)
        except VdtValueTooBigError:
            raise AnswerTooBigException(self._dict[field_attributes.FIELD_CODE], value)
        except VdtValueTooSmallError:
            raise AnswerTooSmallException(self._dict[field_attributes.FIELD_CODE], value)
        except VdtTypeError:
            raise AnswerWrongType(self._dict[field_attributes.FIELD_CODE])

    @property
    def range(self):
        return self._dict.get(self.RANGE)


class DateField(Field):
    DATE_FORMAT = "date_format"

    def __init__(self, name, question_code, label, date_format, language=field_attributes.DEFAULT_LANGUAGE):
        Field.__init__(self, type=field_attributes.DATE_FIELD, name=name, question_code=question_code,
                       label=label, language=language)

        self._dict[self.DATE_FORMAT] = date_format

    def validate(self, value):
        try:
            return datetime.strptime(value, self._dict[self.DATE_FORMAT])
        except ValueError:
            raise IncorrectDate(self._dict.get(field_attributes.FIELD_CODE), value, self._dict.get(self.DATE_FORMAT))

    @property
    def date_format(self):
        return self._dict.get(self.DATE_FORMAT)


class TextField(Field):
    DEFAULT_VALUE = "defaultValue"
    LENGTH = "length"
    ENTITY_QUESTION_FLAG = 'entity_question_flag'

    def __init__(self, name, question_code, label, length=None, defaultValue=None,
                 language=field_attributes.DEFAULT_LANGUAGE, entity_question_flag=False):
        Field.__init__(self, type=field_attributes.TEXT_FIELD, name=name, question_code=question_code,
                       label=label, language=language)
        self._dict[self.DEFAULT_VALUE] = defaultValue if defaultValue is not None else ""
        self.constraint = length if length is not None else TextConstraint()
        self._dict[self.LENGTH] = self.constraint._to_json()
        if entity_question_flag:
            self._dict[self.ENTITY_QUESTION_FLAG] = entity_question_flag

    def validate(self, value):
        try:
            return self.constraint.validate(value)
        except VdtValueTooLongError:
            raise AnswerTooLongException(self._dict[field_attributes.FIELD_CODE], value)
        except VdtValueTooShortError:
            raise AnswerTooShortException(self._dict[field_attributes.FIELD_CODE], value)

    @property
    def is_entity_field(self):
        return self._dict.get(self.ENTITY_QUESTION_FLAG)


class SelectField(Field):
    OPTIONS = "options"

    def __init__(self, name, question_code, label, options, language=field_attributes.DEFAULT_LANGUAGE,
                 single_select_flag=True):
        assert len(options) > 0
        type = field_attributes.SELECT_FIELD if single_select_flag else field_attributes.MULTISELECT_FIELD
        self.SINGLE_SELECT_FLAG = single_select_flag
        Field.__init__(self, type=type, name=name, question_code=question_code,
                       label=label, language=language)
        self._dict[self.OPTIONS] = []
        valid_choices = self._dict[self.OPTIONS]
        if options is not None:
            for option in options:
                if isinstance(option, tuple):
                    single_language_specific_option = {'text': {language: option[0]}, 'val': option[1]}
                elif isinstance(option, dict):
                    single_language_specific_option = option
                else:
                    single_language_specific_option = {'text': {language: option}}
                valid_choices.append(single_language_specific_option)
        self.constraint = ChoiceConstraint(list_of_valid_choices=[each.get('text').get(language) for each in valid_choices], single_select_constraint=single_select_flag, question_code=question_code)

    SINGLE_SELECT_FLAG = 'single_select_flag'

    def validate(self, value):
        return self.constraint.validate(answer=value)

    @property
    def options(self):
        return self._dict.get(self.OPTIONS)


def create_question_from(dictionary):
    """
     Given a dictionary that defines a question, this would create a field with all the validations that are
     defined on it.
    """
    type = dictionary.get("type")
    name = dictionary.get("name")
    code = dictionary.get("question_code")
    is_entity_question = dictionary.get("entity_question_flag")
    label = dictionary.get("label")
    if type == "text":
        length_dict = dictionary.get("length")
        length = TextConstraint(min=length_dict.get(ConstraintAttributes.MIN),
                                max=length_dict.get(ConstraintAttributes.MAX))
        return TextField(name=name, question_code=code, label=label, entity_question_flag=is_entity_question,
                         length=length)
    elif type == "integer":
        range_dict = dictionary.get("range")
        range = IntegerConstraint(min=range_dict.get(ConstraintAttributes.MIN),
                                  max=range_dict.get(ConstraintAttributes.MAX))
        return IntegerField(name=name, question_code=code, label=label, range=range)
    elif type == "date":
        date_format = dictionary.get("date_format")
        return DateField(name=name, question_code=code, label=label, date_format=date_format)
    elif type == "select" or type == "select1":
        choices = dictionary.get("options")
        single_select = True if type == "select1" else False
        return SelectField(name=name, question_code=code, label=label, options=choices,
                           single_select_flag=single_select)
    return None
