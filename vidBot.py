from __future__ import unicode_literals
import telebot
import urllib.request
import os
import praw 
import threading
from flask import Flask, request
import pickle
import requests
from urllib.request import build_opener, HTTPCookieProcessor, Request
import youtube_dl

bot_token = '877541643:AAEOULzC-cgyfYt6yftU6167oDQ1ZQvlCMQ'
bot = telebot.TeleBot(token=bot_token)
reddit = praw.Reddit(client_id= 'CYJNh3ecbQhxzQ', client_secret= 'du58jAIgpE9lbfXoLoJlkEUnl4Y', username= 'tgdankbot', password= 'Kutaluta@3crest', user_agent= 't5' )
subreddit = reddit.subreddit('dankvideos')
top_vids = subreddit.top(limit = 10)
url_arr = []
app = Flask(__name__)
url_sent = []
outtmpl = 'vid.mp4'
ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
            {'key': 'FFmpegMetadata'},
        ],

    }

ydl = youtube_dl.YoutubeDL(ydl_opts)



def update_urls():
    url_arr.clear()
    for submission in top_vids:
        if submission.url in url_sent:
            pass
        else:
            the_url = submission.url
            url_arr.append(the_url)
            url_sent.append(the_url)
            print(url_arr)
    with open('sent.txt','wb') as fp:
        pickle.dump(url_sent, fp)

def dl(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)


def send_vid(): 
    update_urls()
    count = len(url_arr)
    for i in range(0,count-1):
        if(url_arr[i] is not None):
            dl(url_arr[i])
            vid = open('vid.mp4','rb')
            bot.send_video('@testingbottg',vid)
            vid.close
    


def keep_up():
    threading.Timer(500,keep_up).start()
    urllib.request.urlopen('https://dankvids-bot.herokuapp.com/')
    print('requested')

@bot.message_handler(commands = ['start'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome, press /help for more information')
    keep_up()

@bot.message_handler(commands = ['help'])
def send_welcome(message):
    bot.reply_to(message, 'Hit /send')

@bot.message_handler(func=lambda message: 'send 384252204' in message.text)
def every24(message):
        send_vid()
        
        
@app.route('/' + bot_token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://dankvids-bot.herokuapp.com/' + bot_token)
    return "!", 200

if __name__ == "__name__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


