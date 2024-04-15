from django.forms.widgets import Textarea


class LLMTextAreaWidget(Textarea):
    template_name = "widgets/llm_text_area_widget.html"

    def __init__(self, req_url, *args, **kwargs):
        self.llm_req_url = req_url
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["llm_req_url"] = self.llm_req_url
        context["widget"]["btn_class"] = f"{name}-generate-btn"
        return context
