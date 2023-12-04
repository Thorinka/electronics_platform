from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.translation import ngettext

from electronics.models import NetworkNode


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'creation_time', 'supplier_link', 'hierarchy_level', 'debt',)
    list_filter = ('city',)
    actions = ['nullify_debt']

    @admin.action(description="Set debt to '0'")
    def nullify_debt(self, request, queryset):
        updated = queryset.update(debt="0")
        self.message_user(
            request,
            ngettext(
                "%d debt was successfully nullified.",
                "%d debts were successfully nullified.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    def supplier_link(self, obj):
        if obj.supplier:
            url = f'/admin/electronics/networknode/{obj.supplier.id}/change/'
            return format_html('<a href="{}">{}</a>', url, obj.supplier)
        else:
            return None

    supplier_link.short_description = 'Supplier'

    def get_display_links(self, request, list_display):
        """
        Переопределяем метод, чтобы сделать ссылками только столбцы НАЗВАНИЕ и SUPPLIER.
        """
        display_links = super().get_display_links(request, list_display)
        if 'name' in list_display:
            return ['name']
        elif 'supplier_link' in list_display:
            return ['supplier_link']
        return display_links
