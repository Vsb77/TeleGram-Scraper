from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys  #модуль системных
import configparser # импорт модуля для чтения конфигурации с файла
import csv # импорт модуля для работы с csv файлами
import time # импорт модуля время

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"
lb = "\033[1;34m"
wh = "\033[1;37m"

def banner():
    print(f"""
{re}╔╦╗{cy}┌─┐┌─┐┌─┐┌─┐┬─┐{re}╔═╗
{re} ║ {cy}├─┐├┤ ├─┘├─┤├┬┘{re}╚═╗
{re} ╩ {cy}└─┘└─┘┴  ┴ ┴┴└─{re}╚═╝


        """)

cpass = configparser.RawConfigParser()
cpass.read('config.data') # чтение конфигурационного файла config.data

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash) # извлечение данных
except KeyError:
    banner()
    print(re+"[!] Конфигурационный файл не найден, выполните: ",lb+"Настройка.bat\n") # если данные не найдены
    sys.exit(1)

client.connect()  # авторизация пользователя
if not client.is_user_authorized():
    client.send_code_request(phone)
    banner()
    client.sign_in(phone, input(gr+'[+] Введите код из Telegram: '+re))
 
banner()
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
 
print(gr+'[+] Выберите группу для выгрузки списка  участников :'+re)
i=0
for g in groups:
    print(gr+'['+cy+str(i)+gr+']'+cy+' - '+ g.title)
    i+=1
 
print('')
g_index = input(gr+"[+] Введите номер : "+re)
target_group=groups[int(g_index)]
 
print(gr+'[+] Выгрузка участников...')
time.sleep(1)
all_participants = []
all_participants = client.get_participants(target_group, aggressive=False) # лимиты по api True False
 
print(gr+'[+] Сохранение в файл...')
time.sleep(1)
with open("members.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
print(gr+'[+] Выгрузка участников выполнена успешно.')
