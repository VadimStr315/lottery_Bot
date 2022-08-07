import telebot
from telebot import types
from time import sleep
from instaloader import Instaloader, Profile, Post , exceptions
from itertools import islice
import random
import json

def partition(l, size):
    for i in range(0, len(l), size):
        yield list(islice(l, i, i + size))

bot = telebot.TeleBot("")

global admin_list
admin_list=[]
509829521
global login
login='admin'
global password
password='password'

global winner

# data=(
#     {
#         "509829521":{
#             "admin_login": "admin",
#             "admin_password": "password",
#             "inst_login": "_.Strela._",
#             "inst_password": "МфвшьлфШЕ1006"},
#       },
#       )

# def read_data():
#     with open('data.json') as f:
#       data_json=json.load(f)
#     return data_json

# def write_data(data,file):
#     pass

# def save_data(data,file):
#     pass



@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    command_1 = types.KeyboardButton(text="/login_inst",  )
    command_2 = types.KeyboardButton(text="/start_lottery")
    keyboard.add(command_1,command_2)
    bot.send_message(message.chat.id, "Привествую",reply_markup=keyboard)

# админка
# -------------------------------------------------------------------------------------------
@bot.message_handler(commands=["admin"])
def admin(message):
    if message.from_user.id in admin_list:
        bot.send_message(message.chat.id, "Вы уже авторизованы")
        sleep(5)
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id-1)
    else:
        msg=bot.send_message(message.chat.id, "Логин:")
        bot.register_next_step_handler(msg,admin_login)


def admin_login(message):
    if login!=message.text:
        msg=bot.send_message(message.chat.id, "Неверный логин!Введите повторно:")
        bot.register_next_step_handler(msg, admin_login)
    else:
        msg=bot.send_message(message.chat.id, "Пароль:")
        bot.register_next_step_handler(msg, admin_password)


def admin_password(message):
    if password!=message.text:
        msg=bot.send_message(message.chat.id, "Неверный пароль!Введите повторно:")
        bot.register_next_step_handler(msg, admin_password)
    else:
        bot.send_message(message.chat.id, "Вы авторизованы. С чего начнем?\n\nп.с.Сообщения о авторизации удалятся через 5 секунды")
        sleep(5)
        bot.delete_message(message.chat.id, message.message_id+1)
        admin_list.append(message.from_user.id)
        print(admin_list)
        for i in range(5):
            bot.delete_message(message.chat.id, message.message_id-i)


@bot.message_handler(commands=['choose_winner'])
def choose_winner(message):
    if message.from_user.id in admin_list:
        winner=bot.send_message(message.chat.id,"Введите ник:")
        bot.register_next_step_handler(winner,save_winner)


def save_winner(message):
    global winner
    winner=message.text
    bot.send_message(message.chat.id,"Выбор сохранен")
    bot.delete_message(message.chat.id, message.message_id+1)
    for i in range(3):
            bot.delete_message(message.chat.id, message.message_id-i)
# -------------------------------------------------------------------------------------------


# авторизация в instagram
# -------------------------------------------------------------------------------------------
@bot.message_handler(commands=['login_inst'])
def inst_auth(message):
    msg=bot.send_message(message.chat.id,"Введите логин:")
    bot.register_next_step_handler(msg,login_inst)

def login_inst(message):
    # if message.from_user.id in admin_list:
    global inst_login
    inst_login=message.text
    msg=bot.send_message(message.chat.id,"Введите пароль:")
    bot.register_next_step_handler(msg,password_inst)


def password_inst(message):
    bot.send_message(message.chat.id,"Давайте пароль я пока спрячу")
    bot.delete_message(message.chat.id, message.message_id)
# if message.from_user.id in admin_list:
    global inst_password
    inst_password=message.text
    print(f"\n\nВаш логин:{inst_login}\nВаш пароль:{inst_password}\n\n")
    bot.send_message(message.chat.id,"Проверка данных..🤓\nЭто может занять какое-то время...")
    global L
    L = Instaloader()
    try:
        L.login(inst_login, inst_password)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        command_1 = types.KeyboardButton(text="/start_lottery")
        keyboard.add(command_1)
        bot.send_message(message.chat.id,f'Вы успешно авторизованы',reply_markup=keyboard)
    except exceptions.BadCredentialsException:
        bot.send_message(message.chat.id,'❌Не верно введен логин или пароль❌')
    except exceptions.ConnectionException:
        bot.send_message(message.chat.id,'❌Нет связи с Instagram❌')

#розыгрыш
# -------------------------------------------------------------------------------------------
@bot.message_handler(commands=['start_lottery'])
def start_lottery(message):
    # if message.from_user.id in admin_list:
    msg=bot.send_message(message.chat.id,f'Введите ссылку на пост:')
    bot.register_next_step_handler(msg,lottery_admin)


def lottery_admin(message):
    bot.send_message(message.chat.id,f'Считываю данные...')
    global total_amount
    total_amount=1
    global list_of_users
    list_of_users=list()
    global list_of_likers
    list_of_likers=list()
    global winner_number
    winner_number=0
    post_id=message.text
    post_id=(str(post_id).split('/'))[-2]
    post = Post.from_shortcode(L.context, post_id)
    post_likes = post.get_likes()
    post_comments = post.get_comments()
    j=0
    # for comment in post_comments:
    #     print(comment.owner.username)
    # sorting--------------------------------------------------------------
    # for like in post_likes:
    #     list_of_likers.append(str(like.username))
    # --------------------------------------------------------------------
    for comment in post_comments:
        j+=1
        username=str(comment.owner.username)
        list_of_users.append(username)
    user_winner_username=''
    user_winner_number=random.randint(1,total_amount)
    total_amount=len(list_of_users)
    bot.send_message(message.chat.id,'Скачиваем список участников...🧐')
    bot.send_message(message.chat.id,"Cписок участников сохранен")
    bot.send_message(message.chat.id,"Список участников:")
    string=''
    i=0
    list_of_lists=list(partition(list_of_users,15))
    for small_list in list_of_lists:
        for el in small_list:
            i+=1
            # if i==user_winner_number:
            #     user_winner_username=el
            if username==winner:
                winner_number=j
            string+=str(el)+'\n'
        sleep(1)
        bot.send_message(message.chat.id,string)
        string=''
    bot.send_message(message.chat.id,"Выбираем победителя...")
    if message.from_user.id in admin_list:
        bot.send_message(message.chat.id,f"Победитель: Под номером:{winner_number} - {winner}")
    else:
        bot.send_message(message.chat.id,f"Победитель: Под номером:{user_winner_number} - {user_winner_username}")

# -------------------------------------------------------------------------------------------





if __name__ == '__main__':
    bot.infinity_polling()