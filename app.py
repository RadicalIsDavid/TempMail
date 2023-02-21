import os
import asyncio
import requests
import random
import bs4

from pykeyboard import InlineKeyboard
from pyrogram.errors import UserNotParticipant
from pyrogram import filters, Client
from RandomWordGenerator import RandomWord
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid, bad_request_400


from database import (
    get_served_users,
    add_served_user,
    remove_served_user,
    get_served_chats,
    add_served_chat,
    remove_served_chat
)

app = Client(
    "TempMail",
    api_hash= os.environ["API_HASH", "9d83e9bc46cab0c6793faebbd324d4e3"],
    api_id= int(os.environ["API_ID", "28422427"]),
    bot_token=os.environ["BOT_TOKEN", "5946644994:AAGUXVFDAEVEC8NJHG2GosiBED2lPf3wyrs"]
)

CHANNEL_ID = int(os.environ['CHANNEL_ID', "-1001593849748"])
CHANNEL = os.environ['CHANNEL', "@ROCKS_ROBOTS"]
OWNER = int(os.environ['OWNER', "5210727648"])

start_text = """
ʜᴇʟʟᴏ {} , ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴛᴇᴍᴘ ᴍᴀɪʟ ʙᴏᴛ

ᴏɴ ᴛʜɪs ʙᴏᴛ ʏᴏᴜ ᴄᴀɴ ᴄʀᴇᴀᴛᴇ ᴀ ᴛᴇᴍᴘᴏʀᴀʀʏ (ᴅɪsᴘᴏsᴀʙʟᴇ) ᴇᴍᴀɪʟ ɪɴ ᴀ sᴇᴄᴏɴᴅ, ᴛʜᴀᴛ sᴇʟғ-ᴅᴇsᴛʀᴜᴄᴛs ᴀғᴛᴇʀ sᴏᴍᴇ ᴛɪᴍᴇ. sᴛᴀʏ sᴀғᴇ, ᴀᴠᴏɪᴅ sᴘᴀᴍ - ᴛᴀᴋᴇ ᴄᴀʀᴇ ᴏғ ʏᴏᴜʀ ᴀɴᴏɴʏᴍɪᴛʏ. ʏᴏᴜ ᴄᴀɴ sᴇʟᴇᴄᴛ ғʀᴏᴍ ᴍᴀɴʏ ᴅᴏᴍᴀɪɴs

sᴇɴᴅ /new ᴛᴏ sᴇᴛ-ᴜᴘ ʏᴏᴜʀ ᴍᴀɪʟʙᴏx! """
start_button = InlineKeyboardMarkup(
            [[
                    InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url="https://t.me/frienddd_zoneee"),
                    InlineKeyboardButton("ɴᴇᴡs ᴄʜᴀɴɴᴇʟ", url="https://t.me/ROCKS_ROBOTS")
            ]])
fsub_text = """
**ᴀᴛᴛᴇɴᴛɪᴏɴ !**

ʏᴏᴜ sᴇᴇ ᴛʜɪs ᴍᴇssᴀɢᴇ ʙᴇᴄᴀᴜsᴇ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ:
@ROCKS_ROBOTS

ɪᴛ ɪs ɪᴍᴘᴏʀᴛᴀɴᴛ ᴛʜᴀᴛ ʏᴏᴜ ᴀʀᴇ ᴜᴘ ᴛᴏ ᴅᴀᴛᴇ ᴡɪᴛʜ ᴛʜᴇ ʟᴀᴛᴇsᴛ ᴜᴘᴅᴀᴛᴇs ᴀɴᴅ ᴀᴡᴀʀᴇ ᴏғ ᴛʜᴇ ʙʀᴀɴᴅ ɴᴇᴡ ғᴜɴᴄᴛɪᴏɴᴀʟɪᴛʏ. """


async def get_user(message):
    ok = True
    try:
        await message._client.get_chat_member(CHANNEL_ID, message.from_user.id)
        ok = True
    except UserNotParticipant:
        ok = False
    return ok 

