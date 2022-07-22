"""
RadioPlayerV3, Telegram Voice Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

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

import asyncio
from config import Config
from utils import USERNAME, mp
from pyrogram import Client, filters, emoji
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

msg=Config.msg
ADMINS=Config.ADMINS
CHAT_ID=Config.CHAT_ID
playlist=Config.playlist
LOG_GROUP=Config.LOG_GROUP

HOME_TEXT = "👋🏻 **Hi [{}](tg://user?id={})**,\n\nI'm **Radio Player V3.0** \nI Can Play Radio / Music / YouTube Live In Channel & Group 24x7 Nonstop. Made with ❤️ By @Rexxuxxxnx 😉!"
HELP_TEXT = """
💡 --**Setting Up**--:

\u2022 Add the bot and user account in your group with admin rights.
\u2022 Start a voice chat in your group & restart the bot if not joined to vc.
\u2022 Use /play [song name] or use /play as a reply to an audio file or youtube link.

💡 --**Common Commands**--:

\u2022 `/help` - shows help for all commands
\u2022 `/song` [song name] - download the song as audio
\u2022 `/current` - shows current track with controls
\u2022 `/playlist` - shows the current & queued playlist

💡 --**Admins Commands**--:

\u2022 `/radio` - Radionu başlat
\u2022 `/stopradio` - Canlı radionu dayandır
\u2022 `/skip` - mahnını keç
\u2022 `/join` - Məni səsli söhbətə dəvət et
\u2022 `/leave` - məni səsli söhbətdən çxart
\u2022 `/stop` - mahnını dayandır
\u2022 `/volume` - səs keyfiyyətini dəyişdir (0-200)
\u2022 `/replay` - play from the beginning
\u2022 `/clean` - remove unused raw files
\u2022 `/pause` - mahnını dayandır
\u2022 `/resume` - musiqi çalmağa davam edin
\u2022 `/mute` - mahnı səsini kəs
\u2022 `/unmute` - mahnı səsini aç
\u2022 `/restart` - botu yenidən başlat
\u2022 `/setvar` - set/change heroku configs

