from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import Product, Cart, OrderPlaced ,Customer
from app.forms import CustomerRegistrationForm


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.mobile_url = reverse('mobile')
        self.registration_url = reverse('customerregistration')
        self.product_url = reverse('product-detail', args=[1])
        self.add_to_cart_url = reverse('add-to-cart')
        self.show_cart_url = reverse('showcart')
        self.plus_cart_url = reverse('plus_cart')
        self.minus_cart_url = reverse('minus_cart')
        self.remove_cart_url = reverse('remove_cart')
        
        self.test_user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        self.test_product = Product.objects.create(
            title='Test Product',
            selling_price='100.00',
            discounted_price='90.00',
            description='Test description',
            brand='Test Brand',
            category='M',
            product_image ='productimg.jpg'
            
        )
        self.test_cart = Cart.objects.create(
            user=self.test_user,
            product=self.test_product,
            quantity=1
        )

    def test_home_view(self): #test_home_GET
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/home.html')

    def test_product_detail_GET(self):
        response = self.client.get(self.product_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/productdetail.html')

    def test_add_to_cart(self):
        response = self.client.get(self.add_to_cart_url, {'prod_id': self.test_product.id})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Cart.objects.count(), 1)

    def test_plus_cart(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.plus_cart_url, {'prod_id': self.test_product.id})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Cart.objects.get(id=self.test_cart.id).quantity, 2)

    def test_minus_cart(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.minus_cart_url, {'prod_id': self.test_product.id})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Cart.objects.get(id=self.test_cart.id).quantity, 1)

    def test_remove_cart(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.remove_cart_url, {'prod_id': self.test_product.id})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Cart.objects.count(), 0)


    def test_mobile_view(self):
        response = self.client.get(self.mobile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/mobile.html')

    def test_customer_registration_view(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/customerregistration.html')


    def test_customer_registration_form_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomerRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_customer_registration_form_invalid(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass456'
        }
        form = CustomerRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_show_cart_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('showcart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/addtocart.html')

    def test_show_cart_GET(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.show_cart_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/addtocart.html')


