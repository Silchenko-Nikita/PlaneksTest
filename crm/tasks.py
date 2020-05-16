from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from sendgrid import Mail, SendGridAPIClient

from PlaneksTest.celery import app
from PlaneksTest.settings import SEND_GRID_API_KEY
from crm.tokens import account_activation_token


@app.task
def send_verification_email(user_id, domain):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        message = render_to_string('verification_email.html', {
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        message = Mail(
            from_email='nikitiuss@gmail.com',
            to_emails=user.email,
            subject='Подвердите ваш email на сайте {}'.format(domain),
            html_content=message)
        sg = SendGridAPIClient(SEND_GRID_API_KEY)
        sg.send(message)
    except UserModel.DoesNotExist:
        pass
    except Exception as e:
        print(e)