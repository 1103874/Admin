import string
from django.conf import settings
from django.core.exceptions import ValidationError


def file_size(value):
    limit = settings.MAX_UPLOAD_FILESIZE * 1024 * 1024  # Mbytes

    if value.size > limit:
        raise ValidationError(f'첨부파일 크기가 {settings.MAX_UPLOAD_FILESIZE} Mbytes 보다 작아야 합니다.')


# def contains_special_character(value):
#     for char in value:
#         if char in string.punctuation:
#             return True
#     return False
#
#
# def validate_no_special_characters(value):
#     if contains_special_character(value):
#         raise ValidationError("특수문자를 포함할 수 없습니다.")
