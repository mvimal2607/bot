import telegram
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler
from tqdm.contrib.telegram import tqdm, trange
from base64 import decodebytes
from database import *
from pathlib import Path
import pathlib
import logging
import pysftp
import gdown
import time
import math
import gdown
import requests
import paramiko
import os
import shutil
import json
import datetime
import pytz


# Some Global Variables
HOME = os.path.expanduser("~") 
with open(f'{HOME}/secrets.txt', 'r') as file:
    content = file.read().replace('\n', ',')
    content = content.split(',')
    token = content[0]
    sfpass = content[1]
    CHAT_ID = content[2]

# Host key for pysftp
keydata = b"""AAAAC3NzaC1lZDI1NTE5AAAAIOQD35Ujalhh+JJkPvMckDlhu4dS7WH6NsOJ15iGCJLC"""
key = paramiko.Ed25519Key(data=decodebytes(keydata))
cnopts = pysftp.CnOpts()
cnopts.hostkeys.add('frs.sourceforge.net', 'ssh-ed25519', key)

# Official device list
devurl = "https://raw.githubusercontent.com/ProjectEverest/vendor_everst/qpr2/everst.devices"
gdevurl = "https://github.com/ProjectEverst/vendor_everst/blob/12.1/everest.devices"
req = requests.get(devurl)
if req.status_code in [200]:
    devices = req.text
else:
    print(f"Could not retrieve: {devurl}, err: {req.text} - status code: {req.status_code}")
devices = devices.replace('\n', ',')
devices = devices.split(',')

# Start Command
async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    mess_id = update.effective_message.message_id
    mess = '''
Hello, I am EverestBot.
Use /help to know how to use me.
'''
    await context.bot.send_message(CHAT_ID, reply_to_message_id=mess_id, text=mess)

# Help Command
async def help(update: Update, context: CallbackContext.DEFAULT_TYPE):
    mess_id = update.effective_message.message_id
    mess = '''
Helping guide for using me:

Supported commands :
1. /start
2. /help
3. /post

You can use any command without any arguments for help related to that command.

'''
    await context.bot.send_message(CHAT_ID, reply_to_message_id=mess_id, text=mess)

# Post command
async def post(update: Update, context: CallbackContext.DEFAULT_TYPE):
    mess_id = update.effective_message.message_id
    help = f'''
Use this command in following format to make post for your device.

/post device_codename device_changelog_link

device_codename is codename for your device.
Please use UpperCase letters if you did same <a href="{gdevurl}">here</a>

device_changelog_link is telegraph link of changelog for your device.'''

    dmess = f'''
Sorry, I couldn't find your device codename <a href="{gdevurl}" >here</a>.
Please make PR if you didn't.
'''
    arg = context.args
    codename = None
    dclog = None
    try:
        codename = arg[0]
        dclog = arg[1]
    except IndexError:
        await context.bot.send_message(CHAT_ID, reply_to_message_id=mess_id, text=help, parse_mode='HTML', disable_web_page_preview=True)
        return
    if codename in devices:
        pass
    else:
        await content.bot.send_message(CHAT_ID, reply_to_message_id=mess_id, text=dmess, parse_mode='HTML', disable_web_page_preview=True)
        return
    if dclog == None:
        pass
    current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    day = current_time.day
    month = current_time.month
    month = months[month]
    year = current_time.year
    date = f" {month}-{day}-{year} "
    mess = f'''
Project Everest v{database['EverestVersion']} - OFFICIAL | Android 14
📲 : {database[codename]['device']} ({codename})
📅 : {date}
🧑‍💼 : {database[codename]['maintainer']}

▪️ Changelog: <a href="https://github.com/ProjectBlaze/official_devices/blob/12.1/changelog.md" >Source</a> | <a href="{dclog}" >Device</a>
▪️ <a href="https://www.projectblaze.live/download.html" >Download</a>
▪️ <a href="https://t.me/projectblazeupdates/97" >Screenshots</a>
▪️ <a href="{database[codename]['sgroup']}" >Support Group</a>
▪️ <a href="https://t.me/projectblaze" >Community Chat</a>
▪️ <a href="https://t.me/projectblazeupdates" >Updates Channel</a>

#Everest #{codename} #Android14 #U
'''
    await context.bot.send_photo(CHAT_ID, photo=open('images/blaze1.2.png', 'rb'), caption=mess, reply_to_message_id=mess_id, parse_mode='HTML')
