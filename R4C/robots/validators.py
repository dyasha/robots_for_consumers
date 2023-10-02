import datetime

from rest_framework import serializers


class RobotValidator:
    def __call__(self, value):
        DATE_NOW = datetime.datetime.now(datetime.timezone.utc)
        if value["created"] > DATE_NOW:
            message = (
                "Робот не может быть создан в будущем. "
                "Скорректируйте время создания."
            )
            raise serializers.ValidationError(message)
