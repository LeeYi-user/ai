from groq import Groq

while True:
    question = input("問題：")

    if question == "":
        continue

    client = Groq(
        api_key="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",
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="llama3-8b-8192",
    )

    print(chat_completion.choices[0].message.content)