@app.on_message(filters.command("start"))
async def start(_, message: Message):
    if not await get_user(message):   
        return await app.send_message(
			chat_id=message.from_user.id,
			text=fsub_text) 
    name = message.from_user.id
    await app.send_message(
    name,
    text = start_text.format(message.from_user.mention),
    reply_markup = start_button)
    return await add_served_user(message.from_user.id) 
    
#********************************************************************************
API1='https://www.1secmail.com/api/v1/?action=getDomainList'
API2='https://www.1secmail.com/api/v1/?action=getMessages&login='
API3='https://www.1secmail.com/api/v1/?action=readMessage&login='
#********************************************************************************

create = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Rocks Bots 🇮🇳", url="https://t.me/ROCKS_ROBOTS")]])

#********************************************************************************
@app.on_message(filters.command("new"))
async def fakemailgen(_, message: Message):
    name = message.from_user.id
    m =  await app.send_message(name,text=f"ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...",reply_markup = create)
    rp = RandomWord(max_word_size=8, include_digits=True)
    email = rp.generate()
    xx = requests.get(API1).json()
    domain = random.choice(xx)
    #print(email)
    mes = await app.send_message(
    name, 
    text = f"""
**📬ᴅᴏɴᴇ,ʏᴏᴜʀ ᴇᴍᴀɪʟ ᴀᴅᴅʀᴇss ᴄʀᴇᴀᴛᴇᴅ!**
📧 **ᴇᴍᴀɪʟ** : `{email}@{domain}`
📨 **ᴍᴀɪʟ ʙᴏx** : `empty`
**ᴘᴏᴡᴇʀᴇᴅ ʙʏ** : @ROCKS_ROBOTS """,
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔰Update Mail Box🔰", callback_data = f"mailbox |{email}|{domain}")]]))
    pi = await mes.pin(disable_notification=True, both_sides=True)
    await m.delete()
    await pi.delete()

async def gen_keyboard(mails, email, domain):
    num = 0
    i_kbd = InlineKeyboard(row_width=1)
    data = []
    for mail in mails:
        id = mail['id']
        data.append(
            InlineKeyboardButton(f"{mail['subject']}", f"mail |{email}|{domain}|{id}")
        )
        num += 1
    data.append(
        InlineKeyboardButton(f"😑 ᴜᴘᴅᴀᴛᴇ ᴍᴀɪʟ ʙᴏx 😑", f"mailbox |{email}|{domain}")
    )
    i_kbd.add(*data)
    return i_kbd
 
#********************************************************************************

@app.on_callback_query(filters.regex("mailbox"))
async def mail_box(_, query : CallbackQuery):
    Data = query.data
    callback_request = Data.split(None, 1)[1]
    m, email , domain = callback_request.split("|")
    mails = requests.get(f'{API2}{email}&domain={domain}').json()
    if mails == []:
            await query.answer("🤷‍♂️ ɴᴏ ᴍᴀɪʟs ғᴏᴜɴᴅ! 🤷‍♂️")
    else:
        try:
            smail = f"{email}@{domain}"
            mbutton = await gen_keyboard(mails,email, domain)
            await query.message.edit(f""" 
**📬ᴅᴏɴᴇ,ʏᴏᴜʀ ᴇᴍᴀɪʟ ᴀᴅᴅʀᴇss ᴄʀᴇᴀᴛᴇᴅ!**
📧 **ᴇᴍᴀɪʟ** : `{smail}`
📨 **ᴍᴀɪʟ ʙᴏx** : ✅
**ᴘᴏᴡᴇʀᴇᴅ ʙʏ** : @ROCKS_ROBOTS""",
reply_markup = mbutton
)   
        except bad_request_400.MessageNotModified as e:
            await query.answer("🤷‍♂️ ɴᴏ ɴᴇᴡ ᴍᴀɪʟs ғᴏᴜɴᴅ! 🤷‍♂️")

#********************************************************************************

@app.on_callback_query(filters.regex("mail"))
async def mail_box(_, query : CallbackQuery):
    Data = query.data
    callback_request = Data.split(None, 1)[1]
    m, email , domain, id = callback_request.split("|")
    mail = requests.get(f'{API3}{email}&domain={domain}&id={id}').json()
    froms = mail['from']
    subject = mail['subject']
    date = mail['date']
    if mail['textBody'] == "":
        kk = mail['htmlBody']
        body = bs4.BeautifulSoup(kk, 'lxml')
        txt = body.get_text()
        text = " ".join(txt.split())
        url_part = body.find('a')
        link = url_part['href']
        mbutton = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔗 ᴏᴘᴇɴ ʟɪɴᴋ", url=link)
                ],
                [
                    InlineKeyboardButton("ʙᴀᴄᴋ", f"mailbox |{email}|{domain}")
                ]
            ]
        )
        await query.message.edit(f""" 
**ғʀᴏᴍ:** `{froms}`
**sᴜʙᴊᴇᴄᴛ:** `{subject}`   
**ᴅᴀᴛᴇ**: `{date}`
{text}
""",
reply_markup = mbutton
)
    else:
        body = mail['textBody']
        mbutton = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ʙᴀᴄᴋ", f"mailbox |{email}|{domain}")
                ]
            ]
        )
        await query.message.edit(f""" 
**ғʀᴏᴍ:** `{froms}`
**sᴜʙᴊᴇᴄᴛ:** `{subject}`   
**ᴅᴀᴛᴇ**: `{date}`
{body}
""",
reply_markup = mbutton
)
#********************************************************************************

