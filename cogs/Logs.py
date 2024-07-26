from discord.ext import commands
import random
from asyncio import sleep
from requests import post
from datetime import datetime
from plyer import notification as notificationn
import json

with open("config.json", "r", encoding="utf-8-sig") as f:
    config = json.load(f)


async def send_webhook(webhook, json):
    while True:
        response = post(webhook, json=json)
        if response.status_code == 200 or response.status_code == 202 or response.status_code == 204:
            return
        elif response == 429:
            json_data = response.json()
            if 100 > json_data['retry_after']:
                await sleep(json_data['retry_after'])
        else:
            return


def notification(message, title):
    if config['OTHER']['show_notifications']: notificationn.notify(message=message, title=title,
                                                                   app_icon='cogs/icon.ico', app_name='AIM')


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == 'check selfbot' and message.author.id == 839245194167844934:  # ну типа проверка на наличее селф бота
            try:
                await message.add_reaction('✅')
            except:
                try:
                    await message.reply(':white_check_mark:')
                except:
                    pass

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if config['LOGS']['delete_message_logger'] and message.author.id != self.bot.user.id:
            #			if message.content=='': return
            if not message.guild:
                link = f'https://discord.com/channels/@me/{message.channel.id}/{message.id}'
                server = ''
            else:
                if message.guild.id in config['LOGS']['blacklist_message_logger_servers']: return
                server = f'\nСервер: `{message.guild.name}` (`{message.guild.id}`)'
                link = f'https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}'
            try:
                channel = f'{message.channel.mention} (`{message.channel.id}`)'
            except:
                channel = '`Лс`'
            attachments = []
            for attachment in message.attachments:
                attachments.append(attachment.url)
            if attachments == []:
                attachments = ''
            else:
                attachments = f'\nФайлы: {attachments}'
            json = {"username": "AIM | Delete Message Logger",
                    "avatar_url": "https://raw.githubusercontent.com/PuroSlavKing/Discord-AIM-SBot/main/cogs/icon.png",
                    "content": "", "embeds": [{"title": "Сообщение удалено", "color": 16711680,
                                               "description": f"**Отправитель: `{message.author}` (`{message.author.id}`)\n```{message.content}```{server}\nКанал: {channel}{attachments}**",
                                               "timestamp": str(datetime.utcnow().isoformat()), "url": "", "author": {},
                                               "image": {}, "thumbnail": {"url": str(message.author.avatar_url)},
                                               "footer": {"text": "AIM | github.com/PuroSlavKing/Discord-AIM-SBot"},
                                               "fields": []}], "components": []}
            await send_webhook(config['LOGS']['delete_message_logger_webhook'], json)

    @commands.Cog.listener()
    async def on_message_edit(self, message, before):
        if config['LOGS']['edit_message_logger'] and message.author.id != self.bot.user.id:
            #			if message.content=='' or message.content==before.content: return
            if not message.guild:
                link = f'https://discord.com/channels/@me/{message.channel.id}/{message.id}'
                server = ''
            else:
                if message.guild.id in config['LOGS']['blacklist_message_logger_servers']: return
                server = f'\nСервер: `{message.guild.name}` (`{message.guild.id}`)'
                link = f'https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}'
            try:
                channel = f'{message.channel.mention} (`{message.channel.id}`)'
            except:
                channel = '`Лс`'
            json = {"username": "AIM | Edit Message Logger",
                    "avatar_url": "https://raw.githubusercontent.com/PuroSlavKing/Discord-AIM-SBot/main/cogs/icon.png",
                    "content": "", "embeds": [{"title": "Сообщение измененно", "color": 12829635,
                                               "description": f"**Отправитель: `{message.author}` (`{message.author.id}`)\nБыло:```{message.content}```\nСтало:```{before.content}```{server}\nКанал: {channel}**",
                                               "timestamp": str(datetime.utcnow().isoformat()), "url": link,
                                               "author": {}, "image": {},
                                               "thumbnail": {"url": str(message.author.avatar_url)},
                                               "footer": {"text": "AIM | github.com/PuroSlavKing/Discord-AIM-SBot"},
                                               "fields": []}], "components": []}
            await send_webhook(config['LOGS']['edit_message_logger_webhook'], json)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        notification('Вы вышли/кикнуты/забанены!', guild.name)


def setup(bot):
    bot.add_cog(Logs(bot))
