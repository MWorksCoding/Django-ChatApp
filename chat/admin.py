from django.contrib import admin
from .models import Message, Chat

class MessageAdmin(admin.ModelAdmin):
    fields = ('chat', 'text','created_at','author', 'receiver')
    list_display = ('chat', 'text','created_at','author', 'receiver') # table view
    search_fields = ('text',) # browse table
# Decide which of the fields are displayed and in which order in the admin view, adding a search field

admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)