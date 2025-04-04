import discord
from discord import app_commands
from discord.ext import commands
import openai
import os
import requests

# بيئة آمنة لتخزين المفاتيح
DISCORD_TOKEN = os.getenv("MTM1NzYzMTkxMTA4MTgwNzk2Mw.G-Jeh0.NlH-ohqCVGJTs20BPdSvJfl0fX7pBK956LgAX8")
OPENAI_API_KEY = os.getenv("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
")
YOUTUBE_API_KEY = os.getenv("AIzaSyCCJjW6FpqPumWZW5B7DjVfU7PG9dzMiSQ")
ALLOWED_CHANNEL_ID = 1234567890  # استبدله بـ ID القناة الخاصة بك

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# أمر الدردشة مع GPT
@bot.tree.command(name="ask", description="اكتب سؤالك للذكاء الاصطناعي")
@app_commands.describe(prompt="ما هو سؤالك؟")
async def ask(interaction: discord.Interaction, prompt: str):
    if interaction.channel.id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message("❌ هذا الأمر غير مسموح في هذه القناة.", ephemeral=True)
        return

    await interaction.response.defer()
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        answer = response["choices"][0]["message"]["content"]
        await interaction.followup.send(f"🤖: {answer}")
    except Exception as e:
        await interaction.followup.send("حدث خطأ أثناء التواصل مع OpenAI.")
        print(e)

# أمر البحث في يوتيوب
@bot.tree.command(name="youtube", description="ابحث في يوتيوب")
@app_commands.describe(query="ما الذي تريد البحث عنه؟")
async def youtube(interaction: discord.Interaction, query: str):
    if interaction.channel.id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message("❌ هذا الأمر غير مسموح في هذه القناة.", ephemeral=True)
        return

    await interaction.response.defer()
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "key": YOUTUBE_API_KEY,
            "maxResults": 3
        }
        response = requests.get(url, params=params)
        data = response.json()

        if "items" not in data or len(data["items"]) == 0:
            await interaction.followup.send("❌ لا توجد نتائج.")
            return

        results = ""
        for item in data["items"]:
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            results += f"**{title}**\n{video_url}\n\n"

        await interaction.followup.send(f"🔍 نتائج البحث:\n{results}")
    except Exception as e:
        await interaction.followup.send("حدث خطأ أثناء البحث في يوتيوب.")
        print(e)

bot.run(DISCORD_TOKEN)
