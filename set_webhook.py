import requests

TOKEN = '7571425003:AAGEQEtLe3EM19NkEGLQ12Ruu4F_JPd6STM'  # Замените на токен вашего бота
WEBHOOK_URL = 'https://<your-domain>/webhook'  # Замените <your-domain> на ваш домен или IP-адрес

response = requests.post(f'https://api.telegram.org/bot{TOKEN}/setWebhook', data={'url': WEBHOOK_URL})

print(response.json())