# -*- coding: utf-8 -*-
version = 3.1
lencommands = 0
import os

clear = lambda: os.system(f'cls && title Selfbot {version} - {lencommands} Commands' if os.name == 'nt' else 'clear')
try:
    import discord
    from discord.ext import commands
    from colorama import init, Fore;

    init()
    import requests
    from plyer import notification
    from googletrans import Translator
    from emoji import EMOJI_DATA
    from qrcode import make
except:
    os.system('pip install -U discord.py-self==1.9.2 colorama requests plyer googletrans==4.0.0rc1 emoji qrcode')
    import discord
    from discord.ext import commands
    from colorama import init, Fore;

    init()
    import requests
from subprocess import Popen
from time import sleep
from webbrowser import open as webopen
from threading import Thread
from datetime import datetime, timedelta
import random
import json

with open("config.json", "r", encoding="utf-8-sig") as f:
    try:
        config = json.load(f)
    except Exception as e:
        clear()
        print(e)
        print(Fore.LIGHTBLUE_EX + '\nОшибка конфига')
        while True: sleep(9)

theme = config['GENERAL']['theme']
if theme == 'random':
    theme = random.choice(['standart', 'discord', 'hacker', 'beach'])
if theme == 'standart':
    color = {'Intro': Fore.RED, 'Info_name': Fore.MAGENTA, 'Info_value': Fore.YELLOW}
elif theme == 'discord':
    color = {'Intro': Fore.LIGHTBLUE_EX, 'Info_name': Fore.WHITE, 'Info_value': Fore.LIGHTCYAN_EX}
elif theme == 'hacker':
    color = {'Intro': Fore.LIGHTGREEN_EX, 'Info_name': Fore.GREEN, 'Info_value': Fore.WHITE}
elif theme == 'beach':
    color = {'Intro': Fore.LIGHTYELLOW_EX, 'Info_name': Fore.LIGHTYELLOW_EX, 'Info_value': Fore.LIGHTCYAN_EX}
else:
    clear()
    print(Fore.LIGHTBLUE_EX + 'Неизвестная тема')
    while True: sleep(9)
on_command_error = True
Intro = color['Intro'] + r"""
____  ___       .__ 
\   \/  /___.__.|__|
 \     /<   |  ||  |
 /     \ \___  ||  |
/___/\  \/ ____||__|
      \_/\/         
"""
lencommands = 0
clear()
print(Fore.WHITE + 'Загрузка...')
pref = config['GENERAL']['prefix']
try:
    bot = commands.Bot(command_prefix=pref, case_insensitive=True, self_bot=True)
except Exception as e:
    clear()
    print(e)
    print(Fore.LIGHTBLUE_EX + '\nНа гитхабе селфбота написано как решить эту ошибку!!!')
    sleep(3)
    webopen('https://github.com/PuroSlavKing/Discord-AIM-SBot', 2)
    while True: sleep(9)
bot.remove_command('help')
start_time = datetime.now()
update = ''


async def check(ctx):
    if not config['OTHER']['nuke_commands']:
        await ctx.message.edit(
            content='**:warning: Краш команды отключены! Для того чтобы включить краш команды измените файл config.json**')
        return False
    return True


def disco_status():
    while True:
        text = ''
        lasttext = ''
        for i in range(5):
            while True:
                emoji = random.choice(['🔴', '🟢', '🔵', '🟡', '🟣'])
                if not emoji in text:
                    text += emoji
                    break
        if text == lasttext: continue
        lasttext = text
        try:
            requests.patch("https://discord.com/api/v9/users/@me/settings", headers={'authorization': bot.http.token},
                           json={'custom_status': {'text': text}})
        except:
            pass
        sleep(5)

