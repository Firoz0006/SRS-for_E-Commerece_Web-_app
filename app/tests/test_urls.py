from django.test import TestCase
from django.urls import reverse ,resolve
from app.views import *
from django.contrib.auth.views import * # to run some test cases present in forms not in views.py


class TestUrls(TestCase):
    
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, ProductView)

    def test_product_detail_url_resolves(self):
        url = reverse('product-detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, ProductDetailView)

    def test_add_to_cart_url_resolves(self):
        url = reverse('add-to-cart')
        self.assertEquals(resolve(url).func, add_to_cart)

    def test_show_cart_url_resolves(self):
        url = reverse('showcart')
        self.assertEquals(resolve(url).func, show_cart)

    def test_plus_cart_url_resolves(self):
        url = reverse('plus_cart')
        self.assertEquals(resolve(url).func, plus_cart)

    def test_minus_cart_url_resolves(self):
        url = reverse('minus_cart')
        self.assertEquals(resolve(url).func, minus_cart)

    def test_remove_cart_url_resolves(self):
        url = reverse('remove_cart')
        self.assertEquals(resolve(url).func, remove_cart)

    def test_profile_url_resolves(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func.view_class, ProfileView)

    def test_address_url_resolves(self):
        url = reverse('address')
        self.assertEquals(resolve(url).func, address)

    def test_orders_url_resolves(self):
        url = reverse('orders')
        self.assertEquals(resolve(url).func, orders)

    def test_mobile_url_resolves(self):
        url = reverse('mobile')
        self.assertEquals(resolve(url).func, mobile)

    def test_mobiledata_url_resolves(self):
        url = reverse('mobiledata', args=['some-data'])
        self.assertEquals(resolve(url).func, mobile)

    def test_checkout_url_resolves(self):
        url = reverse('checkout')
        self.assertEquals(resolve(url).func, checkout)

    def test_paymentdone_url_resolves(self):
        url = reverse('paymentdone')
        self.assertEquals(resolve(url).func, payment_done)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_passwordchange_url_resolves(self):
        url = reverse('passwordchange')
        self.assertEquals(resolve(url).func.view_class, PasswordChangeView)

    def test_passwordchangedone_url_resolves(self):
        url = reverse('passwordchangedone')
        self.assertEquals(resolve(url).func.view_class, PasswordChangeView)

    def test_password_reset_url_resolves(self):
        url = reverse('password_reset')
        self.assertEquals(resolve(url).func.view_class, PasswordResetView)

    def test_password_reset_done_url_resolves(self):
        url = reverse('password_reset_done')
        self.assertEquals(resolve(url).func.view_class, PasswordResetDoneView)

    def test_password_reset_confirm_url_resolves(self):
        url = reverse('password_reset_confirm', args=['uidb64', 'token'])
        self.assertEquals(resolve(url).func.view_class, PasswordResetConfirmView)

    def test_password_reset_complete_url_resolves(self):
        url = reverse('password_reset_complete')
        self.assertEquals(resolve(url).func.view_class, PasswordResetCompleteView)

    def test_customer_registration_url_resolves(self):
        url = reverse('customerregistration')
        self.assertEquals(resolve(url).func.view_class, CustomerRegistrationView)







