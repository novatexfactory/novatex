from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import NewsletterSubscriber
from .models import ContactMessage

class SubscriberAdmin(ModelAdmin):
    model = NewsletterSubscriber
    menu_label = 'Subscribers'
    menu_icon = 'mail'
    list_display = ('email', 'created_at')
    search_fields = ('email',)

modeladmin_register(SubscriberAdmin)

class ContactMessageAdmin(ModelAdmin):
    model = ContactMessage
    menu_label = 'Contact Messages'
    menu_icon = 'form'
    # Добавляем 'phone' в список отображаемых полей
    list_display = ('subject', 'name', 'email', 'phone', 'created_at') 
    # Позволяем искать по номеру телефона
    search_fields = ('subject', 'name', 'email', 'phone')

modeladmin_register(ContactMessageAdmin)