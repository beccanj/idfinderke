from django.db import models

# Create your models here.

class LostIDReport(models.Model):
    full_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20)
    document_type = models.CharField(
        max_length=50,
        choices=[
            ('ID', 'ID Card'),
            ('Passport', 'Passport'),
            ('License', 'Driving License'),
        ]
    )
    lost_location = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    contact_email = models.EmailField()
    found_by = models.CharField(max_length=100)
    scanned_image = models.ImageField(upload_to='lost_ids/')
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.document_type}"
    

    
class ClaimRequest(models.Model):
    found_id = models.ForeignKey(LostIDReport, on_delete=models.CASCADE)
    claimant_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    message = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim by {self.claimant_name} for {self.found_id}"
    

class Partner(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    contact_email = models.EmailField()
    type = models.CharField(max_length=50, choices=[('collector', 'Collector'), ('sponsor', 'Sponsor')])
    logo = models.ImageField(upload_to='partners/', null=True, blank=True)

    def __str__(self):
        return self.name
    


