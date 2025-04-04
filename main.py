import discord
from discord import app_commands
from discord.ext import commands
import requests
import os

# جلب القيم من GitHub Secrets
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# التأكد من تحميل التوكنات
if not DISCORD_TOKEN or not DEEPSEEK_API_KEY or not YOUTUBE_API_KEY:
    raise ValueError("⚠️ تأكد من إضافة التوكنات إلى GitHub Secrets!")

# إنشاء البوت مع السماح بجميع الـ Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# تخزين القناة المحددة
channel_id = None

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

# أمر لاختيار القناة التي يعمل بها البوت
@bot.tree.command(name="setchannel", description="حدد القناة التي سيعمل فيها البوت")
@app_commands.describe(channel="اختر القناة")
async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    global channel_id
    channel_id = channel.id
    await interaction.response.send_message(f"✅ تم تحديد القناة: {channel.mention}")

# أمر للبحث في يوتيوب
@bot.tree.command(name="youtube", description="ابحث في YouTube عن فيديو معين")
@app_commands.describe(query="ما الذي تريد البحث عنه؟")
async def youtube(interaction: discord.Interaction, query: str):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "maxResults": 1,
        "type": "video"
    }
    
    response = requests.get(search_url, params=params).json()
    
    if "items" in response and len(response["items"]) > 0:
        video_id = response["items"][0]["id"]["videoId"]
        video_title = response["items"][0]["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        await interaction.response.send_message(f"🎬 **{video_title}**\n🔗 {video_url}")
    else:
        await interaction.response.send_message("❌ لم يتم العثور على نتائج.")

# الرد التلقائي في القناة المحددة باستخدام DeepSeek API
@bot.event
async def on_message(message):
    global channel_id
    if message.author.bot:
        return

    if channel_id is not None and message.channel.id == channel_id:
        try:
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": message.content}]
            }
            response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data)
            response_json = response.json()

            if "choices" in response_json:
                bot_reply = response_json["choices"][0]["message"]["content"]
                await message.reply(f"{message.author.mention} {bot_reply}")
            else:
                await message.reply("❌ لم أتمكن من معالجة طلبك، حاول مرة أخرى.")

        except Exception as e:
            print(f"❌ Error: {e}")
            await message.reply("❌ حدث خطأ غير متوقع. يرجى المحاولة لاحقًا.")

    await bot.process_commands(message)

# تشغيل البوت
bot.run(DISCORD_TOKEN)
