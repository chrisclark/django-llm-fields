from functools import partial

from django.urls import re_path

from llm.views import (
    GPTPromptViewSet,
    LLMPromptPlayground,
    generic_llm_prompt_view,
    run_llm_prompt,
)

urlpatterns = [
    re_path(r"^llm-prompt-playground/$", LLMPromptPlayground.as_view(), name="llm-prompt-playground"),
    re_path(
        r"^generate-review-summary/",
        partial(generic_llm_prompt_view, promptDataCls=ReviewSummaryPromptData),
        name="generate-review-summary",
    ),
    re_path(r"^api/run-llm-prompt/", run_llm_prompt, name="run-llm-prompt"),
    re_path(r"^api/gptprompt/(?P<pk>\d+)/$", GPTPromptViewSet.as_view({"get": "retrieve"}), name="get-gptprompt"),
]

# TODO update this for your endpoints
#from .prompt_data import BelievePromptData
#urlpatterns.append(
#    re_path(r"^generate-believe-text/", partial(generic_llm_prompt_view, promptDataCls=BelievePromptData), name="generate-believe-text")
#)
