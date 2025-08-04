from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from . import views

urlpatterns = [
    path('register/user/',views.register_user.as_view(),name='register_user'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('expense_types/',views.expense_types_list.as_view(),name='expense_types_list'),
    path('expenses_types/<int:pk>',views.expense_type_detail.as_view(),name='expense_types_detail'),
    path('expenses/',views.expense_list.as_view(),name='expense_list'),
    path('expenses/<int:pk>',views.expense_detail.as_view(),name='expense_detail')
]