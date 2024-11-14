from django.contrib import admin

from .models import StrategyPost

class StrategyPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title' )

    list_display_links = ('id', 'title')

admin.site.register(StrategyPost, StrategyPostAdmin)

# Register your models here.
