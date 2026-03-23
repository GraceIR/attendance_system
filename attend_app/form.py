from django import forms
from .models import Attendance, Worker

class AttendanceForm(forms.ModelForm):
    worker = forms.ModelChoiceField(queryset=Worker.objects.all(), empty_label="Select worker")
    signature = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Signature / Name'}))

    class Meta:
        model = Attendance
        fields = ['worker', 'signature']