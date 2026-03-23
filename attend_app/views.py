# attend_app/views.py
import datetime 
import csv
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.utils import timezone
from django.core import serializers
from .models import Worker, Attendance
from .form import AttendanceForm
import json

def index(request):
    today = timezone.now().date()
    context = {'today': today}

    if request.method == 'POST':
        # AJAX submission handling
        form = AttendanceForm(request.POST)
        if form.is_valid():
            worker = form.cleaned_data['worker']
            signature = form.cleaned_data['signature']
            existing = Attendance.objects.filter(worker=worker, date=today).first()
            if existing:
                return JsonResponse({'status': 'error', 'message': f"{worker.name} already attended today at {existing.check_in_time}"}, status=400)
            else:
                now = timezone.now()
                attendance = Attendance.objects.create(
                    worker=worker,
                    date=today,
                    check_in_time=now.time(),
                    signature=signature
                )
                # Return the new record data for immediate display
                return JsonResponse({
                    'status': 'success',
                    'message': f"Attendance recorded for {worker.name} at {now.strftime('%H:%M:%S')}.",
                    'record': {
                        'id': attendance.id,
                        'worker_name': worker.name,
                        'check_in_time': attendance.check_in_time.strftime('%H:%M:%S'),
                        'signature': signature,
                        'late': attendance.is_late()
                    }
                })
        else:
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({'status': 'error', 'message': 'Form invalid', 'errors': errors}, status=400)

    else:
        form = AttendanceForm()
        attendances = Attendance.objects.filter(date=today).order_by('check_in_time')
        context['form'] = form
        context['attendances'] = attendances
        return render(request, 'attend_app/index.html', context)

@require_GET
def attendance_data(request):
    """Return attendance records for a given date as JSON."""
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'error': 'Date parameter missing'}, status=400)
    try:
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    attendances = Attendance.objects.filter(date=date).order_by('check_in_time')
    data = []
    for idx, att in enumerate(attendances, start=1):
        data.append({
            'id': att.id,
            'serial': idx,
            'worker_name': att.worker.name,
            'check_in_time': att.check_in_time.strftime('%H:%M:%S'),
            'signature': att.signature,
            'late': att.is_late()
        })
    return JsonResponse({'attendances': data})

@require_POST
def delete_attendance(request, pk):
    """Delete an attendance record."""
    attendance = get_object_or_404(Attendance, pk=pk)
    attendance.delete()
    return JsonResponse({'status': 'deleted'})

@require_http_methods(['GET', 'POST'])
def edit_attendance(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'GET':
        data = {
            'id': attendance.id,
            'worker_name': attendance.worker.name,
            'check_in_time': attendance.check_in_time.strftime('%H:%M'),
            'signature': attendance.signature,
        }
        return JsonResponse(data)

    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            new_time = body.get('check_in_time')
            new_signature = body.get('signature')
            if new_time:
                try:
                    
                    attendance.check_in_time = datetime.time.fromisoformat(new_time)
                except ValueError:
                   
                    parts = new_time.split(':')
                    if len(parts) == 2:
                        hour, minute = map(int, parts)
                        attendance.check_in_time = datetime.time(hour, minute, 0)
                    elif len(parts) == 3:
                        hour, minute, second = map(int, parts)
                        attendance.check_in_time = datetime.time(hour, minute, second)
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Invalid time format'}, status=400)
            if new_signature is not None:
                attendance.signature = new_signature
            attendance.save()
            return JsonResponse({
                'status': 'updated',
                'record': {
                    'id': attendance.id,
                    'worker_name': attendance.worker.name,
                    'check_in_time': attendance.check_in_time.strftime('%H:%M:%S'),
                    'signature': attendance.signature,
                    'late': attendance.is_late()
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def export_csv(request):
    date_str = request.GET.get('date')
    if not date_str:
        return HttpResponse('Date parameter missing', status=400)
    try:
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponse('Invalid date format', status=400)

    attendances = Attendance.objects.filter(date=date).order_by('check_in_time')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="attendance_{date}.csv"'
    writer = csv.writer(response)
    writer.writerow(['S/N', 'Worker Name', 'Check-in Time', 'Signature', 'Status'])
    for idx, att in enumerate(attendances, start=1):
        status = 'Late' if att.is_late() else 'On Time'
        writer.writerow([idx, att.worker.name, att.check_in_time.strftime('%H:%M:%S'), att.signature, status])
    return response
