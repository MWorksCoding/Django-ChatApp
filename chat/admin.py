from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    fields = ('chat','text','created_at','author')
    list_display = ('text','created_at','author')
    search_fields = ('text',)
# Decide which of the fields are displayed and in which order in the admin view, adding a search field

admin.site.register(Message)