from django.core.mail import send_mail

from robots.models import Robot
from waitlist.models import WaitList


class SMessage:
    def get_robot(data):
        return Robot.objects.get(
            model=data["model"],
            version=data["version"],
            created=data["created"],
        )

    def waitlist_entry(serial):
        return WaitList.objects.filter(robot_serial=serial).first()

    def send_message(data):
        robot = SMessage.get_robot(data)
        entry = SMessage.waitlist_entry(robot.serial)
        if entry:
            customer_email = entry.customer.email
            robot_model = robot.model
            robot_version = robot.version
            subject = "Робот в наличии."
            message = (
                f"Добрый день!\n"
                f"Недавно вы интересовались нашим роботом модели {robot_model}, версии {robot_version}.\n"
                f"Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."
            )
            from_email = "vladislaw.beresnev2018@yandex.ru"
            recipient_list = [customer_email]
            send_mail(subject, message, from_email, recipient_list)
            entry.delete()
