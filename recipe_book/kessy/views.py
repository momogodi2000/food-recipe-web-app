from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .models import Recipe, Category, ProposedRecipe, User
from .forms import ProposedRecipeForm, CustomUserCreationForm, RecipeForm
from .models import Recipe
from django.views.generic import ListView

def home(request):
    categories = Category.objects.all()
    recipes = Recipe.objects.all()
    return render(request, 'kessy/home.html', {'categories': categories, 'recipes': recipes})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    recipes = Recipe.objects.filter(category=category)
    return render(request, 'kessy/category_detail.html', {'category': category, 'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'kessy/recipe_detail.html', {'recipe': recipe})

@login_required
def propose_recipe(request):
    if request.method == 'POST':
        form = ProposedRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            proposed_recipe = form.save(commit=False)
            proposed_recipe.user = request.user
            proposed_recipe.save()
            return redirect('user_panel')
    else:
        form = ProposedRecipeForm()
    return render(request, 'kessy/propose_recipe.html', {'form': form})

@login_required
def user_panel(request):
    proposed_recipes = ProposedRecipe.objects.filter(user=request.user)
    return render(request, 'kessy/user_panel.html', {'proposed_recipes': proposed_recipes})

@user_passes_test(lambda u: u.is_superuser)
def admin_panel(request):
    if request.method == 'POST':
        if 'approve' in request.POST:
            recipe_id = request.POST.get('recipe_id')
            proposed_recipe = ProposedRecipe.objects.get(id=recipe_id)
            Recipe.objects.create(
                user=proposed_recipe.user,
                title=proposed_recipe.title,
                description=proposed_recipe.description,
                ingredients=proposed_recipe.ingredients,
                instructions=proposed_recipe.instructions,
                category=proposed_recipe.category,
                image=proposed_recipe.image
            )
            proposed_recipe.approved = True
            proposed_recipe.save()
        elif 'delete' in request.POST:
            recipe_id = request.POST.get('recipe_id')
            ProposedRecipe.objects.get(id=recipe_id).delete()
    proposed_recipes = ProposedRecipe.objects.filter(approved=False)
    return render(request, 'kessy/admin_panel.html', {'proposed_recipes': proposed_recipes})
    

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_superuser:
                return redirect('admin_panel')
            else:
                return redirect('user_panel')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('admin_panel')
            else:
                return redirect('user_panel')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def password_reset_request(request):
    # Implement password reset logic here
    return render(request, 'registration/password_reset.html')


## user crud
@user_passes_test(lambda u: u.is_superuser)
def crud_user(request):
    users = User.objects.all()
    return render(request, 'kessy/crud_user/list_users.html', {'users': users})

@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crud_user')
    else:
        form = CustomUserCreationForm()
    return render(request, 'kessy/crud_user/create_user.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('crud_user')
    else:
        form = CustomUserCreationForm(instance=user)
    return render(request, 'kessy/crud_user/edit_user.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('crud_user')
    return render(request, 'kessy/crud_user/delete_user.html', {'user': user})

@user_passes_test(lambda u: u.is_superuser)
def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'kessy/crud_user/view_user.html', {'user': user})




# CRUD views for recipes
@user_passes_test(lambda u: u.is_superuser)
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user  # Set the current user
            recipe.save()
            return redirect('crud_recipe')
    else:
        form = RecipeForm()
    return render(request, 'kessy/crud_recipe/create_recipe.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            edited_recipe = form.save(commit=False)
            edited_recipe.user = recipe.user  # Preserve the original user
            edited_recipe.save()
            return redirect('crud_recipe')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'kessy/crud_recipe/edit_recipe.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        recipe.delete()
        return redirect('crud_recipe')
    return render(request, 'kessy/crud_recipe/delete_recipe.html', {'recipe': recipe})

@user_passes_test(lambda u: u.is_superuser)
def view_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'kessy/crud_recipe/view_recipe.html', {'recipe': recipe})

@user_passes_test(lambda u: u.is_superuser)
def crud_recipe(request):
    recipes = Recipe.objects.all()
    return render(request, 'kessy/crud_recipe/list_recipes.html', {'recipes': recipes})



class ViewRecipeList(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'