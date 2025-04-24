from django import forms
from .models import Review, Recipe

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'image']
        labels = {
            'title': 'Recipe Title',
            'description': 'Description',
            'ingredients': 'Ingredients',
            'instructions': 'Instructions',
            'image': 'Recipe Image',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }  