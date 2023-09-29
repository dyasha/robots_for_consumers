from rest_framework import serializers
from .models import Robot
from .validators import RobotValidator


class RobotSerializer(serializers.ModelSerializer):
    serial = serializers.ReadOnlyField()

    class Meta:
        model = Robot
        fields = ("serial", "model", "version", "created")
        validators = [RobotValidator()]

    def create(self, validated_data):
        serial = (
            validated_data.get("model") + "-" + validated_data.get("version")
        )
        validated_data["serial"] = serial
        return Robot.objects.create(**validated_data)
