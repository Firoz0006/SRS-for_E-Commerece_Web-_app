from django.test import TestCase
from django.contrib.auth.models import User
from app.forms import CustomerRegistrationForm, LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm, CustomerProfileForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from app.models import Customer

class CustomerRegistrationFormTestCase(TestCase):
    def test_form_valid(self):
        form_data = {'username': 'testuser', 'email': 'test@example.com', 'password1': 'testpassword123', 'password2': 'testpassword123'}
        form = CustomerRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {'username': '', 'email': '', 'password1': '', 'password2': ''}
        form = CustomerRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

class LoginFormTestCase(TestCase):
    def test_form_valid(self):
        user = User.objects.create_user(username='testuser', password='testpassword123')
        form_data = {'username': 'testuser', 'password': 'testpassword123'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {'username': '', 'password': ''}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())



class MyPasswordChangeFormTestCase(TestCase):
    def test_form_valid(self):
        user = User.objects.create_user(username='testuser', password='testpassword123')
        form_data = {'old_password': 'testpassword123', 'new_password1': 'newtestpassword123', 'new_password2': 'newtestpassword123'}
        form = MyPasswordChangeForm(user=user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        user = User.objects.create_user(username='testuser', password='testpassword123')
        form_data = {'old_password': '', 'new_password1': '', 'new_password2': ''}
        form = MyPasswordChangeForm(user=user, data=form_data)
        self.assertFalse(form.is_valid())

class MyPasswordResetFormTestCase(TestCase):
    def test_form_valid(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
        form_data = {'email': 'test@example.com'}
        form = MyPasswordResetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {'email': ''}
        form = MyPasswordResetForm(data=form_data)
        self.assertFalse(form.is_valid())

class MySetPasswordFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = PasswordResetTokenGenerator().make_token(self.user)

    def test_form_valid(self):
        form_data = {
            'new_password1': 'newtestpass123',
            'new_password2': 'newtestpass123',
        }
        form = MySetPasswordForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {
            'new_password1': 'newtestpass123',
            'new_password2': 'wrongtestpass123',
        }
        form = MySetPasswordForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())

class CustomerProfileFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.customer = Customer.objects.create(user=self.user, locality='Test Locality', city='Test City', state='TS', zipcode=12345)
        self.form_data = {
            'name': 'Test User',
            'locality': 'Test Locality',
            'city': 'Test City',
            'state': 'Goa',
            'zipcode': 12345
        }

    def test_customer_profile_form_initial_data(self):
        form = CustomerProfileForm(instance=self.customer)
        self.assertEquals(form.fields['name'].initial, '')

    def test_customer_profile_form_valid_data(self):
        form = CustomerProfileForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_customer_profile_form_invalid_data(self):
        form_data = self.form_data.copy()
        form_data['state'] = 'Invalid'
        form = CustomerProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

