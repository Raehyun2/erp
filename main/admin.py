from django.contrib import admin
from . models import Upload_Excel, Receipts_page, Issue_page, Stock_page

class ProductAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['user', 'product_name','product_number','remain_product','date']
    search_fields = ['user',]


admin.site.register(Upload_Excel)
admin.site.register(Receipts_page,ProductAdmin)
admin.site.register(Issue_page,ProductAdmin)
admin.site.register(Stock_page,ProductAdmin)
