import os
from dotenv import load_dotenv
import discord
import time
import threading

# .envファイルの内容を読み込見込む
load_dotenv()

# 自分のBotのアクセストークンに置き換えてください
TOKEN = os.environ['TOKEN']

# 通知
notification_text_channel_id = os.environ['NOTIFICATION_TEXT_CHANNEL']
notification_vc_channel_id = os.environ['NOTIFICATION_VC_CHANNEL']
change_channel_id = os.environ['CHANGE_CHANNEL']
button_channel_id = os.environ['BUTTON_CHANNEL']


class View(discord.ui.View):
    def __init__(self):
        super().__init__()

        channelNameList = ['home', 'home(Game)', 'home(Talk)']

        for item in range(3):
            self.add_item(
                Button(channelNameList[item], int(change_channel_id), channelNameList[item]))


class Button(discord.ui.Button):

    def __init__(self, label: str, channelID: int, channelName: str):
        super().__init__(label=label, style=discord.ButtonStyle.red)
        self.channelID = channelID
        self.channelName = channelName

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'{interaction.user.display_name}は{self.label}を押しました', delete_after=3)

        channel = client.get_channel(self.channelID)

        await channel.edit(name=self.channelName)


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await client.get_channel(int(button_channel_id)).send('押したボタンに名前を変更することができるよ！')
        await client.get_channel(int(button_channel_id)).send(view=View())

    async def on_voice_state_update(self, member, before, after):
        # チャンネルの状態が変わっているか
        if before.channel != after.channel:
            print(member)
            # チャンネルをIDから取得
            info_channel = client.get_channel(
                int(notification_text_channel_id))
            try:
                if after.channel.id == int(notification_vc_channel_id):
                    print(after.channel.name + 'に' + member.name + 'が現れた！！')
                    await info_channel.send(after.channel.name + 'に' + member.name + 'が現れた！！')
            except:
                print("Channel is None")


#intents = discord.Intents.default()
intents = discord.Intents.all()
intents.message_content = True
intents.voice_states = True

client = MyClient(intents=intents)
client.run(TOKEN)
