from rest_framework import serializers
from .models import Ds18b20


class dstser(serializers.ModelSerializer):
    class Meta:
        model = Ds18b20
        fields = ['dt','tmp','vbat']


class dstser1(serializers.ModelSerializer):
    class Meta:
        model = Ds18b20
        fields = ['tmp','vbat', 'dt']


