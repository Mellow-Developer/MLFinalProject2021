from django import forms
from auctions.models import Listing, Category


class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing

        fields = ('title', 'long_title', 'description', 'starting_price', 'image_url', 'cats')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your title here'}),
            'long_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a longer title here'}),
            'description': forms.Textarea(attrs={'class': 'form-control from-control-mod'}),
            'starting_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '100.00'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'cats': forms.Select(attrs={'class': 'form-control'})
        }
