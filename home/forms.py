from django import forms
from .models import MedicineTest

class TestMedicineForm(forms.ModelForm):
    class Meta:
        model = MedicineTest
        fields = "__all__"