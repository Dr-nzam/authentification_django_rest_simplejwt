from rest_framework import serializers
from compte.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        user = self.Meta.model.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user