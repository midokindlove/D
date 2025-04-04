import os
import discord
from discord.ext import commands

# استرجاع التوكن من GitHub Secrets
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# تأكد من أن التوكن تم تحميله
if not DISCORD_TOKEN:
    raise ValueError("⚠️  DISCORD_TOKEN غير موجود! تأكد من إضافته إلى GitHub Secrets.")

# إنشاء البوت
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# تشغيل البوت
bot.run(DISCORD_TOKEN)
