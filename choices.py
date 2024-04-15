GPT4 = 0
GPT3 = 1

GPT_MODELS = (
    (GPT4, "gpt-4"),
    (GPT3, "gpt-3.5-turbo"),
)

# OpenAI does not have API endpoints to retrieve this data
# So we take the same approach as Langchain and hardcode it
# https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/llms/openai.py#L552
MODEL_SIZES = {
    "gpt-4": 8192,
    "gpt-3.5-turbo": 4096,
}
