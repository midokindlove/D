import discord
from discord import app_commands
from discord.ext import commands
import requests
import os

# جلب المفاتيح من Secrets
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# التحقق من وجود المفاتيح
if not DISCORD_TOKEN or not DEEPSEEK_API_KEY or not YOUTUBE_API_KEY:
    raise ValueError("⚠️ تأكد من إضافة المفاتيح إلى Secrets!")

# إعداد Intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

# إنشاء البوت
bot = commands.Bot(command_prefix="/", intents=intents)

# حفظ قناة الرد التلقائي
channel_id = None

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

# أمر لتحديد القناة
@bot.tree.command(name="setchannel", description="حدد القناة التي يعمل فيها البوت")
@app_commands.describe(channel="اختر القناة")
async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    global channel_id
    channel_id = channel.id
    await interaction.response.send_message(f"✅ تم تعيين القناة: {channel.mention}")

# أمر للبحث في يوتيوب
@bot.tree.command(name="youtube", description="ابحث في YouTube عن فيديو")
@app_commands.describe(query="ما الذي تريد البحث عنه؟")
async def youtube(interaction: discord.Interaction, query: str):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "maxResults": 1,
        "type": "video"
    }
    response = requests.get(url, params=params).json()

    if "items" in response and len(response["items"]) > 0:
        item = response["items"][0]
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        link = f"https://www.youtube.com/watch?v={video_id}"
        await interaction.response.send_message(f"🎬 **{title}**\n🔗 {link}")
    else:
        await interaction.response.send_message("❌ لم يتم العثور على نتائج.")

# الرد التلقائي في القناة المحددة باستخدام DeepSeek
@bot.event
async def on_message(message):
    global channel_id
    if message.author.bot or message.channel.id != channel_id:
        return

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": message.content}]
    }

    try:
        res = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data)
        res_json = res.json()

        if "choices" in res_json:
            reply = res_json["choices"][0]["message"]["content"]
            await message.reply(f"{message.author.mention} {reply}")
        else:
            await message.reply("❌ لم أتمكن من الرد.")

    except Exception as e:
        print(f"Error: {e}")
        await message.reply("❌ حدث خطأ غير متوقع.")

    await bot.process_commands(message)

# تشغيل البوت
bot.run(DISCORD_TOKEN)
