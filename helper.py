import openai

openai.api_key = "api_key"


def ask_computer(prompt):
    res = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
    )
    return res["choices"][0]["text"]
