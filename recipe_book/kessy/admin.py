from django.contrib import admin
from .models import User, Recipe, Category
from django.shortcuts import render


admin.site.site_header = 'Recipe Book Administration'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

try:
    admin.site.unregister(Recipe)
except admin.sites.NotRegistered:
    pass

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'description')

admin.site.register(Recipe, RecipeAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)



def admin_panel(request):
    testimonials = [
        {"name": "John Doe", "text": "The recipes are amazing and easy to follow!"},
        {"name": "Jane Smith", "text": "I love the variety of dishes. My go-to for meal ideas!"},
        {"name": "Emily Johnson", "text": "Beautifully photographed and delicious recipes. Highly recommend!"}
    ]
    return render(request, 'kessy/admin_panel.html', {'testimonials': testimonials})

