import json
import logging

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.views.generic import FormView
from rest_framework import viewsets

from .forms import PromptPlaygroundForm
from .models import GPTPrompt
from .serializers import GPTPromptSerializer

logger = logging.getLogger(__name__)
LEVER_CACHE_TIMEOUT = 4 * 60 * 60


@permission_required("product.change_product", raise_exception=True)
def generic_llm_prompt_view(request, promptDataCls=None):
    prompt = GPTPrompt.objects.get(key=promptDataCls.PROMPT_KEY)
    prompt.prompt_data = promptDataCls(request.GET.get("model_id"))
    return HttpResponse(json.dumps({"text": prompt.get_text()}), content_type="application/json")


class GPTPromptViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GPTPrompt.objects.all()
    serializer_class = GPTPromptSerializer


class LLMPromptPlayground(PermissionRequiredMixin, FormView):
    permission_required = ("can_use_prompts",)
    template_name = "llm_prompt_playground.html"
    form_class = PromptPlaygroundForm


def run_llm_prompt(request):
    if request.method == "POST":
        p = GPTPrompt(
            system_message_template=request.POST.get("system_prompt"),
            human_message_template=request.POST.get("human_prompt"),
            model=int(request.POST.get("model")),
        )
        p.prompt_data = lambda: {}
        return JsonResponse({"response_text": p.get_text().replace("/n", "<br>")})

    return JsonResponse({"error": "Invalid request"}, status=400)
