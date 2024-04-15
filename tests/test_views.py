import json
from unittest.mock import patch

from django.conf import settings
from django.test import RequestFactory, TestCase

from llm.models import GPT3, GPTPrompt
from llm.prompt_data import BelievePromptData, ReviewSummaryPromptData
from product.tests.factories import ProductFactory
from pypantry.tests.factories import CustomerFactory


class ViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomerFactory(email="test@test.com", is_staff=True)
        self.customer = CustomerFactory(is_superuser=True, is_staff=True)
        self.client.login(username=self.customer.email, password=settings.CUSTOMER_PASSWORD)

    @patch("llm.models.openai.ChatCompletion.create")
    def test_believe_text_view(self, mock_chat_openai):
        mock_chat_openai.return_value = {"choices": [{"message": {"content": "Mocked Text"}}]}

        GPTPrompt(key=BelievePromptData.PROMPT_KEY).save()

        # Assuming there's a product with id 1 in the database
        p1 = ProductFactory()
        response = self.client.get("/llm/generate-believe-text/?model_id=" + str(p1.id))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"text": "Mocked Text"})

    @patch("llm.models.openai.ChatCompletion.create")
    @patch("llm.prompt_data.Product.get_top_helpful_reviews")
    def test_review_summary_view(self, mocked_reviews, mock_chat_openai):
        mock_chat_openai.return_value = mock_chat_openai.return_value = {"choices": [{"message": {"content": "Mocked Text"}}]}
        mocked_reviews.return_value = [{"Title": "foo", "ReviewText": "bar"}]

        GPTPrompt(key=ReviewSummaryPromptData.PROMPT_KEY).save()

        # Assuming there's a product with id 1 in the database
        p1 = ProductFactory()
        response = self.client.get("/llm/generate-review-summary/?model_id=" + str(p1.id))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"text": "Mocked Text"})

    def test_llm_prompt_playground_view(self):
        response = self.client.get("/llm/llm-prompt-playground/")
        self.assertEqual(response.status_code, 200)

    @patch("llm.models.openai.ChatCompletion.create")
    def test_run_llm_prompt_view(self, mock_chat_openai):
        mock_chat_openai.return_value = mock_chat_openai.return_value = {"choices": [{"message": {"content": "Mocked Text"}}]}
        response = self.client.post(
            "/llm/api/run-llm-prompt/",
            data={
                "system_prompt": "Hello, {name}!",
                "human_prompt": "Hi, bot!",
                "model": GPT3,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"response_text": "Mocked Text"})

    def test_gpt_prompt_view_set(self):
        GPTPrompt(system_message_template="foo", human_message_template="bar", model=GPT3, key="key").save()
        gpt = GPTPrompt.objects.get(key="key")
        response = self.client.get("/llm/api/gptprompt/" + str(gpt.id) + "/")
        self.assertEqual(json.loads(response.content)["data"]["id"], str(gpt.id))
        self.assertEqual(response.status_code, 200)
