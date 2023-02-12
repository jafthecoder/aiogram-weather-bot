open_weather_token = '97de33ebc06b2cf40cedb47072964c01'
tg_token = '5759458877:AAHwRbDNvus8DtKQrC-OQpkB1PGwn_jHESs'

import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import  executor

bot = Bot(token=tg_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
 await message.reply('Hi! Enter the city name! In english plz)')


@dp.message_handler()
async def get_weather(message: types.Message):
        code_emoji = {
            'Clear': 'Clear \U00002600',
            'Clouds': 'Cloudy \U00002601',
            'Rain': 'Rainy \U00002614',
            'Drizzle': 'Drizzly \U00002614',
            'Snow': 'Snowy \U0001F328',
            'Mist': 'Foggy \U0001F32B'
        }
        try:
            r = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric")
            data = r.json()

            city = data['name']
            cur_weather = data['main']['temp']

            weather_desc = data['weather'][0]['main']
            if weather_desc in code_emoji:
                wd = code_emoji[weather_desc]
            else:
                wd = 'Look out the window yourself!)'

            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            wind = data['wind']['speed']
            sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
            sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])

            await message.reply(f"***{datetime.datetime.now().strftime('%d-%m-%Y  %H:%M')}***\n"
                  f"Weather in {city} city\nTemperature: {cur_weather} C° {wd}\n"
                  f"Humidity: {humidity}\nPressure: {pressure} mm_rt_st\nWind {wind} m/s\n"
                  f"Sunrise: {sunrise_timestamp}\nSunset: {sunset_timestamp}\n"

                  f"Have a nice day)")
        except:
            await message.reply('Check the city name !!!')

if __name__=='__main__':
    executor.start_polling(dp)