from .models import Expenses, Expensestypes
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Expensestypes
        fields = '__all__'

class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        return user
        
    def get_token(self,user):
        refresh=RefreshToken.for_user(user)
        return {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }