def validate_audio_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp3']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


def validate_image_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.png', '.jpg', '.bmp', '.jpeg', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')