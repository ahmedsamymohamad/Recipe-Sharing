from django.forms import ModelForm

from interactions.models import Rate


class RateForm(ModelForm):
    class Meta:
        model = Rate
        fields = ["rate"]