@app.on_message(filters.command("domains"))
async def fakemailgen(_, message: Message):
    name = message.from_user.id
    x = requests.get(f'https://www.1secmail.com/api/v1/?action=getDomainList').json()
    xx = str(",".join(x))
    email = xx.replace(",", "\n")
    await app.send_message(
    name, 
    text = f"""
**{email}**
""",
    reply_markup = create)



#============================================================================================
#Owner commands pannel here
#user_count, broadcast_tool

@app.on_message(filters.command("stats") & filters.user(OWNER))
async def stats(_, message: Message):
    name = message.from_user.id
    served_chats = len(await get_served_chats())
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    served_users = len(await get_served_users())
    served_users = []
    users = await get_served_users()
    for user in users:
        served_users.append(int(user["bot_users"]))

    await app.send_message(
        name,
        text=f"""
🍀 ᴄʜᴀᴛs sᴛᴀᴛs 🍀
🙋‍♂️ ᴜsᴇʀs : `{len(served_users)}`
👥 ɢʀᴏᴜᴘs : `{len(served_chats)}`
🚧 ᴛᴏᴛᴀʟ ᴜsᴇʀs & ɢʀᴏᴜᴘs : {int((len(served_chats) + len(served_users)))} """)

async def broadcast_messages(user_id, message):
    try:
        await message.forward(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await remove_served_user(user_id)
        return False, "Deleted"
    except UserIsBlocked:
        await remove_served_user(user_id)
        return False, "Blocked"
    except PeerIdInvalid:
        await remove_served_user(user_id)
        return False, "Error"
    except Exception as e:
        return False, "Error"

@app.on_message(filters.private & filters.command("bcast") & filters.user(OWNER) & filters.reply)
async def broadcast_message(_, message):
    b_msg = message.reply_to_message
    chats = await get_served_users() 
    m = await message.reply_text("ʙʀᴏᴀᴅᴄᴀsᴛ ɪɴ ᴘʀᴏɢʀᴇss")
    for chat in chats:
        try:
            await broadcast_messages(int(chat['bot_users']), b_msg)
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(int(e.x))
        except Exception:
            pass  
    await m.edit(f"""
ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ:.""")    

print("I'm Alive Now!")
app.run()
