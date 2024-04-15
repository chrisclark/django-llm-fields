import openai
from django.conf import settings
from django.core.cache import cache
from django.db import models

from core.db import CoreModel
from llm.choices import GPT3, GPT_MODELS, MODEL_SIZES

openai.api_key = settings.OPENAI_API_KEY


class GPTPrompt(object):
    system_message_template = models.TextField(blank=False)
    human_message_template = models.TextField(blank=False)
    key = models.CharField(blank=False, unique=True, max_length=100)
    model = models.IntegerField(choices=GPT_MODELS, default=GPT3)

    # Could be moved to DB-backed field if we want
    CACHE_EXPIRATION = 60 * 60 * 24 * 14  # Expire is two weeks. LLM tech moves fast!

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt_data = None

    def _max_tokens(self):
        return MODEL_SIZES.get(self.model_name, 0)

    def get_text(self):
        # Cache the result based on the prompt being sent to the LLM
        # Same prompts/messages = same result
        ms = self.messages()
        k = hash("".join([m["content"] for m in ms]))
        r = cache.get(k)
        if not r:
            try:
                resp = openai.ChatCompletion.create(model=self.model_name, messages=ms)
                r = resp["choices"][0]["message"]["content"].strip()
                cache.set(k, r, self.CACHE_EXPIRATION)
            except Exception as e:
                r = "Error: " + str(e)
        return r

    def messages(self):
        class SafeDict(dict):
            def __missing__(self, key):
                return "{" + key + "}"

        def format_string_safe(template, values):
            return template.format_map(SafeDict(values))

        return [{"role": i["role"], "content": format_string_safe(i["content"], self.prompt_data())} for i in self.prompt()]

    def prompt(self):
        return [{"role": "system", "content": self.system_message_template}, {"role": "user", "content": self.human_message_template}]

    @property
    def model_name(self):
        return GPT_MODELS[self.model][1]

    def __str__(self):
        return self.key
