from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient,APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import ErrorDetail
from .models import Expenses,Expensestypes
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta

user={
            'username':'rolo',
            'password':'rolo12345',
            'email':'rolo@rolo.com'
        }

data_expenses_types= [{'name':'Groceries'},{'name':'Leisure'},{'name':'Electronics'}]
class UsersTest(TestCase):
 
    def test_register_user(self):
        url=reverse('register_user')
        response=self.client.post(url,user,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertIn('tokens',response.data)
        self.assertIn('user',response.data)
        self.assertIn('message',response.data)
        self.assertEqual(response.data['message'],'User created successfully')
        self.assertIn('refresh',response.data['tokens'])
        self.assertIn('access',response.data['tokens'])
    def test_user_login(self):
        url=reverse('login')
        User.objects.create_user(**user)
        data={
            'username':user['username'],
            'password':user['password']
        }
        response=self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('access',response.data)
        self.assertIn('refresh',response.data)
    def test_token_refresh(self):
        User.objects.create_user(**user)
        data={
            'username':user['username'],
            'password':user['password']
        }
        url_login=reverse('login')
        response=self.client.post(url_login,data,format='json')
        refresh_token=response.data['refresh']
        url=reverse('token_refresh')
        data={
            'refresh':refresh_token
        }
        response=self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('access',response.data)
     
class ExpenseTypesTest(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(**user)
        self.client=APIClient()
        self.accestoken=str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.accestoken)

    def test_expense_types_list(self):
        url=reverse('expense_types_list')
        for expense_type in data_expenses_types:
            Expensestypes.objects.create(**expense_type)
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        names=[item['name'] for item in response.data]
        for data in data_expenses_types:
            self.assertIn(data['name'],names)
    
    def test_expense_types_create(self):
        url=reverse('expense_types_list')
        new_expense_type={
            'name':'newexpense'
        }
        response=self.client.post(url,new_expense_type,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertIn('message',response.data)
        self.assertEqual(response.data['message'],'Expense type created successfully')
    
    def test_expense_types_update(self):
        expense_type=Expensestypes.objects.create(**data_expenses_types[0])
        url=reverse('expense_types_detail',kwargs={'pk':expense_type.pk})
        update_expense=data_expenses_types[0]
        update_expense['name']='newexpense'
        response=self.client.put(url,update_expense,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'newexpense')
        expense_type.refresh_from_db()
        self.assertEqual(expense_type.name, 'newexpense')
    
    def test_expense_types_delete(self):
        expense_type=Expensestypes.objects.create(**data_expenses_types[0])
        url=reverse('expense_types_detail',kwargs={'pk':expense_type.pk})
        response=self.client.delete(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Expensestypes.objects.all()),0)
    
    def test_expense_types_detail(self):
        expense_type=Expensestypes.objects.create(**data_expenses_types[0])
        url=reverse('expense_types_detail',kwargs={'pk':expense_type.pk})
        response=self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['name'],data_expenses_types[0]['name'])
        self.assertEqual(response.data['id'],expense_type.id)

    def test_update_with_invalid_data(self):
        expense_type = Expensestypes.objects.create(**data_expenses_types[0])
        url = reverse('expense_types_detail', kwargs={'pk': expense_type.pk})
    
        invalid_data = {'name': ''} 
        response = self.client.put(url, invalid_data, format='json')
    
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_update_non_existent_type(self):
        url = reverse('expense_types_detail', kwargs={'pk': 999})
        response = self.client.put(url, {'name': 'test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_unauthenticated(self):
        expense_type = Expensestypes.objects.create(**data_expenses_types[0])
        url = reverse('expense_types_detail', kwargs={'pk': expense_type.pk})
        self.client.credentials()
        response = self.client.put(url, {'name': 'test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_nonexistent_expense_type(self):
        non_existent_pk = 9999 
        url = reverse('expense_types_detail', kwargs={'pk': non_existent_pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        error=ErrorDetail(string='No Expensestypes matches the given query.', code='not_found')
        self.assertEqual(response.data['detail'], error)  
    
    def test_get_expense_type_unauthenticated(self):
        expense_type = Expensestypes.objects.create(**data_expenses_types[0])
        url = reverse('expense_types_detail', kwargs={'pk': expense_type.pk})
        self.client.credentials()  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_delete_nonexistent_expense_type(self):
        non_existent_pk = 9999
        url = reverse('expense_types_detail', kwargs={'pk': non_existent_pk})
    
        response = self.client.delete(url)
    
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        error=ErrorDetail(string='No Expensestypes matches the given query.', code='not_found')
        self.assertEqual(response.data['detail'], error)
    
    def test_delete_expense_type_unauthenticated(self):
        expense_type = Expensestypes.objects.create(**data_expenses_types[0])
        url = reverse('expense_types_detail', kwargs={'pk': expense_type.pk})
    
        self.client.credentials()
    
        response = self.client.delete(url)
    
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
    
    def test_delete_already_deleted_type(self):
        expense_type = Expensestypes.objects.create(**data_expenses_types[0])
        url = reverse('expense_types_detail', kwargs={'pk': expense_type.pk})
    

        self.client.delete(url)
   
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
class ExpenseTest(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(**user)
        self.client=APIClient()
        self.accestoken=str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.accestoken)
    
    def test_list_expenses(self):
        expense_type = Expensestypes.objects.create(**data_expenses_types[0])
        time=timezone.now()
        Expenses.objects.create(owner=self.user, type=expense_type,
                                           amount=100,title='A good Expense',date=time)
        url = reverse('expense_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['amount'], 100)
        self.assertEqual(response.data[0]['title'], 'A good Expense')
        self.assertEqual(response.data[0]['type'],expense_type.pk)
        self.assertEqual(response.data[0]['date'], time.strftime('%Y-%m-%d'))
        self.assertEqual(response.data[0]['owner'],self.user.pk)
    def test_add_expenses(self):
        time=timezone.now()
        expense_type = Expensestypes.objects.create(**data_expenses_types[0])
        url=reverse('expense_list')
        data={
            'amount':100,
            'title':'A good Expense',
            'type':expense_type.pk,
            'date':time.strftime('%Y-%m-%d'),
            'owner':self.user.pk
        }
        response=self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertIn('message',response.data)
        self.assertEqual(response.data['message'],'Expense created successfully')
    
    def test_update_expense(self):
        expense_type = Expensestypes.objects.create(**data_expenses_types[0])
        time=timezone.now()
        expense=Expenses.objects.create(owner=self.user, type=expense_type,
                                           amount=100,title='A good Expense',date=time)
        url=reverse('expense_detail',kwargs={'pk':expense.pk})
        data={
            'amount':200,
            'title':'A bad Expense',
            'type':expense_type.pk,
            'date':time.strftime('%Y-%m-%d'),
            'owner':self.user.pk
        }
        response=self.client.put(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('amount',response.data)
        self.assertIn('title',response.data)
        self.assertIn('type',response.data)
        self.assertIn('date',response.data)
        self.assertIn('owner',response.data)
        self.assertEqual(response.data['amount'],200)
        self.assertEqual(response.data['title'],'A bad Expense')
        self.assertEqual(response.data['type'],expense_type.pk)
        self.assertEqual(response.data['date'],time.strftime('%Y-%m-%d'))
        self.assertEqual(response.data['owner'],self.user.pk)
    def test_get_expense(self):
        expense_type = Expensestypes.objects.create(**data_expenses_types[0])
        time=timezone.now()
        expense=Expenses.objects.create(owner=self.user, type=expense_type,
                                           amount=100,title='A good Expense',date=time)
        url=reverse('expense_detail',kwargs={'pk':expense.pk})
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('amount',response.data)
        self.assertIn('title',response.data)
        self.assertIn('type',response.data)
        self.assertIn('date',response.data)
        self.assertIn('id',response.data)
        self.assertEqual(response.data['amount'],100)
        self.assertEqual(response.data['title'],'A good Expense')
        self.assertEqual(response.data['type'],expense_type.pk)
        self.assertEqual(response.data['date'],time.strftime('%Y-%m-%d'))
        self.assertEqual(response.data['owner'],self.user.pk)
    
    def test_delete_expense(self):
        expense_type = Expensestypes.objects.create(**data_expenses_types[0])
        time=timezone.now()
        expense=Expenses.objects.create(owner=self.user, type=expense_type,
                                           amount=100,title='A good Expense',date=time)
        url=reverse('expense_detail',kwargs={'pk':expense.pk})
        response=self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Expenses.objects.all()),0)

class ExpenseFilterTests(APITestCase):
    def setUp(self):
    
        user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com'
        }
        self.user = User.objects.create_user(**user_data)
        self.client = APIClient()
        self.accesstoken = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.accesstoken)

        self.food_type = Expensestypes.objects.create(name='Comida')
        self.transport_type = Expensestypes.objects.create(name='Transporte')
        

        self.today = date.today()
        self.yesterday = self.today - timedelta(days=1)
        self.last_week = self.today - timedelta(weeks=1)
        self.last_month = self.today - relativedelta(months=1)
        
  
        Expenses.objects.create(
            title='Almuerzo hoy', 
            amount=15.0, 
            type=self.food_type,
            date=self.today,
            owner=self.user
        )
        
        Expenses.objects.create(
            title='Cena ayer', 
            amount=20.0, 
            type=self.food_type,
            date=self.yesterday,
            owner=self.user
        )
        
        Expenses.objects.create(
            title='Bus semana pasada', 
            amount=2.5, 
            type=self.transport_type,
            date=self.last_week,
            owner=self.user
        )
        
        Expenses.objects.create(
            title='Gasolina mes pasado', 
            amount=30.0, 
            type=self.transport_type,
            date=self.last_month,
            owner=self.user
        )
        
        
        self.list_url = reverse('expense_list')

    def test_filter_by_start_date(self):
      
        start_date = (self.today - timedelta(days=2)).strftime('%Y-%m-%d')
        
        response = self.client.get(self.list_url, {'start_date': start_date})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) 
        titles = [item['title'] for item in response.data]
        self.assertIn('Almuerzo hoy', titles)
        self.assertIn('Cena ayer', titles)
        self.assertNotIn('Bus semana pasada', titles)

    def test_filter_by_end_date(self):

        end_date = (self.today - timedelta(days=3)).strftime('%Y-%m-%d')
        
        response = self.client.get(self.list_url, {'end_date': end_date})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  
        titles = [item['title'] for item in response.data]
        self.assertIn('Bus semana pasada', titles)
        self.assertIn('Gasolina mes pasado', titles)
        self.assertNotIn('Almuerzo hoy', titles)

    def test_filter_by_date_range(self):
        
        start_date = (self.today - timedelta(days=10)).strftime('%Y-%m-%d')
        end_date = (self.today - timedelta(days=2)).strftime('%Y-%m-%d')
        
        response = self.client.get(self.list_url, {
            'start_date': start_date,
            'end_date': end_date
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  
        self.assertEqual(response.data[0]['title'], 'Bus semana pasada')

    def test_filter_by_last_weeks(self):
        
        response = self.client.get(self.list_url, {'week': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        titles = [item['title'] for item in response.data]
        self.assertIn('Almuerzo hoy', titles)
        self.assertIn('Cena ayer', titles)
        self.assertIn('Bus semana pasada', titles)
        self.assertNotIn('Gasolina mes pasado', titles)

    def test_filter_by_last_months(self):
       
        response = self.client.get(self.list_url, {'last_months': 2})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  
        titles = [item['title'] for item in response.data]
        self.assertIn('Almuerzo hoy', titles)
        self.assertIn('Cena ayer', titles)
        self.assertIn('Bus semana pasada', titles)
        self.assertIn('Gasolina mes pasado', titles)

    def test_filter_combined_type_and_date(self):
        
        response = self.client.get(self.list_url, {
            'type': self.food_type.id,
            'start_date': (self.today - timedelta(days=3)).strftime('%Y-%m-%d')
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  
        for item in response.data:
            self.assertEqual(item['type'], self.food_type.id)
            self.assertIn(item['title'], ['Almuerzo hoy', 'Cena ayer'])

    def test_empty_filter_results(self):
        
        future_date = (self.today + timedelta(days=365)).strftime('%Y-%m-%d')
        response = self.client.get(self.list_url, {'start_date': future_date})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_invalid_date_format(self):
       
        response = self.client.get(self.list_url, {'start_date': '2023-13-01'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('start_date', response.data)