import os
import telebot
from utils import *
from tabulate import tabulate

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Ciao a tutti, questo è un messaggio di intro stupido, se vuoi sapere cose intelligenti chiedi a /help")

# visualizza lista di comandi 
@bot.message_handler(commands=['help'])
def help(message):
    help_       = "\n/help : Aiuto mi stanno derubando e non mi ricordo più cosa fa questo bot"
    points      = "\n/points : Ahia, qualcuno sis ta per beccare dei punti deludenza"
    ranking     = "\n/ranking : vuoi sapere la classifica attuale per qualche championship? chiama il numero verde: 800900313prestitòincontanticelho!!!"
    oroscopo    = "\n/horoscope : scopri il tuo oroscopo di qualsiasi giorno. Perché? Boh, di solito alle ragazze piace" 
    end         = "\n\nPuoi contribuire a modificarmi sulLA repo: aggiungi_qui_repo"
    bot.reply_to(message, "Uè Uè, questi sono i comandi disponibili:" + help_ + points + ranking + oroscopo+)

#############
# HOROSCOPE #
#############
@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)


def day_handler(message):
    sign = message.text
    text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, fetch_horoscope, sign.capitalize())


def fetch_horoscope(message, sign):
    day = message.text
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Here's your horoscope!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")

##############
# ADD POINTS #
##############
@bot.message_handler(commands=['points'])
def championship_handler(message):
    text = "Oh wow! someone got some points!\nWhich is the championship?\n"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, player_handler)


def player_handler(message):
    championship = message.text
    text = "Which is the player?\n"
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, points_adder, championship.capitalize())


def points_adder(message, championship):
    player = message.text
    text = "How many points do you think he deserves?\n"
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, reason_adder, championship, player.capitalize())


def reason_adder(message, championship, player):
    points = int(message.text)
    text = "Whats the reason?\n"
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, fetch_championship, championship, player, points)


def fetch_championship(message, championship, player, points):
    reason = message.text
    ranking = push_championship(championship, player, points, reason).drop(columns=['championship'])
    #Human readable
    ranking = ranking.sort_index(ascending=False).head(5)
    ranking.index = list(range(1, len(ranking)+1))
    print(ranking)
    championship_message = f'*Championship * {championship}:\n'+ \
                            tabulate(ranking, headers='keys', tablefmt='psql')
    bot.send_message(message.chat.id, "Here's your championship status!")
    bot.send_message(message.chat.id, championship_message, parse_mode="Markdown")

###############
# GET RANKING #
###############
@bot.message_handler(commands=['ranking'])
def championship_ranking_handler(message):
    text = "You are gonna find out the ranking! What's the championship name?\n"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, show_ranking_handler)


def show_ranking_handler(message):
    championship = message.text
    text = "Here is the Ranking!\n{}".format(
                                tabulate(get_championship(championship), headers='keys', tablefmt='psql')
                            )
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")


bot.infinity_polling()
