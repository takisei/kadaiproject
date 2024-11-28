from django.contrib import admin

from .models import Category, KadaiPost

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    
    list_display_links=('id','title')

class KadaiPostAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    
    list_display_links = ('id','title')
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(KadaiPost, KadaiPostAdmin)