from django.contrib import admin

from .models import GPTPrompt


class GPTPromptAdmin(admin.ModelAdmin):
    list_display = ("id", "key", "model", "system_message_template", "human_message_template")
    search_fields = ("key", "system_message_template", "human_message_template")
    list_filter = ("key",)

    def get_ordering(self, request):
        return ["key"]


admin.site.register(GPTPrompt, GPTPromptAdmin)
