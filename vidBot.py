from __future__ import unicode_literals
import telebot
import urllib.request
import os
import praw 
import threading
#from flask import Flask, request
#import pickle
import requests
import youtube_dl
#from shutil import copyfile
import subprocess
import glob



bot_token = 'your_bot_token'
bot = telebot.TeleBot(token=bot_token)
reddit = praw.Reddit(client_id= 'CYJNh3ecbQhxzQ', client_secret= 'du58jAIgpE9lbfXoLoJlkEUnl4Y', username= 'tgdankbot', password= 'Kutaluta@3crest', user_agent= 't5' )
subreddit = reddit.subreddit('dankvideos')
tops = subreddit.hot(limit = 5)
url_arr = []
#app = Flask(__name__)
#url_sent = []
ydl_opts = {
        'format': 'bestvideo+bestaudio',
        

    }

ydl = youtube_dl.YoutubeDL(ydl_opts)
bot.delete_webhook()

def update_urls():
    del url_arr[:]
    for submission in tops:
        url_arr.append(submission.url)

    


    

def dl(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        

        



def send_vid(): 
    update_urls()
    count = len(url_arr)
    for i in range(0,count-1):
        if(url_arr[i] is not None):
            dl(url_arr[i])
    my_list = glob.glob(r'C:\Users\husam\source\repos\vidBot\vidBot\*.mp4' or r'C:\Users\husam\source\repos\vidBot\vidBot\*.m4a')
    countr = len(my_list)
    print(countr)
    print(my_list)
    for i in range(0,countr):
        vid = open(my_list[i],'rb')
        print('sent')
        bot.send_video('channel/chat_id',vid)
        vid.close
    


#def keep_up():
    #threading.Timer(500,keep_up).start()
    #urllib.request.urlopen('https://dankvids-bot.herokuapp.com/')
    #print('requested')

@bot.message_handler(commands = ['start'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome, press /help for more information')
    #keep_up()

@bot.message_handler(commands = ['help'])
def send_welcome(message):
    bot.reply_to(message, 'Hit /send')

@bot.message_handler(func=lambda message: 'send 384252204' in message.text)
def every24(message):
        send_vid()
        
        
#@app.route('/' + bot_token, methods=['POST'])
#def getMessage():
    #bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    #return "!", 200


#@app.route("/")
#def webhook():
    #bot.remove_webhook()
   # bot.set_webhook(url='https://dankvids-bot.herokuapp.com/' + bot_token)
    #return "!", 200

#if __name__ == "__name__":
    #app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

def listener(messages):
    for m in messages:
        print(str(m))


bot.set_update_listener(listener)
bot.polling()