© **Powered By** : 
**@AsmSafone | @Alay57Chat** 👑
"""


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.from_user.id not in Config.ADMINS and query.data != "help":
        await query.answer(
            "You're Not Allowed! 🤣",
            show_alert=True
            )
        return

    if query.data.lower() == "replay":
        group_call = mp.group_call
        if not playlist:
            await query.answer("⛔️ Empty Playlist !", show_alert=True)
            return
        group_call.restart_playout()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} **Empty Playlist!**"
        else:
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.answer("🔂 Replaying !", show_alert=True)
            await query.edit_message_text(f"{pl}",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔄", callback_data="replay"),
                                InlineKeyboardButton("⏸", callback_data="pause"),
                                InlineKeyboardButton("⏩", callback_data="skip")
                            ],
                        ]
                    )
                )
        except MessageNotModified:
            pass

    elif query.data.lower() == "pause":
        if not playlist:
            await query.answer("⛔️ Empty Playlist !", show_alert=True)
            return
        else:
            mp.group_call.pause_playout()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.answer("⏸ Paused !", show_alert=True)
            await query.edit_message_text(f"{pl}",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔄", callback_data="replay"),
                                InlineKeyboardButton("▶️", callback_data="resume"),
                                InlineKeyboardButton("⏩", callback_data="skip")
                            ],
                        ]
                    )
                )
        except MessageNotModified:
            pass

    elif query.data.lower() == "resume":   
        if not playlist:
            await query.answer("⛔️ Empty Playlist !", show_alert=True)
            return
        else:
            mp.group_call.resume_playout()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.answer("▶️ Resumed !", show_alert=True)
            await query.edit_message_text(f"{pl}",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔄", callback_data="replay"),
                                InlineKeyboardButton("⏸", callback_data="pause"),
                                InlineKeyboardButton("⏩", callback_data="skip")
                            ],
                        ]
                    )
                )
        except MessageNotModified:
            pass

    elif query.data.lower() == "skip":   
        if not playlist:
            await query.answer("⛔️ Empty Playlist !", show_alert=True)
            return
        else:
            await mp.skip_current_playing()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.answer("⏩ Skipped !", show_alert=True)
            await query.edit_message_text(f"{pl}",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔄", callback_data="replay"),
                                InlineKeyboardButton("⏸", callback_data="pause"),
                                InlineKeyboardButton("⏩", callback_data="skip")
                            ],
                        ]
                    )
                )
        except MessageNotModified:
            pass

    elif query.data.lower() == "help":
        buttons = [
            [
                InlineKeyboardButton("SEARCH SONGS INLINE", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("ƏLAQƏ", url="https://t.me/Rexxuxxxnx"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/Alay57Chat"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://t.me/AsmSafone/173"),
                InlineKeyboardButton("SOURCE CODE", url="https://github.com/AsmSafone/RadioPlayerV3"),
            ],
            [
                InlineKeyboardButton("BACK HOME", callback_data="home"),
                InlineKeyboardButton("CLOSE MENU", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HELP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data.lower() == "home":
        buttons = [
            [
                InlineKeyboardButton("SEARCH SONGS INLINE", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/Alay57Chat"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/Alay57Chat"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://t.me/AsmSafone/173"),
                InlineKeyboardButton("SOURCE CODE", url="https://github.com/AsmSafone/RadioPlayerV3"),
            ],
            [
                InlineKeyboardButton("❔ HOW TO USE ❔", callback_data="help"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HOME_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data.lower() == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass

    await query.answer()



@Client.on_message(filters.command(["start", f"start@{USERNAME}"]))
async def start(client, message):
    buttons = [
            [
                InlineKeyboardButton("SEARCH SONGS INLINE", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/Alay57Chat"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/Alay57Chat"),
            ],
            [
                InlineKeyboardButton("DEVELOPER", url="https://t.me/Rexxuxxxnx"),
                InlineKeyboardButton("SOURCE CODE", url="https://github.com/AsmSafone/RadioPlayerV3"),
            ],
            [
                InlineKeyboardButton("❔ HOW TO USE ❔", callback_data="help"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    m=await message.reply_photo(photo="https://telegra.ph/file/4e839766d45935998e9c6.jpg", caption=HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await mp.delete(m)
    await mp.delete(message)


@Client.on_message(filters.command(["help", f"help@{USERNAME}"]))
async def help(client, message):
    buttons = [
            [
                InlineKeyboardButton("SEARCH SONGS INLINE", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("CHAT", url="https://t.me/Alay57Chat"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/Alay57Chat"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://t.me/AsmSafone/173"),
                InlineKeyboardButton("SOURCE CODE", url="https://github.com/AsmSafone/RadioPlayerV3"),
            ],
            [
                InlineKeyboardButton("BACK HOME", callback_data="home"),
                InlineKeyboardButton("CLOSE MENU", callback_data="close"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if msg.get('help') is not None:
        await msg['help'].delete()
    msg['help'] = await message.reply_photo(photo="https://telegra.ph/file/4e839766d45935998e9c6.jpg", caption=HELP_TEXT, reply_markup=reply_markup)
    await mp.delete(message)


@Client.on_message(filters.command(["setvar", f"setvar@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT_ID) | filters.private | filters.chat(LOG_GROUP)))
async def set_heroku_var(client, message):
    if not Config.HEROKU_APP:
        buttons = [[InlineKeyboardButton('HEROKU_API_KEY', url='https://dashboard.heroku.com/account/applications/authorizations/new')]]
        k=await message.reply_text(
            text="❗ **No Heroku App Found !** \n__Please Note That, This Command Needs The Following Heroku Vars To Be Set :__ \n\n1. `HEROKU_API_KEY` : Your heroku account api key.\n2. `HEROKU_APP_NAME` : Your heroku app name. \n\n**For More Ask In @AsmSupport !!**", 
            reply_markup=InlineKeyboardMarkup(buttons))
        await mp.delete(k)
        await mp.delete(message)
        return
    if " " in message.text:
        cmd, env = message.text.split(" ", 1)
        if  not "=" in env:
            k=await message.reply_text("❗ **You Should Specify The Value For Variable!** \n\nFor Example: \n`/setvar CHAT_ID=-1001313215676`")
            await mp.delete(k)
            await mp.delete(message)
            return
        var, value = env.split("=", 2)
        config = Config.HEROKU_APP.config()
        if not value:
            m=await message.reply_text(f"❗ **No Value Specified, So Deleting `{var}` Variable !**")
            await asyncio.sleep(2)
            if var in config:
                del config[var]
                await m.edit(f"🗑 **Sucessfully Deleted `{var}` !**")
                config[var] = None
            else:
                await m.edit(f"🤷‍♂️ **Variable Named `{var}` Not Found, Nothing Was Changed !**")
            return
        if var in config:
            m=await message.reply_text(f"⚠️ **Variable Already Found, So Edited Value To `{value}` !**")
        else:
            m=await message.reply_text(f"⚠️ **Variable Not Found, So Setting As New Var !**")
        await asyncio.sleep(2)
        await m.edit(f"✅ **Succesfully Set Variable `{var}` With Value `{value}`, Now Restarting To Apply Changes !**")
        config[var] = str(value)
        await mp.delete(m)
        await mp.delete(message)
        return
    else:
        k=await message.reply_text("❗ **You Haven't Provided Any Variable, You Should Follow The Correct Format !** \n\nFor Example: \n• `/setvar CHAT_ID=-1001313215676` to change or set CHAT var. \n• `/setvar REPLY_MESSAGE=` to delete REPLY_MESSAGE var.")
        await mp.delete(k)
        await mp.delete(message)
