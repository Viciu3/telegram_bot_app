from flask import Flask, request, render_template, jsonify
import requests
import json
from database import init_db, add_user

app = Flask(__name__)

TOKEN = '7571425003:AAGEQEtLe3EM19NkEGLQ12Ruu4F_JPd6STM'  # Замените на токен вашего бота

init_db()  # Инициализируем базу данных

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    chat_id = update['message']['chat']['id']
    username = update['message']['chat'].get('username', 'Не указано')

    if update['message']['text'] == '/start':
        add_user(chat_id, username)  # Добавляем пользователя в базу данных
        send_message(chat_id, "Добро пожаловать! Это ваше мини-приложение.")
        send_menu(chat_id)  # Отправляем меню
        return jsonify({'status': 'ok'})
    
    return jsonify({'status': 'ok'})

@app.route('/send-message', methods=['POST'])
def send_message_to_user():
    data = request.get_json()
    username = data['username']
    message = data['message']

    chat_id = get_chat_id_by_username(username)
    if chat_id:
        send_message(chat_id, message)
        return jsonify({'response': 'Сообщение отправлено!'})
    else:
        return jsonify({'response': 'Пользователь не найден!'}), 404

def get_chat_id_by_username(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT chat_id FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    requests.post(url, data={'chat_id': chat_id, 'text': text})

def send_menu(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Опция 1", "callback_data": "option1"},
                {"text": "Опция 2", "callback_data": "option2"}
            ]
        ]
    }
    
    requests.post(url, data={
        'chat_id': chat_id,
        'text': "Выберите опцию:",
        'reply_markup': json.dumps(keyboard)
    })

if __name__ == '__main__':
    app.run(port=5000)