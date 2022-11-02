from celery import shared_task
from celery.utils.log import get_task_logger
from .models import CustomerEmail
from datetime import date

@shared_task()
def show():
    today = date.today()
    emails = CustomerEmail.objects.filter(date__month=today.month)
    print("The number of new emails added in this month:",len(emails))