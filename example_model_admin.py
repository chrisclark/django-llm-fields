#TODO: An example of how to hook the widget into the modeladmin
# You would do something similar in your existing admin.py file

from django.contrib import admin
from django import forms
from llm.widgets import LLMTextAreaWidget

from models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = "__all__"
        # Configure the widget to point to the endpoint you made in urls.py
        widgets = {
            "why_we_believe": LLMTextAreaWidget(req_url="/llm/generate-believe-text/"),
        }


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm

admin.site.register(Product, ProductAdmin)
