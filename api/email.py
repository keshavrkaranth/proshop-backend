from django.conf import settings
from django.core.mail import send_mail


def sendEmail(tomail, type, name=None, order_id=None):
    emil_from = settings.EMAIL_HOST_USER
    to_mail = [tomail, ]
    if type == 'register':
        mail_subject = 'Welcome To Proshop :)'
        message = f'Hi,{name},Thank you for registering in proshop.Hope you get your desired product at cheap price ' \
                  f'and at earliest time '
        send_mail(subject=mail_subject, message=message, from_email=emil_from, recipient_list=to_mail)
    elif type == 'order':
        mail_subject = 'Congratulations Your order is Successfully placed :)'
        message = f'Congratulations {name} Your order is successfully placed hre is your order id {order_id} kindly Note it down for future refrences.'
        send_mail(subject=mail_subject, message=message, from_email=emil_from, recipient_list=to_mail)
