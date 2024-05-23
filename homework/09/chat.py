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
