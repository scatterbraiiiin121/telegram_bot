import telebot
import base
import app_api

bot= telebot.TeleBot(base.TOKEN)
print("bot created..")

@bot.message_handler(commands=['start'])
def say_hello(message):
    bot.send_message(message.chat.id, text='به بات خوش آمدید')

@bot.message_handler(commands=['help', 'contact'])
def support(message):

    markup = telebot.types.ReplyKeyboardRemove()

    bot.send_message(
        message.chat.id,
        text='''دستورات ربات:
        /start
        /news
        /menu
        /movie''')

@bot.message_handler(commands=['news'])
def show_news(message):
    try:
        markup= telebot.types.InlineKeyboardMarkup()
        btn1= telebot.types.InlineKeyboardButton(text='اخبار فیلم', url= 'https://collider.com/')
        btn2= telebot.types.InlineKeyboardButton(text='سایت IMDB', url= 'https://www.imdb.com/')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text='یکی از گزینه های زیر را انتخاب کنید', reply_markup=markup)
    except:
        bot.send_message(message.chat.id, text='اختلال در اتصال به نت', reply_markup=markup)

@bot.message_handler(commands=['menu'])
def show_menu(message):
    markup= telebot.types.ReplyKeyboardMarkup(row_width=1)
    btn1= telebot.types.KeyboardButton(text='تماس با ما')
    btn2= telebot.types.KeyboardButton(text='درباره ما')
    btn3= telebot.types.KeyboardButton(text='بازگشت')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text='یکی از گزینه های زیر را انتخاب کنید', reply_markup=markup)

@bot.message_handler(commands =['movie'])
def get_movie_step_one(message):
    msg = bot.send_message(message.chat.id, text='نام فیلم مورد نظر را وارد کنید:')
    bot.register_next_step_handler(msg, get_movie_info)

def get_movie_info(message):
    # print('hello')
    movie_name = message.text
    try:
        result = app_api.get_movie_by_name(movie_name)
        title = result[0]
        year = result[1]
        genres = result[2]
        imdb_rating = result[3]

        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton(
            text=f'{title} ({year})',
            callback_data=f'{title}|{year}|{genres}|{imdb_rating}'
        )
        markup.add(btn)
        bot.send_message(
            message.chat.id,
            text='یکی از نتایج زیر را انتخاب کنید:',
            reply_markup=markup
        )
    except:
        bot.send_message(message.chat.id, text='فیلم پیدا نشد.')

@bot.callback_query_handler(func=lambda message: True)
def callback(message):

    data = message.data.split('|')
    title = data[0]
    year = data[1]
    genres = data[2]
    imdb_rating = data[3]
    info = f'''title : {title}
year : {year}
genres : {genres}
imdb rate : {imdb_rating}
'''

    bot.send_message(message.message.chat.id, info)

@bot.message_handler(func= lambda message: True)
def answer_to_other_msg(message):
    if message.text == 'تماس با ما':
        mobile = '09169160052'
        email = 'tamanarabani123@gmail.com'
        info = f'mobile:{mobile}\n email: {email}'
        bot.send_message(message.chat.id, text = info)
    elif message.text == 'درباره ما':
         bot.send_message(message.chat.id, "این بات مربوط به فیلم است.")
    elif message.text == 'بازگشت':
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, text = "بازگشت به منوی اصلی", reply_markup=markup)

if __name__ == '__main__':
    bot.infinity_polling()