from django.contrib import admin

from .models import StrategyPost, Tweet, Reply

class StrategyPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title' )

    list_display_links = ('id', 'title')

admin.site.register(StrategyPost, StrategyPostAdmin)
admin.site.register(Tweet)
admin.site.register(Reply)
# Register your models here.
