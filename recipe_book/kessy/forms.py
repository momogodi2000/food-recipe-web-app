from django import forms
from .models import ProposedRecipe, Recipe, User
from django.contrib.auth.forms import UserCreationForm
from .models import Recipe

class ProposedRecipeForm(forms.ModelForm):
    class Meta:
        model = ProposedRecipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'category', 'image']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'category', 'image']
        widgets = {
            'category': forms.Select(choices=Recipe.CATEGORY_CHOICES),
        }

