from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from sendgrid import Mail, SendGridAPIClient

from PlaneksTest.celery import app
from PlaneksTest.settings import SEND_GRID_API_KEY


@app.task
def send_informing_about_comment_email(news_author_id, comment_author_id, news_id, domain):
    UserModel = get_user_model()
    try:
        news_author = UserModel.objects.get(pk=news_author_id)
        comment_author = UserModel.objects.get(pk=comment_author_id)
        message = render_to_string('informing_about_comment_mail.html', {
            'news_author': news_author,
            'comment_author': comment_author,
            'domain': domain,
            'news_id': news_id
        })

        message = Mail(
            from_email='nikitiuss@gmail.com',
            to_emails=news_author.email,
            subject='К вашемей новости на сайте {} оставлен комментарий'.format(domain),
            html_content=message)
        sg = SendGridAPIClient(SEND_GRID_API_KEY)
        sg.send(message)
    except UserModel.DoesNotExist:
        pass
    except Exception as e:
        print(e)