from django.contrib import admin

from eCommerce.forms.userForms import UserAdmin
from .models import Post, User, Product, Category

# Register your models here.
admin.site.register(Post)

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(User)

