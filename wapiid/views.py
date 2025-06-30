
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
from django.contrib import messages

from .forms import LostIDReportForm

from django.http import JsonResponse
import json
import folium
from wapiid.models import LostIDReport
from django.db.models import Q
# Create your views here.
def home(request):
    return render(request, 'home.html')


def index(request):
    return render(request, 'index.html')

def bap(request):
    return render(request, 'bap.html')

def report(request):
    if request.method == 'POST':
        form = LostIDReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Lost ID reported successfully.")
            return redirect('home')
    else:
        form = LostIDReportForm()
    return render(request, 'report.html', {'form': form})

def newhero(request):
    return render(request, 'newhero.html')

def search(request):
    query = request.GET.get('q')
    if query:
        results = LostIDReport.objects.annotate(
            search=SearchVector('full_name', 'id_number', 'lost_location', 'found_by', 'latitude', 'longitude', 'date_reported'),
        ).filter(search=query)
    else:
        results = LostIDReport.objects.none()

     # Initialize map
    folium_map = folium.Map(location=[-1.2921, 36.8219], zoom_start=6)  # Center on Kenya

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

def results(request):
    return render(request, 'results.html')





