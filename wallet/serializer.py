from rest_framework import serializers

class FundSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=100, max_value=100000000)
