from django.contrib import admin
from app.models import Customer, User,Analysis,Item,VAT,SYSTEM_SEQCONTRL,Currency,SYSTEM_MAIN,SYSTEM_BANK

admin.site.register(SYSTEM_SEQCONTRL)
admin.site.register(SYSTEM_MAIN)
admin.site.register(SYSTEM_BANK)
admin.site.register(Currency)
admin.site.register(Customer)
admin.site.register(Analysis)
admin.site.register(Item)
admin.site.register(VAT)


