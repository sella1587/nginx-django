from rest_framework import serializers
from .models import ConsolidatedObjects, ObjectsFromCao

class SerialConsolidatedObject(serializers.ModelSerializer):
    class Meta:
        model = ConsolidatedObjects
        fields = []

class SerialObjectFromCao(serializers.ModelSerializer):
    class Meta:
        model = ObjectsFromCao
        fields = []