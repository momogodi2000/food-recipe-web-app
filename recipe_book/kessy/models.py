from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User

class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='kessy_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='kessy_users_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('Appetizers & Snacks', 'Appetizers & Snacks'),
        ('Beverages & Cocktails', 'Beverages & Cocktails'),
        ('Breads & Breakfasts', 'Breads & Breakfasts'),
        ('Cakes & Frostings', 'Cakes & Frostings'),
        ('Casseroles & Skillets', 'Casseroles & Skillets'),
        ('Condiments, Spreads & Relishes', 'Condiments, Spreads & Relishes'),
        ('Cookies & Candies', 'Cookies & Candies'),
        ('Desserts', 'Desserts'),
        ('Beef', 'Beef'),
        ('Bread', 'Bread'),
        ('Chicken', 'Chicken'),
        ('Fish & Seafood', 'Fish & Seafood'),
        ('Indian Food', 'Indian Food'),
        ('Italian Food', 'Italian Food'),
        ('Lamb', 'Lamb'),
        ('Main Course', 'Main Course'),
        ('Pasta', 'Pasta'),
        ('Pork', 'Pork'),
        ('Salads', 'Salads'),
        ('Soups', 'Soups'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Ensure null=False and blank=False

    def __str__(self):
        return self.title


class ProposedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='proposed_recipe_images/', null=True, blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title
