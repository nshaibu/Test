import csv
import time
from django.core.mail import send_mail
from django.core.files.storage import default_storage
from celery.utils.log import get_task_logger
from program_test.celery import app


logger = get_task_logger(__name__)


@app.task(name="send_notification_email")
def send_notification_email(email: str, message: str):
    msg = "Hello,\n"
    msg += message
    logger.info(message)
    try:
        send_mail(subject="Service Done",
                  message=message,
                  from_email="system@example.com",
                  recipient_list=[email], fail_silently=False)
    except Exception:
        pass


@app.task(name="process_csv_file")
def process_csv_file(file_name, user_email=None):
    from api.serializers import DiagnosisCodeSerializer
    start_time = time.time()
    failure_count = 0
    success_count = 0
    fd = default_storage.open(file_name, "r")
    reader = csv.reader(fd)
    for row in reader:
        try:
            conf = {
                "category_code": row[0],
                "diagnosis_code": row[1],
                "full_code": row[2],
                "abbreviated_description": row[3],
                "full_description": row[4],
                "category_title": row[5]
            }
            serializer = DiagnosisCodeSerializer(data=conf)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except:
            failure_count += 1
        else:
            success_count += 1
    end_time = time.time()
    msg_template = f"We are done processing your file `{file_name}`." \
                   f"\nIt took {end_time - start_time}ms with {failure_count}" \
                   f" failures and {success_count} successful uploads.\n"
    if user_email:
        send_notification_email.delay(user_email, msg_template)


