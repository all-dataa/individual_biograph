import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('minimax_api_key'), base_url="https://api.minimax.chat/v1")
# print(os.getenv('minimax_api_key'))

response = client.chat.completions.create(
  model="abab6.5s-chat",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "minimax ai这个公司支持可以将语音mp3文件转化成文本文件吗"}
  ],
  temperature=100,
  # stream=True
)

# for chunk in response:
#   print(chunk.choices)

print(response.choices[0].message.content)