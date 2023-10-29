import telebot
import json

token = '6269767469:AAHQBAndvR_9ix3u2biM-42EIYpguJ0Uy84'
bot = telebot.TeleBot(token)

def start_bot():
    bot.polling()

def save_state(state, filename):
    with open(filename, 'w') as file:
        json.dump(state, file)


def load_state(filename):
    try:
        with open(filename, 'r') as file:
            state = json.load(file)
            return state
    except FileNotFoundError:
        return {}


def add_chat_id(chat_id, state, filename):
    if 'chat_ids' in state:
        chat_ids = state['chat_ids']
        if chat_id not in chat_ids:
            chat_ids.append(chat_id)
            state['chat_ids'] = chat_ids
            save_state(state, filename)
    else:
        state['chat_ids'] = [chat_id]
        save_state(state, filename)

state = load_state('bot_state.json')
if 'chat_ids' in state:
    id_list = state['chat_ids']
else:
    id_list = []

@bot.message_handler(commands=['start'])
def main(message):
    chat_id = message.chat.id  # Получаем ID пользователя
    if chat_id not in id_list:  # Проверяем, не существует ли уже этот ID
        bot.send_message(chat_id, f'Добрый день! Вы добавлены к оповещению обнаружения оружия')
        id_list.append(chat_id)
        state['chat_ids'] = id_list
        save_state(state, 'bot_state.json')

@bot.message_handler(commands=['stop'])
def stop(message):
    chat_id = message.chat.id  # Получаем ID пользователя
    if chat_id in id_list:  # Проверяем, существует ли этот ID
        bot.send_message(chat_id, f'Вы удалены из оповещения обнаружения оружия')
        id_list.remove(chat_id)
        state['chat_ids'] = id_list
        save_state(state, 'bot_state.json')

if __name__ == "__main__":
    start_bot()