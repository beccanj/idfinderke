from django import forms
from django.contrib.auth.models import User
from wapiid.models import LostIDReport



class LostIDReportForm(forms.ModelForm):
    class Meta:
        model = LostIDReport
        fields = ['full_name', 'id_number', 'document_type', 'lost_location', 'latitude', 'longitude', 'contact_email', 'found_by','scanned_image']
        