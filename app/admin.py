from django.contrib import admin
from .models import BlogPost, Feedback, Comment, Product, CartItem

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'content')
    list_filter = ('published_date',)

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.username == 'admin'

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity_in_basket')
    search_fields = ('name',)
    list_filter = ('price',)

admin.site.register(BlogPost)
admin.site.register(Feedback)
admin.site.register(Comment)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)