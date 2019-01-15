from django.contrib import admin
from GameManager.models import Game, Profile


class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'id']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_superuser', ]


admin.site.register(Game, GameAdmin)
admin.site.register(Profile, ProfileAdmin)
