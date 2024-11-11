from django.core import mail
from django.contrib.auth.tokens import default_token_generator as dtg


def send_mail(user):
    subject = 'Confirmation code'
    to = user.email
    text_content = f'Confirmation code: {dtg.make_token(user)}'
    mail.send_mail(subject, text_content, None, [to])
