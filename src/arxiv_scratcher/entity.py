import requests
import json

class Paper:
    def __init__(self, title, abstract, url):
        self.title = title
        self.abstract = abstract
        self.url = url

    def get(self):
        dct = {}
        dct['title'] = self.title
        dct['abstract'] = self.abstract
        dct['url'] = self.url
        return dct

    def __str__(self):
        return self.get()

    def __name__(self):
        return self.get()


class ChatModel:

    def __init__(self, api):
        self.api = api

    def chat(self, question):

        url = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
        api_key = self.api  # 替换为你的 API 密钥

        # 设置请求头
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        # 设置请求数据
        data = {
            'model': 'glm-4-plus',
            'messages': [
                {
                    'role': 'user',
                    'content': question
                }
            ]
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()['choices'][0]['message']['content']
