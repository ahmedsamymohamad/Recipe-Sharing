from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    description = forms.CharField(
        # NOTE: styling in css probably would be a better practice
        widget=forms.Textarea(attrs={"style": "resize:none;"})
    )

    class Meta:
        model = Recipe
        fields = ["name", "image", "description", "difficulty", "ingredients"]
        help_texts = {
            "ingredients": "Select Ingredients  (Hold down the Ctrl (windows/linux)"
            " / Command (Mac) button to select multiple options.)",
        }
