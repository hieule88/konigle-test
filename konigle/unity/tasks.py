from celery import shared_task
import datetime
from unity.models import ShopOwner, CustomerEmail

@shared_task(name="send_email_task")
def send_email_task():
    current_date = datetime.date.today()
    
    list_shopes = ShopOwner.objects.all()

    for shop in list_shopes:
        count_new_emails = CustomerEmail.objects.filter(shop_owner=shop, \
                                                        created_date__year=current_date.year, \
                                                        created_date__month=current_date.month).count()
        
        # Simulate sending email
        print("Statistics of the number of new emails this month of {}: ".format(shop), count_new_emails)