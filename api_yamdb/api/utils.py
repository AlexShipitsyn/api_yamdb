from django.conf import settings
from django.contrib.auth.tokens import default_token_generator as dtg
from django.core import mail


def send_mail(user):
    subject = 'Confirmation code'
    to = user.email
    from_email = settings.DEFAULT_FROM_EMAIL
    text_content = f'Confirmation code: {dtg.make_token(user)}'
    mail.send_mail(subject, text_content, from_email, [to])
