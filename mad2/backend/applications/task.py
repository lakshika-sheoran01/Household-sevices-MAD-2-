from .worker import celery
from .models import User, HouseholdRequest
from jinja2 import Template
from celery.schedules import crontab
import csv
from .mailer import send_mail

def get_html_report(username, data):
    with open("applications/report.html", "r") as file:
        jinja_template = Template(file.read())
        html_report = jinja_template.render(username=username, data=data)

        return html_report

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, monthly_report.s(), name='Report every 10 sec for test')
    sender.add_periodic_task(10.0, daily_reminder.s(), name='Daily reminder every 10 sec for test')

    sender.add_periodic_task(
        crontab(hour=18, minute=30),
        daily_reminder.s(),
        name='Daily reminder at 6:30 p.m.'
    )

    sender.add_periodic_task(
        crontab(day_of_month='1', month_of_year='*'),
        monthly_report.s(),
        name='Monthly report on 1st of every month.'
    )


@celery.task
def daily_reminder():
    customers = User.query.filter_by(customer_status=True).all()
    for customer in customers:
        msg = f'<h1>Hi {customer.username}! Please visit our service platform for updates.</h1>'
        send_mail(email=customer.username, email_content=msg, subject="Daily Reminder")
    print('Reminder Sent!')

    professionals = User.query.filter_by(professional_status=True).all()
    for professional in professionals:
        msg = f'<h1>Hi {professional.username}! Please check your professional dashboard for updates.</h1>'
        send_mail(email=professional.username, email_content=msg, subject="Daily Reminder")
    
    print('Reminder Sent!')

@celery.task
def monthly_report():
    customers = User.query.filter_by(customer_status=True).all()
    for customer in customers:
        requests = HouseholdRequest.query.filter_by(client_id=customer.id).all()
        order_details = []
        
        for req in requests:
            temp_order = [
                req.id,
                req.service.service_title if req.service else 'Unknown',
                req.request_type,
                req.request_status,
                req.created_at,
                req.closed_at or 'Pending'
            ]
            order_details.append(temp_order)
        
        html_report = get_html_report(username=customer.username, data=order_details)
        send_mail(email=customer.user_address, email_content=html_report, subject="Monthly Report")

    print("Monthly Reports Sent!")

@celery.task
def data_export(details, email='admin'):
    with open('data_export.csv', 'w', newline='') as csvfile:
        fieldnames = ['Service Title', 'Request Type', 'Created At', 'Closed At', 'Review']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(details)
    
    send_mail(
        email=email,
        email_content="Please find the exported request data.",
        subject="Data Export",
        attachment="data_export.csv"
    )
    return "Data Exported Successfully!"
