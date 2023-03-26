# شناسه های اکانت ها در این لیست وارد شود
auths = ['auth']
# لینک پست در این متغیر وارد شود
post_link = 'https://rubika.ir/Persian_PyThon/DDBEJAHJDBCBAFE'
# تنظیم زمان استراحت بین هربار ارسال پست (ثانیه)
sleep_send = 1
# در صورتی که می خواهید لینک دونی ها را دستی وارد کنید گوید های لینک دونی را در این لیست وارد کنید در غیر این صورت خود سورس لینک دونی ها را به صورت خودکار پیدا می کند
linkdonis = []

from pyrubi import Bot
from re import findall
from random import choice
from os import name, system
from threading import Thread
from time import sleep
from datetime import datetime

bot = Bot(auths[-1])

class Fore:
    Black = '\u001b[30m'
    Red = '\u001b[31m'
    Green = '\u001b[32'
    Yellow = '\u001b[33m'
    Blue = '\u001b[34m'
    Magenta = '\u001b[35m'
    Cyan = '\u001b[36m'
    White = '\u001b[37m'

post_data = bot.get_link_info(post_link)
del post_data['object_type']

linkdoni_ids = linkdonis or [i['object_guid'] for i in bot.search_chats('لینکدونی')]

def get_group_join_links():
    while True:
        try:
            print(f'{Fore.Yellow}Receiving the {Fore.Cyan}Group Join Links {Fore.Yellow}from linkdonis ...\n')
            group_join_links = []
            for linkdoni_id in linkdoni_ids:
                linkdoni_messages = [i['text'] for i in bot.get_chat_messages(linkdoni_id, bot.get_chat_last_message_id(linkdoni_id))]
                for message in linkdoni_messages:
                    join_links = findall(r'https://rubika.ir/joing/\w{32}', message)
                    for join_link in join_links:
                        group_join_links.append(join_link)
            print(f'{Fore.Cyan}{len(group_join_links)} {Fore.Yellow}Group Join Links were found')
            sleep(2.5)
            if name == 'nt':
                system('cls')
            else:
                system('clear')
            return group_join_links
        except:
            continue

def forward_post_to_group(group_join_link, count_send):
    try:
        bot = Bot(choice(auths))
        join_data = bot.join_group(group_join_link)
        time_join = datetime.now().strftime('%H : %M : %S - %p')
        if 'SendMessages' in join_data['chat_update']['chat']['access']:
            forward_data = bot.forward_message(post_data['object_guid'], [post_data['message_id']], join_data['group']['group_guid'])
            bot.leave_group(join_data['group']['group_guid'])
            return print(f'{Fore.White}| {count_send} - {Fore.Cyan}Sended to the {Fore.Magenta}{join_data["group"]["group_title"]}\n{Fore.Blue}| Link : {group_join_link}\n{Fore.Cyan}| Guid : {join_data["group"]["group_guid"]}\n{Fore.Yellow}| Count seen : {forward_data["message_updates"][0]["message"]["count_seen"]}\n{Fore.Magenta}| Time send : {time_join}\n')
        else:
            bot.leave_group(join_data['group']['group_guid'])
            print(f'{Fore.White}| {count_send} - {Fore.Red}The {Fore.Magenta}{join_data["group"]["group_title"]} {Fore.Red}is locked and cannot be sent !\n{Fore.Magenta}| Time check : {time_join}\n')
    except:
        print(f'{Fore.Red}Error ! There was a problem joining the group.')

count_send = 0
while 1:
    for join_link in get_group_join_links():
        count_send += 1
        Thread(target=forward_post_to_group, args=[join_link, count_send]).start()
        sleep(sleep_send)