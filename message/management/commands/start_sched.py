import pytz
import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from django_apscheduler.jobstores import DjangoJobStore

from message.models import Mailings, Log

logger = logging.getLogger(__name__)


def my_job():
    timezone.activate('Europe/Moscow')
    today = datetime.now()
    moskow_tz = pytz.timezone('Europe/Moscow')
    today = today.astimezone(moskow_tz)
    mailings = Mailings.objects.all()

    for mailing in mailings:
        if today >= mailing.date and mailing.state == 'start' and mailing.periodicity == 'once_a_day':
            for clien in mailing.client.all():
                send_mail(
                    subject=mailing.message.name,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[clien.email],
                )
            mailing.date = datetime.now().astimezone(moskow_tz) + timedelta(days=1)
            mailing.save()
            Log.objects.create(data=datetime.now().astimezone(moskow_tz), state='finish', email_answer=result)
        elif today >= mailing.date and mailing.state and mailing.periodicity == 'once_a_week':
            for clien in mailing.client.all():
                result = send_mail(

                    subject=mailing.message.name,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[clien.email],

                )
            mailing.date = datetime.now().astimezone(moskow_tz) + timedelta(days=7)
            mailing.save()
            Log.objects.create(data=datetime.now().astimezone(moskow_tz), state='finish', email_answer=result)
        elif today >= mailing.date and mailing.state and mailing.periodicity == 'once_a_month':
            for clien in mailing.client.all():
                send_mail(
                    subject=mailing.message.name,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[clien.email],
                )
            mailing.date = datetime.now().astimezone(moskow_tz) + timedelta(days=30)
            mailing.save()
            Log.objects.create(data=datetime.now().astimezone(moskow_tz), state='finish', email_answer=result)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
