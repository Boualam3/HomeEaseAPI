from django.db import models


class Role(models.TextChoices):
    HOST = 'HOST', 'Host'
    GUEST = 'GUEST', 'Guest'


class LANGUAGES(models.TextChoices):
    ARABIC = 'AR', 'Arabic'
    ENGLISH = 'EN', 'English'
    FRENCH = 'FR', 'French'
    SPANISH = 'ES', 'Spanish'
    # and other languages

    # we used for define default value coz it should be callable for ArrayField
    @staticmethod
    def default_language():
        return [LANGUAGES.ENGLISH]
