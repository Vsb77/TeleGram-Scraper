#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import configparser
import os, sys
import csv
import random
import time

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"
lb = "\033[1;34m"
wh = "\033[1;37m"
SLEEP_TIME = 30

class main():

    def banner():
        
        print(f"""
    {re}╔╦╗{cy}┌─┐┌─┐┌─┐┌─┐┬─┐{re}╔═╗
    {re} ║ {cy}├─┐├┤ ├─┘├─┤├┬┘{re}╚═╗
    {re} ╩ {cy}└─┘└─┘┴  ┴ ┴┴└─{re}╚═╝
    
            """)

    def send_sms():
        try:
            cpass = configparser.RawConfigParser()
            cpass.read('config.data')
            api_id = cpass['cred']['id']
            api_hash = cpass['cred']['hash']
            phone = cpass['cred']['phone']
        except KeyError:
            main.banner()
            print(re + "[!] Конфигурационный файл не найден, выполните: ",lb+"Настройка.bat\n")
            sys.exit(1)

        client = TelegramClient(phone, api_id, api_hash)
         
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            main.banner()
            client.sign_in(phone, input(gr + '[+] Введите код из Telegram: ' + re))

        main.banner()
        input_file = sys.argv[1]
        users = []
        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f,delimiter=",",lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                users.append(user)
        print(gr+"[1] отправлять по идентификатору пользователя (user id)"
           "\n[2] отправлять по имени пользователя (username) ")
        mode = int(input(gr+"Выберите параметр : "+re))
         
        message = input(gr+"[+] Введите текст вашего сообщения : "+re)
         
        for user in users:
            if mode == 2:
                if user['username'] == "":
                    continue
                receiver = client.get_input_entity(user['username'])
            elif mode == 1:
                receiver = InputPeerUser(user['id'],user['access_hash'])
            else:
                print(re+"[!] Неверный режим, Выполняется выход")
                client.disconnect()
                sys.exit()
            try:
                print(gr+"[+] Отправка сообщения:", user['name'])
                client.send_message(receiver, message.format(user['name']))
                print(gr+"[+] Задерка {} секунд".format(SLEEP_TIME))
                time.sleep(1)
            except PeerFloodError:
                print(re+"[!] Получено сообщение об ошибке флуда из telegram. "
                       "\n[!] Сценарий сейчас останавливается. "
                       "\n[!] Пожалуйста, повторите попытку через некоторое время.")
                client.disconnect()
                sys.exit()
            except Exception as e:
                print(re+"[!] Ошибка:", e)
                print(re+"[!] Продолжаем... ")
                continue
        client.disconnect()
        print("Задание выполнено. Сообщение отправлено всем пользователям.")



main.send_sms()
