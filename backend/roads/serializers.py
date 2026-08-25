from rest_framework import serializers

from .models import Road


class RoadSerializer(serializers.ModelSerializer):
    prefecture_display = serializers.CharField(source='get_prefecture_display', read_only=True)

    class Meta:
        model = Road
        fields = '__all__'
        validators = []

    def validate_prefecture(self, value):
        return value
