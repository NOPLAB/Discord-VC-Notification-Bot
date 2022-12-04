import os
from dotenv import load_dotenv
import discord

# .envファイルの内容を読み込見込む
load_dotenv()

# 自分のBotのアクセストークンに置き換えてください
TOKEN = os.environ['TOKEN']

# 通知
notification_text_channel_id = os.environ['NOTIFICATION_TEXT_CHANNEL']
notification_vc_channel_id = os.environ['NOTIFICATION_VC_CHANNEL']

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_voice_state_update(self, member, before, after):
        # チャンネルの状態が変わっているか
        if before.channel != after.channel:
            print(member)
            # チャンネルをIDから取得
            info_channel = client.get_channel(int(notification_text_channel_id))
            try:
                if after.channel.id == int(notification_vc_channel_id):
                    print (after.channel.name + 'に' + member.name + 'が現れた！！')
                    await info_channel.send(after.channel.name + 'に' + member.name + 'が現れた！！')
            except:
                print ("Channel is None")

#intents = discord.Intents.default()
intents = discord.Intents.all()
intents.message_content = True
intents.voice_states = True

client = MyClient(intents=intents)
client.run(TOKEN)