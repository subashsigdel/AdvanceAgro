# everest_broker/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

received_data = []
from collections import deque

MAX_RECORDED_DATA = 10
received_data = deque(maxlen=MAX_RECORDED_DATA)

@csrf_exempt
def process_data(data):
    received_data.append(data)
@csrf_exempt
def receive_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(f"Received POST request on {request.path}: {data}")

            # Start a new thread to process the data concurrently
            process_data(data)

            # Send a confirmation response
            response_data = {'status': 'connected'}
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            response_data = {'error': 'Invalid JSON'}
            return JsonResponse(response_data, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def live_data(request):
    return render(request, 'live_data.html', {'received_data': received_data})
