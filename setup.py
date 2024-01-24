#!/bin/env python3

"""

you can re run setup.py
if you have added some wrong value

"""
import pandas as pd

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"
lb = "\033[1;34m"
wh = "\033[1;37m"

import os, sys  # импорт функций системы
import time  # импорт библиотеки время


#######################################################################################################################
def shutdown():
    print("\nЕсли хотите продолжить работу, введите в командной строке: ", lb + "python setup.py")
def config_setup():  # функция - настройки конфигурации
    import configparser
    banner()
    cpass = configparser.RawConfigParser()
    cpass.add_section('cred')
    xid = input(gr + "[+] введите api ID :  " + re)
    cpass.set('cred', 'id', xid)
    xhash = input(gr + "[+] введите hash ID : " + re)
    cpass.set('cred', 'hash', xhash)
    xphone = input(gr + "[+] введите телефонный номер : " + re)
    cpass.set('cred', 'phone', xphone)
    setup = open('config.data', 'w')
    cpass.write(setup)
    setup.close()
    print(gr + "[+] настройки сохранены !")

def requirements():  # установка библиотек cython, numpy, pandas
    def csv_lib():
        banner()
        print(gr + '[' + cy + '+' + gr + ']' + cy + 'Загрузка...')
        os.system("""
			pip3 install cython numpy pandas
			python3 -m pip install cython numpy pandas
			""")

    banner()  # показ баннера
    print(gr + '[' + cy + '+' + gr + ']' + cy + 'установка csv merge займет до 10 минут.')
    input_csv = input(gr + '[' + cy + '+' + gr + ']' + cy + 'Вы хотите использовать функцию '
                                                            '"объеденить таблицы" (y/n)): ').lower()
    if input_csv == "y":
        csv_lib()
    else:
        pass
    print(gr + "[+] Установка модулей...")
    os.system("""
		pip3 install telethon requests configparser
		python3 -m pip install telethon requests configparser
		touch config.data
		""")

    print(gr + "[+] установка закончена.\n")

def merge_csv():  # функция слияние csv
    import pandas as pd           #загрузка модуля
    banner()                       #показ баннера
    f1 = input("Введите название файлов через пробел (file1.csv file2.csv) ").split()
    df1, df2 = pd.read_csv(f1[0]), pd.read_csv(f1[1])
    merge = pd.concat([df1,df2])
    merge = merge.drop_duplicates()
    #merge = df1.merge(df2, on='username')
    merge.to_csv("output.csv", index=False)
    print(gr + '[' + cy + '+' + gr + ']' + cy + 'объединение' + f1[0] + ' & ' + f1[1] + ' ...')
    print(gr + '[' + cy + '+' + gr + ']' + cy + 'обработка больших файлов может занять некоторое время... ')
    print(gr + '[' + cy + '+' + gr + ']' + cy + 'файл сохранен "output.csv" \n')


#######################################################################################################################
def banner():
    print(f"""
	{re}╔═╗{cy}┌─┐┌┬┐┬ ┬┌─┐
	{re}╚═╗{cy}├┤  │ │ │├─┘
	{re}╚═╝{cy}└─┘ ┴ └─┘┴
	""")


banner()
print("1. Стандартная установка (рекомендуется) \n"
    "2. Настройка конфигурации api\n"
	"3. Установка библиотек \n"
	"4. Объединить 2 файла .csv в один\n"
	"5. Обновить программу до последней версии\n"
	"6. Справка")
cm = int(input(gr +"Выберите цифру и нажмите Enter: "))
if cm == 1: requirements(), config_setup(), shutdown()
elif cm == 2: config_setup(), shutdown()
elif cm == 3: requirements(), shutdown()
elif cm ==6: print(wh + "Стандартная установка (рекомендуется) - полная установка необходимой конфигурации\n"
						"Настройка конфигурации api - привязка аккаунта Telegram (через СМС код)\n"
						"Установка библиотек - рекомендуется установить все предложенные библиотеки"
						"\nОбъединить 2 файла .csv в один - объеденит 2 списка в один, удалив повторения"
						"\nОбновить программу до последней версии - обновление ПО"), shutdown()
elif cm == 4: merge_csv(), shutdown()


