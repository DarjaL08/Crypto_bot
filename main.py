import telebot
from telebot import types
from Token import key
from Token import Coin_API
import requests

bot = telebot.TeleBot(key) 

bot = telebot.TeleBot(key)
API_KEY = 'Coin_API'  

def get_price(symbol, currency='USD'):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {
        'X-CMC_PRO_API_KEY': API_KEY
    }
    params = {
        'symbol': symbol,
        'convert': currency
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()['data'][symbol]
    price = data['quote'][currency]['price']
    change = data['quote'][currency]['percent_change_24h']
    return price, change


@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("💵 Курсы в USD", callback_data="usd"),
        types.InlineKeyboardButton("💶 Курсы в EUR", callback_data="eur")
    )
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! 👋\nВыбери валюту:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    currency = 'USD' if call.data == 'usd' else 'EUR'

    btc_price, btc_change = get_price('BTC', currency)
    eth_price, eth_change = get_price('ETH', currency)
    ltc_price, ltc_change = get_price('LTC', currency)

    trend_btc = "📈" if btc_change >= 0 else "📉"
    trend_eth = "📈" if eth_change >= 0 else "📉"
    trend_ltc = "📈" if ltc_change >= 0 else "📉"

    symbol = '$' if currency == 'USD' else '€'

    text = (
        f"🪙 Биткоин: {btc_price:.2f}{symbol} ({btc_change:.2f}%) {trend_btc}\n"
        f"🪙 Эфириум: {eth_price:.2f}{symbol} ({eth_change:.2f}%) {trend_eth}\n"
        f"🪙 Лайткоин: {ltc_price:.2f}{symbol} ({ltc_change:.2f}%) {trend_ltc}"
    )

    bot.send_message(call.message.chat.id, text)   

bot.polling(none_stop=True)