@bot.event
async def on_connect():
    global lencommands
    lencommands = len(bot.commands)
    for file in ['LICENSE', 'README.md']:
        try:
            os.remove(file)
        except:
            pass
    for file in os.listdir():
        if file.endswith('.txt') or file.endswith('.png'):
            os.remove(file)
    if config['OTHER']['disco_status']: Thread(target=disco_status).start()
    #	status=config['GENERAL']['status']
    response = requests.get('https://discord.com/api/users/@me/settings', headers={'authorization': bot.http.token})
    status = response.json()['status']
    sstatus = discord.Status.online
    if status == 'idle':
        sstatus = discord.Status.idle
    elif status == 'dnd':
        sstatus = discord.Status.dnd
    elif status == 'invisible':
        sstatus = discord.Status.invisible
    await bot.change_presence(status=sstatus)
    try:
        channel = bot.get_channel(config['OTHER']['auto_send_channel'])
        for i in config['OTHER']['auto_send_text']:
            await channel.send(i)
    except:
        pass
    clear()
    print(Intro)
    print(f"{color['Info_name']}Аккаунт: {color['Info_value']}{bot.user}")
    print(f"{color['Info_name']}ID: {color['Info_value']}{bot.user.id}")
    print(f"{color['Info_name']}Префикс: {color['Info_value']}{pref}")
    print(f"{color['Info_name']}Время запуска: {color['Info_value']}{start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    if float(requests.get(
            'https://raw.githubusercontent.com/PuroSlavKing/Discord-AIM-SBot/main/cogs/version').text) > version:
        global update
        update = f':warning: Пожалуйста, обновите селфбота используя команду {pref}bot**\n**'
        print(
            f'{Fore.CYAN}Пожалуйста, обновите селфбота используя команду {Fore.LIGHTCYAN_EX}{pref}bot{Fore.RESET}{Fore.RED}\n')
        return

    print(Fore.RED)


if on_command_error:
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error = ':warning: Недостаточно аргументов!'
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.BadArgument):
            error = ':warning: Указан не правильный аргумент!'
        elif isinstance(error, discord.errors.Forbidden):
            error = ':warning: Не достаточно прав для выполнения данной команды!'
        error = str(error).replace('Command raised an exception: ', '')
        print(f"{Fore.RED}[ERROR] {error}")
        try:
            await ctx.send(f'**:warning: Произошла ошибка :x:\n```{error}```**')
        except:
            pass


@bot.event
async def on_command(ctx):
    time = datetime.now().strftime('%H:%M:%S')
    arguments = ctx.message.content.replace(pref + ctx.invoked_with, '')
    print(
        f'{Fore.LIGHTWHITE_EX}[{time}] {Fore.LIGHTCYAN_EX}{pref}{ctx.invoked_with}{Fore.LIGHTGREEN_EX}{arguments}{Fore.RESET}')


@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)


