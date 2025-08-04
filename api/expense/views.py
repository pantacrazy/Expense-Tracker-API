from django.shortcuts import render
from rest_framework import generics,status,permissions
from rest_framework.response import Response
from .serializers import (user_serializer,ExpenseCategorySerializer,ExpenseSerializer)
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Expensestypes,Expenses
from .permissions import IsOwnerOrReadOnly
from .filterset import ExpenseFilter
from django_filters.rest_framework import DjangoFilterBackend

# to register user
class register_user(generics.CreateAPIView):
    serializer_class=user_serializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        tokens=serializer.get_token(user)
        return Response({
            "tokens":tokens,
            "user":{
                'user':user.username,
                'email':user.email
            },
            "message":"User created successfully"   
            },status=status.HTTP_201_CREATED)
class expense_types_list(generics.ListCreateAPIView):
    serializer_class=ExpenseCategorySerializer
    permission_classes=[permissions.IsAuthenticated]
    queryset=Expensestypes.objects.all()
    authentication_classes=[JWTAuthentication]
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
            "message":"Expense type created successfully"   
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class expense_type_detail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=ExpenseCategorySerializer
    permission_classes=[permissions.IsAuthenticated]
    queryset=Expensestypes.objects.all()
    authentication_classes=[JWTAuthentication]

class expense_list(generics.ListCreateAPIView):
    serializer_class=ExpenseSerializer
    permission_classes=[permissions.IsAuthenticated]
    queryset=Expenses.objects.all()
    authentication_classes=[JWTAuthentication]
    filter_backends=[DjangoFilterBackend]
    filterset_class=ExpenseFilter
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
            "message":"Expense created successfully"   
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class expense_detail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=ExpenseSerializer
    permission_classes=[permissions.IsAuthenticated,IsOwnerOrReadOnly]
    queryset=Expenses.objects.all()
    authentication_classes=[JWTAuthentication]