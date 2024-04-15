For more information, see the corresponding [blog post](https://blog.untrod.com/2024/04/llm-chatgpt-powered-django-admin-fields.html).

## What is it?

This code will help you add buttons next to Django Admin text fields that will generate copy according to a specific prompt and data payload. For example, at [my company](https://www.grove.co) (an ecommerce site) we have a section on our product detail pages titled "Why we believe in this product", backed by an attribute on the Product model called why_we_believe. In the Django Admin, when viewing a Product model, there is a button that our merchandising team can use to populate the field.

![LLM-powered field in the Django Admin](https://blog.untrod.com/images/gpt-django-textarea.png)

The underlying prompts are editable in the admin as well so users can tweak the copy that ChatGPT is generating without getting in touch with engineering:

![Managing prompts in the Django Admin](https://blog.untrod.com/images/gpt-django-prompts.png)

And a playground area allows admin users to test the prompts out without leaving Django.

![Prompt playground area](https://blog.untrod.com/images/gpt-django-playground.png)

## How to use it yourself

First, the usual:

1. Install the app (adding `llm` to `INSTALLED_APPS` in settings)
2. Add a valid `OPENAI_API_KEY` to `settings`
3. Include llm/urls.py in your Django project
4. Run migrations

Then, create your own prompts, prompt data, urls, and register the widgets. The easiest way to do this is simply search for "TODO" in this repo. Examples are given in code for each step.
