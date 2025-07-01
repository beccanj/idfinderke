from django import forms
from django.contrib.auth.models import User
from wapiid.models import LostIDReport, ClaimRequest



class LostIDReportForm(forms.ModelForm):
    class Meta:
        model = LostIDReport
        fields = ['full_name', 'id_number', 'document_type', 'lost_location', 'latitude', 'longitude', 'contact_email', 'found_by','scanned_image']




class ClaimRequestForm(forms.ModelForm):
    class Meta:
        model = ClaimRequest
        fields = ['found_id', 'claimant_name', 'contact_email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'cols': 80, 'rows': 4})
        }

        