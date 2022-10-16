"""
RadioPlayerV3, Telegram Voice Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/Raviveyis>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import os
import sys
import asyncio
import subprocess
from time import sleep
from threading import Thread
from signal import SIGINT
from pyrogram import Client, filters, idle
from config import Config
from utils import mp, USERNAME, FFMPEG_PROCESSES
from pyrogram.raw.functions.bots import SetBotCommands
from pyrogram.raw.types import BotCommand, BotCommandScopeDefault
from user import USER
from pyrogram.types import Message
from pyrogram.errors import UserAlreadyParticipant

ADMINS=Config.ADMINS
CHAT_ID=Config.CHAT_ID
LOG_GROUP=Config.LOG_GROUP

bot = Client(
    "RadioPlayer",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins.bot")
)
if not os.path.isdir("./downloads"):
    os.makedirs("./downloads")
async def main():
    async with bot:
        await mp.start_radio()
        try:
            await USER.join_chat("@lovelesslifee")
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            print(e)
            pass

def stop_and_restart():
    bot.stop()
    os.system("git pull")
    sleep(10)
    os.execl(sys.executable, sys.executable, *sys.argv)


bot.run(main())
bot.start()
print("\n\nFast Music bot başladı, Qoşulun @lovelesslifee!")
bot.send(
    SetBotCommands(
        scope=BotCommandScopeDefault(),
        lang_code="en",
        commands=[
            BotCommand(
                command="start",
                description="Botu başlatmaq"
            ),
            BotCommand(
                command="help",
                description="Kömek Mesajını Gösterin"
            ),
            BotCommand(
                command="play",
                description="You Tube-den musiqi oxudun"
            ),
            BotCommand(
                command="song",
                description="Musiqini Audio Fayl Kimi Yükleyin"
            ),
            BotCommand(
                command="skip",
                description="Cari Musiqini Keçin"
            ),
            BotCommand(
                command="pause",
                description="Cari Musiqini Dayandırın"
            ),
            BotCommand(
                command="resume",
                description="Dayanmış Musiqini Başladın"
            ),
            BotCommand(
                command="radio",
                description="Radio / Canlı Yayımı başladın"
            ),
            BotCommand(
                command="current",
                description="Mövcud ifa olunan mahnını gösterin"
            ),
            BotCommand(
                command="playlist",
                description="Cari çalğı siyahısını gösterin"
            ),
            BotCommand(
                command="join",
                description="Sesli Çata qoşun"
            ),
            BotCommand(
                command="leave",
                description="Sesli Çatdan Ayırın"
            ),
            BotCommand(
                command="stop",
                description="Musiqini dayandır"
            ),
            BotCommand(
                command="stopradio",
                description="Radio / Canlı Yayımı dayandırın"
            ),
            BotCommand(
                command="replay",
                description="Başlanğıcdan Tekrar"
            ),
            BotCommand(
                command="clean",
                description="İstifade edilmemiş RAW PCM fayllarını temizleyin"
            ),
            BotCommand(
                command="mute",
                description="Sesli söhbetde userbotu susdur"
            ),
            BotCommand(
                command="unmute",
                description="Sesli söhbetde userbotun sesini aç"
            ),
            BotCommand(
                command="volume",
                description="Sesli Söhbet Sesini Deyişin"
            ),
            BotCommand(
                command="restart",
                description="Yenile & Botu Yeniden başlat (Yalnız Adminler Üçün)"
            ),
            BotCommand(
                command="setvar",
                description="Set / Change Configs Var (For Heroku)"
            )
        ]
    )
)

@bot.on_message(filters.command(["restart", f"restart@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT_ID) | filters.private | filters.chat(LOG_GROUP)))
async def restart(_, message: Message):
    k=await message.reply_text("🔄 **Checking ...**")
    await asyncio.sleep(3)
    if Config.HEROKU_APP:
        await k.edit("🔄 **Heroku Detected, \nRestarting Your App...**")
        Config.HEROKU_APP.restart()
    else:
        await k.edit("🔄 **Yeniden başlatmaq üçün gözleyin...**")
        process = FFMPEG_PROCESSES.get(CHAT_ID)
        if process:
            try:
                process.send_signal(SIGINT)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                print(e)
                pass
            FFMPEG_PROCESSES[CHAT_ID] = ""
        Thread(
            target=stop_and_restart()
            ).start()
    try:
        await k.edit("✅ **Uğurla yeniden başladıldı! \nYenileme üçün @lovelesslifee-a qoşulun!**")
        await k.reply_to_message.delete()
    except:
        pass

idle()
print("\n\nFast Music Bot Dayandı, Qoşulmaq üçün @lovelesslifee!")
bot.stop()
