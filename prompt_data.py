import json


class PromptData(object):
    PROMPT_KEY = None

    def __call__(self):
        return {}



# TODO: Simply an example; you will have to write your own
class BelievePromptData(PromptData):
    # The PROMPT_KEY will match whatever key you give the GPTPrompt you create via the admin
    PROMPT_KEY = "WHY_WE_BELIEVE_PROMPT"

    def __init__(self, model_id):
        from product.models import Product
        self.product = Product.objects.get(pk=model_id)

    def __call__(self):
        keys = ["name", "selling_points", "manufacturer_description", "ingredients"]
        return {"product_json": json.dumps({k: str(getattr(self.product, k)) for k in keys})}