@bot.command(aliases=['хелп', 'помощь'])
async def help(ctx, cat=None):
    if cat == None:
        await ctx.message.edit(content=(f'\n'
                                        f'⟃⟞⟞⟞⟞⟞⟞⟞✫**⟮Разделы⟯**✫⟝⟝⟝⟝⟝⟝⟝⟝⟄\n'
                                        f'**{pref}help tools** — полезные команды.\n'
                                        f'**{pref}help info** — команды для получения информации.\n'
                                        f'**{pref}help fun** — развлекательные команды.\n'
                                        f'**{pref}help moderation** — команды модерации.\n'
                                        f'**{pref}help image** — команды связанные с изображениями.\n'
                                        f'**{pref}help nuke** — команды краша.\n'
                                        f'\n'
                                        f'⟃⟞⟞⟞⟞⟞⟞⟞✫**⟮Debug⟯**✫⟝⟝⟝⟝⟝⟝⟝⟄\n'
                                        f'**{pref}reload**  — перезагрузить бота.\n'
                                        f'**{pref}github**  — ссылка на GitHub.\n'))
        return
    cat = cat.lower()
    if cat == 'tools':
        await ctx.message.edit(content=(f'\n'
                                        f'⟃⟞⟞⟞⟞⟞⟞⟞✫**⟮Tools⟯**✫⟝⟝⟝⟝⟝⟝⟝⟝⟄\n'
                                        f'**{pref}status [Тип статуса] [Текст]** — меняет статус.\n'
                                        f'**{pref}purge [Количество]** — удаляет ваши сообщения.\n'
                                        f'**{pref}clear [Количество]** — удаляет все сообщения.\n'
                                        f'**{pref}masspin [Количество]** — закрепляет последние сообщения.\n'
                                        f'**{pref}messages [Количество]** — сохраняет последние сообщения в файл.\n'
                                        f'**{pref}groupsleave** — выходит из всех групп.\n'
                                        f'**{pref}blocksend [Пинг/ID] [Текст]** — отправляет сообщение в ЛС, даже если вы добавили пользователя в ЧС.\n'
                                        f'**{pref}copystatus [Пинг/ID]** — копирует RPC статус.\n'
                                        f'**{pref}translate [На какой язык] [Текст]** — переводчик.\n'
                                        f'**{pref}nitro [Количество] [classic/full]** — генерирует нитро (без проверок).\n'
                                        f'**{pref}copyemojis [ID Сервера на который нужно скопировать]** — копирует эмодзи.\n'
                                        f'**{pref}hackpurge** — "удаляет" сообщения без прав.\n'
                                        f'**{pref}deletedms [Имя]** — удаляет ЛС от ботов с указанным именем.\n'))
    elif cat == 'info':
        await ctx.message.edit(content=(f'\n'
                                        f'⟃⟞⟞⟞⟞⟞⟞⟞✫**⟮Info⟯**✫⟝⟝⟝⟝⟝⟝⟝⟝⟄\n'
                                        f'**{pref}server** — показывает информацию о сервере.\n'
                                        f'**{pref}user [Пинг/ID]** — показывает информацию о пользователе.\n'
                                        f'**{pref}token [Токен]** — показывает информацию о токене.\n'))
    elif cat == 'fun':
        await ctx.message.edit(content=(f'\n'
                                        f'⟃⟞⟞⟞⟞⟞⟞⟞✫**⟮Fun⟯**✫⟝⟝⟝⟝⟝⟝⟝⟝⟄\n'
                                        f'**{pref}trolldelete [Пинг/ID]** — удаление всех сообщений от пользователя.\n'
                                        f'**{pref}trollreaction [Пинг/ID] [Эмодзи]** — ставит эмодзи на все сообщения пользователя.\n'
                                        f'**{pref}trollrepeat [Пинг/ID]** — повторение всех сообщений пользователя.\n'
                                        f'**{pref}trollmove [Количество] [Пинг/ID]** — перемещает пользователя по голосовым каналам.\n'
                                        f'**{pref}untroll** — выключение команды troll.\n'
                                        f'**{pref}reactions [Количество] [Эмодзи] [ID Канала]** — спамит реакциями.\n'
                                        f'**{pref}ball [Вопрос]** — ответит на любые вопросы.\n'
                                        f'**{pref}hack [Пинг/ID]** — взлом аккаунта.\n'
                                        f'**{pref}faketyping [Длительность в секундах] [ID Канала]** — печатает сообщение...\n'
                                        f'**{pref}reactionbot [Эмодзи] [ID Сервера]** — ставит реакции на все сообщения.\n'
                                        f'**{pref}say [Пинг/ID] [Текст]** — пишет сообщение от имени другого пользователя.\n'
                                        f'**{pref}criptext** — делает ваши сообщения очень страшними!!!\n'
                                        f'**{pref}color [rainbow/water/white]** — делает ваши сообщения красочными.\n'))
    elif cat == 'moderation':
        await ctx.message.edit(content=(f'\n'
                                        f'⟃⟞⟞⟞⟞⟞⟞⟞✫**⟮Moderation⟯**✫⟝⟝⟝⟝⟝⟝⟝⟝⟄\n'
                                        f'**{pref}ban [Пинг/ID] [Причина]** — банит пользователя.\n'
                                        f'**{pref}unban - [Пинг/ID]** — разбанивает пользователя.\n'
                                        f'**{pref}kick [Пинг/ID] [Причина]** — кикает пользователя.\n'
                                        f'**{pref}mute [Пинг/ID] [Длительность] [Причина]** — мутит пользователя.\n'
                                        f'**{pref}unmute [Пинг/ID] [Причина]** — размучивает пользователя.\n'
                                        f'**{pref}slowmode [Длительность]** — ставит слоумод на канал (Пример длительности: 3ч - 3 часа).\n'))
    elif cat == 'image':
        await ctx.message.edit(content=(f'\n'
                                        f'⟃⟞⟞⟞⟞⟞⟞⟞✫**⟮Image⟯**✫⟝⟝⟝⟝⟝⟝⟝⟝⟄\n'
                                        f'**{pref}lgbt [Пинг/ID]** — делает аватарку пользователя разноцветной.\n'
                                        f'**{pref}comment [Пинг/ID] [Текст]** — делает комментарий на ютубе.\n'
                                        f'**{pref}jail [Пинг/ID]** — садит пользователя в тюрьму.\n'
                                        f'**{pref}cmm [Текст]** — change my mind.\n'
                                        f'**{pref}fox** — картинка лисы.\n'
                                        f'**{pref}lightshot [Количество]** — генерирует случайные ссылки на lighshot.\n'
                                        f'**{pref}qrcode [Контент]** — создаёт QRcode.\n'))
    elif cat == 'nuke':
        if await check(ctx):
            await ctx.message.edit(content=(f'\n'
                                            f'⟃⟞⟞⟞⟞⟞⟞⟞✫**⟮Nuke⟯**✫⟝⟝⟝⟝⟝⟝⟝⟝⟄\n'
                                            f'**{pref}nuke** — уничтожение сервера.\n'
                                            f'**{pref}silentnuke [ID Сервера] [Сообщение]** — уничтожение сервера с обходом ВСЕХ анти-краш ботов, и нельзя определить, кто уничтожил сервер.\n'
                                            f'**{pref}spamchannels [Имя]** — спам каналами.\n'
                                            f'**{pref}spamroles [Имя]** — спам ролями.\n'
                                            f'**{pref}spamwebhooks [Сообщение]** — спам вебхуками.\n'
                                            f'**{pref}spam [Количество] [Текст]** — спам с обходом анти-спама.\n'
                                            f'**{pref}timedspam [Задержка (с)] [Количество] [Текст]** — спам с задержкой между сообщениями и обходом анти-спама.\n'
                                            f'**{pref}spamall [Количество] [Текст]** — спам во все каналы.\n'
                                            f'**{pref}spamthreads [Количество] [Имя ветки]** — спамит ветками.\n'
                                            f'**{pref}spamthreadsall [Количество] [Имя ветки]** — спамит во всех каналах ветками.\n'
                                            f'**{pref}spamgroups [Количество] [Жертвы от 2 до 9]** — спамит группами.\n'
                                            f'**{pref}pingall [Количество]** — пингует всех участников на сервере.\n'
                                            f'**{pref}lags [Тип лагов] [Количество]** — делает сильные лаги в канале.\n'
                                            f'**{pref}nukechannel** — удаляет все сообщения в канале, и меняет айди канала.\n'
                                            f'**{pref}deleteall** — удаление всего.\n'
                                            f'**{pref}deletechannels** — удаляет только каналы.\n'
                                            f'**{pref}deleteroles** — удаляет только роли.\n'
                                            f'**{pref}deleteemojis** — удаляет только эмодзи.\n'))
    else:
        await ctx.message.edit(
            content=f'**Напишите `{pref}help`, для просмотра всех категорий команд**')


@bot.command(name='github', aliases=['selfbot', 'бот', 'селфбот', 'гит', 'гитхаб', 'git', 'hub'])
async def __bot(ctx):
    await ctx.message.edit(content='**Ссылка: https://github.com/PuroSlavKing/Discord-AIM-SBot**')


@bot.command(aliases=['перезагрузка', 'стоп', 'перезагрузить', 'stop_all', 'остановить', 'reload', 'stop', 'reset'])
async def stopall(ctx):
    await ctx.message.edit(content=(f'\n'
                                    f'Перезагрузка бота...\n'
                                    f'█▒▒▒▒▒▒▒▒▒\n'))
    clear()
    Popen('python main.py')
    await ctx.message.edit(content=(f'\n'
                                    f'Перезагрузка завершена!\n'
                                    f'██████████\n'))
    await bot.logout()


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
try:
    bot.run(config['GENERAL']["token"])
except:
    while True:
        clear()
        print(Fore.LIGHTBLUE_EX + "Неверный токен")
        while True: sleep(9)
