from django.http import JsonResponse
from .models import Event
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

@require_http_methods(["GET"])
def get_data(request):
    events = list(Event.objects.values())  # Get all events as dictionaries
    return JsonResponse(events, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def create_event(request):
    try:
        data = json.loads(request.body)
        if Event.objects.filter(name=data['name']).exists():
            return JsonResponse({'error': 'Event with the same name already exists'}, status=400)
        event = Event.objects.create(
            name=data['name'],
            start_time=data['starttime'],
            end_time=data['endtime'],
            location=data['location'],
            description=data['description'],
            category=data['category'],
            banner_image_url=data['bannerImage']
        )
        return JsonResponse({'message': 'Event created successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'error': 'Failed to create event', 'details': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        event.delete()
        return JsonResponse({'message': 'Event deleted successfully'})
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': 'Failed to delete event', 'details': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_event(request, event_id):
    try:
        data = json.loads(request.body)
        event = Event.objects.get(id=event_id)
        for field in ['name', 'starttime', 'endtime', 'location', 'description', 'category', 'bannerImage']:
            setattr(event, field, data[field])
        event.save()
        return JsonResponse({'message': 'Event updated successfully'})
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': 'Failed to update event', 'details': str(e)}, status=500)
