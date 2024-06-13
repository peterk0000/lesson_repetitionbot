import logging

import requests
from config import system_content, assistant_content, GPT_LOCAL_URL, HEADERS, MAX_TOKENS


class GPT:
    def __init__(self, system_content=system_content):
        self.system_content = system_content
        self.URL = GPT_LOCAL_URL
        self.HEADERS = HEADERS
        self.MAX_TOKENS = MAX_TOKENS
        self.assistant_content = "Решим задачу по шагам: "

    # Подсчитываем количество токенов в промте
    @staticmethod
    def count_tokens(prompt):
        tokens = len(prompt)
        return tokens

    # Проверка ответа на возможные ошибки и его обработка
    def process_resp(self, response: object) -> [bool, str]:
        # Проверка статус кода
        if response.status_code < 200 or response.status_code >= 300:
            return False, f"Ошибка: {response.status_code}"

        # Проверка json
        try:
            full_response = response.json()
        except:
            return False, "Ошибка получения JSON"

        # Проверка сообщения об ошибке
        if "error" in full_response or 'choices' not in full_response:
            return False, f"Ошибка: {full_response}"

        # Результат
        result = full_response['choices'][0]['message']['content']

        # Пустой результат == объяснение закончено
        if result == "":
            return True, "Конец объяснения"

        return True, result

    # Формирование промта
    def make_promt(self, text):
        json = {
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": text},
                {"role": "assistant", "content": assistant_content}
            ],
            "temperature": 1.2,
            "max_tokens": self.MAX_TOKENS,
        }
        return json

    # Отправка запроса
    def send_request(self, json):
        try:
            resp = requests.post(url=self.URL, headers=self.HEADERS, json=json)
            return resp
        except Exception as e:
            logging.error(e)
