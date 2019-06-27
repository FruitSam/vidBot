import telebot
import urllib.request
import os
import praw 
import threading
from flask import Flask, request
import pickle

bot_token = '877541643:AAEOULzC-cgyfYt6yftU6167oDQ1ZQvlCMQ'
bot = telebot.TeleBot(token=bot_token)
reddit = praw.Reddit(client_id= 'CYJNh3ecbQhxzQ', client_secret= 'du58jAIgpE9lbfXoLoJlkEUnl4Y', username= 'tgdankbot', password= 'Kutaluta@3crest', user_agent= 't5' )
subreddit = reddit.subreddit('dankvideos')
top_vids = subreddit.top(limit = 10)
url_arr = []
app = Flask(__name__)
url_sent = []

def update_urls():
    url_arr.clear()
    for submission in top_vids:
        if submission.url in url_sent:
            pass
        else:
            url_arr.append(submission.url)
            url_sent.append(submission.url)
            print(url_arr)
    with open('sent.txt','wb') as fp:
        pickle.dump(url_sent, fp)

def dl(url):
    f = open('vid.mp4', 'wb')
    f.write(urllib.request.urlopen(url).read())
    f.close


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


