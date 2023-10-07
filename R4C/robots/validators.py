import datetime
from rest_framework import serializers


class RobotValidator:
    def __call__(self, value):
        date_now = datetime.datetime.now(datetime.timezone.utc)
        if value["created"] < date_now:
            message = (
                "Робот не может быть создан в прошлом. "
                "Скорректируйте время создания."
            )
            raise serializers.ValidationError(message)
