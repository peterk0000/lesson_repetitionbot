TOKEN = 'TOKEN'
LOGS = 'logs.txt'
assistant_content = 'Напомни тему: '
GPT_LOCAL_URL = 'http://localhost:1234/v1/chat/completions'
system_content = ("Ты - дружелюбный помощник для напоминания тем по школьным предметам. Вкратце напоминай тему на русском"
                  "языке. Не пиши никакой пояснительный текст от себя")
HEADERS = {"Content-Type": "application/json"}

MAX_TOKENS = 150

db_file = 'messages.db'
