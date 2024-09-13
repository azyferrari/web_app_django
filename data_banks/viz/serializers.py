from rest_framework import serializers
from .models import *

class OwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ownership
        fields = '__all__'

class HistoricalFinancialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalFinancials
        fields = '__all__'

class HistoricalValuationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalValuation
        fields = '__all__'

class OverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overview
        fields = '__all__'



        