
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
from django.contrib import messages
from django.urls import reverse
from .forms import LostIDReportForm, ClaimRequestForm
from django.http import JsonResponse
import json
import folium
from wapiid.models import LostIDReport
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
import os
from django.core.mail import send_mail

# Create your views here.
# Home page
def home(request):
    return render(request, 'home.html')

# Base/Master
def index(request):
    return render(request, 'index.html')

#Become A Partner
def bap(request):
    return render(request, 'bap.html')

#Report a lost ID
def report(request):
    show_success = False
    if request.method == 'POST':
        form = LostIDReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            show_success = True
            form = LostIDReportForm()  # reset form
    else:
        form = LostIDReportForm()
    return render(request, 'report.html', {'form': form, 'show_success': show_success})

#Testing New page
def newhero(request):
    return render(request, 'newhero.html')

# Search for a lost ID
def search(request):
    query = request.GET.get('q')
    if query:
        results = LostIDReport.objects.annotate(
            search=SearchVector('full_name', 'id_number', 'lost_location', 'found_by', 'latitude', 'longitude', 'date_reported'),
        ).filter(search=query)
    else:
        results = LostIDReport.objects.none()

     # Initialize map
    folium_map = folium.Map(location=[-1.2921, 36.8219], zoom_start=6, tiles='https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
    attr='OpenStreetMap HOT')  

    # Add markers to map
    for report in results:
        if report.latitude and report.longitude:
            folium.Marker(
                location=[report.latitude, report.longitude],
                popup=f"{report.full_name} - {report.lost_location}",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(folium_map)

    # Convert map to HTML
    map_html = folium_map._repr_html_()

    return render(request, 'search.html', {
        'results': results,
        'folium_map': map_html,
    })

#Attempting an AJAX search - Failed :(
@csrf_exempt
def ajax_search(request):
    if request.method == "POST":
        data = json.loads(request.body)
        query = data.get("id_number")

        if query:
            results = LostIDReport.objects.annotate(
                search=SearchVector('full_name', 'id_number', 'lost_location', 'found_by'),
            ).filter(search=query)
        else:
            results = LostIDReport.objects.none()

        # Generate map
        folium_map = folium.Map(location=[-1.2921, 36.8219], zoom_start=6)
        for report in results:
            if report.latitude and report.longitude:
                folium.Marker(
                    location=[report.latitude, report.longitude],
                    popup=f"{report.full_name} - {report.lost_location}",
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(folium_map)

        # Convert to HTML
        map_html = folium_map._repr_html_()

        # Convert results to JSON
        result_list = []
        for r in results:
            result_list.append({
                "full_name": r.full_name,
                "id_number": r.id_number,
                "lost_location": r.lost_location,
                "status": getattr(r, "status", "Unknown")
            })

        return JsonResponse({
            "results": result_list,
            "map_html": map_html
        })
    return JsonResponse({"error": "Invalid request"}, status=400)

#Results pag edemo
def results(request):
    return render(request, 'results.html')

# Claim a lost ID
def claim(request):
    if request.method == 'POST':
        form = ClaimRequestForm(request.POST, request.FILES)
        if form.is_valid():
            claim_instance = form.save()

            # Get form data
            claimant_email = form.cleaned_data.get('contact_email')
            full_name = form.cleaned_data.get('claimant_name')

            # Map image CIDs to image file paths
            cid_map = {
                'image_1_cid': 'assety/img/email/image-1.png',
                'image_2_cid': 'assety/img/email/image-2.png',
                'image_3_cid': 'assety/img/email/image-3.png',
                'image_4_cid': 'assety/img/email/image-4.png',
                'image_5_cid': 'assety/img/email/image-5.png',
                'image_6_cid': 'assety/img/email/image-6.png',
            }

            # Pass the CIDs (keys) to the template
            context = {
                'full_name': full_name,
                **{cid: cid for cid in cid_map}
            }

            # Render email content
            html_content = render_to_string('confirmation_email.html', context)
            text_content = strip_tags(html_content)

            # Create the email
            email = EmailMultiAlternatives(
                subject='Lost ID Claim Confirmation',
                body=text_content,
                from_email='rebeccancovers@gmail.com',
                to=[claimant_email]
            )
            email.attach_alternative(html_content, "text/html")

            # Attach each image using CID
            for cid, path in cid_map.items():
                try:
                    with open(path, 'rb') as f:
                        img = MIMEImage(f.read())
                        img.add_header('Content-ID', f'<{cid}>')
                        img.add_header('Content-Disposition', 'inline', filename=os.path.basename(path))
                        email.attach(img)
                except FileNotFoundError:
                    print(f"⚠️ Image not found: {path}")

            email.send()

            return redirect(reverse('home') + '?claim_success=1')
    else:
        form = ClaimRequestForm()
    return render(request, 'claim.html', {'form': form})



 







