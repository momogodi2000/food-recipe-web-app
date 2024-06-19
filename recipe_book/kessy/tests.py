from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Recipe, Category, ProposedRecipe

User = get_user_model()

class KessyTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Desserts")
        self.user = User.objects.create_user(username="testuser", password="password")
        self.admin = User.objects.create_superuser(username="admin", password="password")
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test Description",
            ingredients="Test Ingredients",
            instructions="Test Instructions",
            category=self.category,
            user=self.user
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kessy/home.html')

    def test_category_detail(self):
        response = self.client.get(reverse('category_detail', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kessy/category_detail.html')

    def test_recipe_detail(self):
        response = self.client.get(reverse('recipe_detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kessy/recipe_detail.html')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'password123',
            'password2': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('user_panel'))

    def test_logout_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_user_panel_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('user_panel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kessy/user_panel.html')

    def test_propose_recipe_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('propose_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kessy/propose_recipe.html')
        response = self.client.post(reverse('propose_recipe'), {
            'title': 'New Recipe',
            'description': 'New Description',
            'ingredients': 'New Ingredients',
            'instructions': 'New Instructions',
            'category': self.category.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ProposedRecipe.objects.filter(title='New Recipe').exists())

    def test_admin_panel_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('admin_panel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kessy/admin_panel.html')

    def test_crud_user_views(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('crud_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kessy/crud_user/list_users.html')

        response = self.client.get(reverse('create_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kessy/crud_user/create_user.html')

        response = self.client.post(reverse('create_user'), {
            'username': 'newadmin',
            'password1': 'password123',
            'password2': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newadmin').exists())

        user_id = User.objects.get(username='newadmin').id
        response = self.client.get(reverse('edit_user', args=[user_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kessy/crud_user/edit_user.html')

        response = self.client.post(reverse('edit_user', args=[user_id]), {
            'username': 'updatedadmin',
            'password1': 'password123',
            'password2': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='updatedadmin').exists())

        response = self.client.get(reverse('delete_user', args=[user_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kessy/crud_user/delete_user.html')

        response = self.client.post(reverse('delete_user', args=[user_id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='updatedadmin').exists())

        response = self.client.get(reverse('view_user', args=[user_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kessy/crud_user/view_user.html')

    def test_crud_recipe_views(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('crud_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kessy/crud_recipe/list_recipes.html')

        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kessy/crud_recipe/create_recipe.html')

        response = self.client.post(reverse('create_recipe'), {
            'title': 'Another Recipe',
            'description': 'Another Description',
            'ingredients': 'Another Ingredients',
            'instructions': 'Another Instructions',
            'category': self.category.id,
            'user': self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recipe.objects.filter(title='Another Recipe').exists())

        recipe_id = Recipe.objects.get(title='Another Recipe').id
        response = self.client.get(reverse('edit_recipe', args=[recipe_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kessy/crud_recipe/edit_recipe.html')

        response = self.client.post(reverse('edit_recipe', args=[recipe_id]), {
            'title': 'Updated Recipe',
            'description': 'Updated Description',
            'ingredients': 'Updated Ingredients',
            'instructions': 'Updated Instructions',
            'category': self.category.id,
            'user': self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recipe.objects.filter(title='Updated Recipe').exists())

        response = self.client.get(reverse('delete_recipe', args=[recipe_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kessy/crud_recipe/delete_recipe.html')

        response = self.client.post(reverse('delete_recipe', args=[recipe_id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Recipe.objects.filter(title='Updated Recipe').exists())

        response = self.client.get(reverse('view_recipe', args=[recipe_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kessy/crud_recipe/view_recipe.html')
