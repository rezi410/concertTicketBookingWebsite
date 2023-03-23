from django.contrib import admin

from .models import GoldTicket,SliverTicket,BronzeTicket, Concert
# Register your models here.

admin.site.register(GoldTicket)
admin.site.register(SliverTicket)
admin.site.register(BronzeTicket)
admin.site.register(Concert)
