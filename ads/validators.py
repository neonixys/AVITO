from rest_framework.exceptions import ValidationError


def not_null(value):
    if value:
        raise ValidationError("Значение не может быть 'True'!")
