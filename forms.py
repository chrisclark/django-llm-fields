from django import forms
from django.contrib import admin

from .choices import GPT_MODELS
from .models import GPTPrompt

admin.autodiscover()


class PromptPlaygroundForm(forms.Form):
    prompt = forms.ModelChoiceField(queryset=GPTPrompt.objects.all())
    system_prompt = forms.CharField(widget=forms.Textarea)
    human_prompt = forms.CharField(widget=forms.Textarea)
    model = forms.ChoiceField(choices=GPT_MODELS)
