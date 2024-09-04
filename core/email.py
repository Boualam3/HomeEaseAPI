"""
All email template are here we can customize based on original version
https://github.com/sunscrapers/djoser/tree/master/djoser/templates/email 
"""
from django.contrib.auth.tokens import default_token_generator
# djoser imports
from templated_mail.mail import BaseEmailMessage
from djoser import utils
from djoser.conf import settings

EMAILS = {}


class ActivationEmail(BaseEmailMessage):
    """Email Activation Token Generator
    """
    template_name = "email/activation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()
        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        uid, token = context['uid'], context['token']
        # here we store all the requested tokens in a dictionary for later use
        EMAILS[user.email] = {'uid': uid, 'token': token}
        return context
