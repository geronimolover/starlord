# (c) PR0FESS0R-99
from Config import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, TUTORIAL
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
from pyrogram.errors import UserNotParticipant
from LuciferMoringstar_Robot import get_filter_results, get_file_details, is_subscribed, get_poster
from LuciferMoringstar_Robot import RATING, GENRES, HELP, ABOUT
import random
from OMDB import get_movie_info
BUTTONS = {}
BOT = {}

@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    movie_name = message.text
    movie_info = get_movie_info(movie_name)
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📢Join Updates Channel📢", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        filter_mymes = f"**🗂️ Title:** {search}\n**⭐ Rating:** {random.choice(RATING)}\n**🎭 Genre:** {random.choice(GENRES)}\n**📤 Uploaded by {message.chat.title}**"
        mo_tech_yt = f"""📀 𝖳𝗂𝗍𝗅𝖾 : <b>{movie_info['title']}</b>
                            
⏱️ 𝖱𝗎𝗇𝗍𝗂𝗆𝖾 : <b>{movie_info['duration']}</b>
🌟 𝖱𝖺𝗍𝗂𝗇𝗀 : <b>{movie_info['imdb_rating']}/10</b>
🗳️ 𝖵𝗈𝗍𝖾𝗌 : <b>{movie_info['votes']}</b>

📆 𝖱𝖾𝗅𝖾𝖺𝗌𝖾 : <b>{movie_info['release']}</b>
🎭 𝖦𝖾𝗇𝗋𝖾 : <b>{movie_info['genre']}</b>
🎙 𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾 : <b>{movie_info['language']}</b>
🌐 𝖢𝗈𝗎𝗇𝗍𝗋𝗒 : <b>{movie_info['country']}</b>

🎥 𝖣𝗂𝗋𝖾𝖼𝗍𝗈𝗋𝗌 : <b>{movie_info['director']}</b>
📝 𝖶𝗋𝗂𝗍𝖾𝗋𝗌 : <b>{movie_info['writer']}</b>
🔆 𝖲𝗍𝖺𝗋𝗌 : <b>{movie_info['actors']}</b>

🗒 **Storyline** : <code>{movie_info['plot']}</code>"""
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"pr0fess0r_99#{file_id}")]
                    )
        else:
            await client.send_photo(
        chat_id=message.chat.id,
        photo="https://telegra.ph/file/86f4da717fc9ba639e469.png",
        caption=f"👋Hey {message.from_user.mention}\n\n👉If this movie is not in our database you will not get that movie..\n\n👉Otherwise, the spelling of the name of the requested movie may not be correct...\nSo you go to [Google](https://www.google.com/search?q={search}) and check the spelling of the name of the movie you want.\n\n👉Check if the movie is [released](https://www.google.com/search?q={search}+release+date)\n\n👉Or wait till the movie uploads",
        reply_to_message_id=message.message_id)
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_photo(photo="https://telegra.ph/file/8d4795557009f998c7b22.png", caption=filter_mymes, reply_markup=InlineKeyboardMarkup(buttons))
            if mo_tech_yt:
                await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await client.send_photo(
        chat_id=message.chat.id,
        photo="https://telegra.ph/file/86f4da717fc9ba639e469.png",
        caption=f"👋Hey {message.from_user.mention}\n\n👉If this movie is not in our database you will not get that movie..\n\n👉Otherwise, the spelling of the name of the requested movie may not be correct...\nSo you go to [Google](https://www.google.com/search?q={search}) and check the spelling of the name of the movie you want.\n\n👉Check if the movie is [released](https://www.google.com/search?q={search}+release+date)\n\n👉Or wait till the movie uploads",
        reply_to_message_id=message.message_id)
            return            

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="⏩CLICK FOR MORE RESULTS⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_photo(photo="https://telegra.ph/file/8d4795557009f998c7b22.png", caption=filter_mymes, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    movie_name = message.text
    movie_info = get_movie_info(movie_name)
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        mo_tech_yt = f"""📀 𝖳𝗂𝗍𝗅𝖾 : <b>{movie_info['title']}</b>
                            
⏱️ 𝖱𝗎𝗇𝗍𝗂𝗆𝖾 : <b>{movie_info['duration']}</b>
🌟 𝖱𝖺𝗍𝗂𝗇𝗀 : <b>{movie_info['imdb_rating']}/10</b>
🗳️ 𝖵𝗈𝗍𝖾𝗌 : <b>{movie_info['votes']}</b>

📆 𝖱𝖾𝗅𝖾𝖺𝗌𝖾 : <b>{movie_info['release']}</b>
🎭 𝖦𝖾𝗇𝗋𝖾 : <b>{movie_info['genre']}</b>
🎙 𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾 : <b>{movie_info['language']}</b>
🌐 𝖢𝗈𝗎𝗇𝗍𝗋𝗒 : <b>{movie_info['country']}</b>

🎥 𝖣𝗂𝗋𝖾𝖼𝗍𝗈𝗋𝗌 : <b>{movie_info['director']}</b>
📝 𝖶𝗋𝗂𝗍𝖾𝗋𝗌 : <b>{movie_info['writer']}</b>
🔆 𝖲𝗍𝖺𝗋𝗌 : <b>{movie_info['actors']}</b>

🗒 **Storyline** : <code>{movie_info['plot']}</code>"""
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=pr0fess0r_99_-_-_-_{file_id}")]
                )
        else:
            LuciferMoringstar=await client.send_photo(
        chat_id=message.chat.id,
        photo="https://telegra.ph/file/86f4da717fc9ba639e469.png",
        caption=f"👋Hey {message.from_user.mention}\n\n👉If this movie is not in our database you will not get that movie..\n\n👉Otherwise, the spelling of the name of the requested movie may not be correct...\nSo you go to [Google](https://www.google.com/search?q={search}) and check the spelling of the name of the movie you want.\n\n👉Check if the movie is [released](https://www.google.com/search?q={search}+release+date)\n\n👉Or wait till the movie uploads",
        reply_to_message_id=message.message_id)
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_photo(photo="https://telegra.ph/file/8d4795557009f998c7b22.png", caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="⏩CLICK FOR MORE RESULTS⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_photo(photo="https://telegra.ph/file/8d4795557009f998c7b22.png", caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ END OF THE RESULTS ⏪", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "help":
            buttons = [[
                InlineKeyboardButton('Channel', url='t.me/free_music123'),
                InlineKeyboardButton('Group', url="t.me/all_super_movies")
                ],[
                InlineKeyboardButton('💫Developer💫', url='t.me/geronimo1234')
                ]]
            await query.message.edit(text=f"{HELP}", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton('Developer', url='t.me/geronimo1234'),
                    InlineKeyboardButton('Group', url="t.me/all_super_movies")
                ]
                ]
            await query.message.edit(text=f"{ABOUT}".format(TUTORIAL), reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


        elif query.data.startswith("pr0fess0r_99"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('💫 DEVELOPER 💫', url="t.me/geronimo1234")
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('🖥️ Developer 🖥️', url="t.me/geronimo1234")
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("Dont touch it👀",show_alert=True)
