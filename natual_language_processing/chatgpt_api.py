# I exceeded my current quota

import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system"
        },
        {
            "role": "user",
            "content": "你知道怎麼使用OpenAI Python API嗎？",
        }
    ],
    model="gpt-3.5-turbo",
)


print(chat_completion.choices[0].message.content)
