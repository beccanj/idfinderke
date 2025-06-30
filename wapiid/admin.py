from django.contrib import admin

# Register your models here.
from django.contrib import admin
from wapiid.models import LostIDReport, ClaimRequest, Partner

admin.site.site_header='ID Tracker '
admin.site.site_title='Kenyas 1st ID Tracker'


class LostIDReportAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'id_number', 'document_type', 'lost_location', 'contact_email', 'found_by', 'scanned_image', 'date_reported')
    search_fields = ('full_name', 'id_number', 'document_type', 'lost_location', 'contact_email', 'found_by', 'scanned_image', 'date_reported')
    list_filter = ['full_name']
    ordering = ['-date_reported']


class ClaimRequestAdmin(admin.ModelAdmin):
    list_display = ('found_id', 'claimant_name', 'contact_email', 'message', 'status', 'date_requested')
    search_fields = ('found_id', 'claimant_name', 'contact_email', 'message', 'status', 'date_requested')
    list_filter = ['found_id']
    ordering = ['-date_requested']


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact_person', 'phone_number', 'contact_email', 'type', 'logo')
    search_fields = ('name', 'location', 'contact_person', 'phone_number', 'contact_email', 'type', 'logo')
    list_filter = ['name']
    ordering = ['-name']



admin.site.register(LostIDReport, LostIDReportAdmin)
admin.site.register(ClaimRequest, ClaimRequestAdmin)
admin.site.register(Partner, PartnerAdmin)

 