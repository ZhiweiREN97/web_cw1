from rating.models import User, Score, Module
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','email')

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('id','score','professor')


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('module_id', 'module_name','year','semester','prof')


class AvgSerializer(serializers.Serializer):
    class Meta:
        fields = ('p_id','module_id')