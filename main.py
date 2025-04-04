import discord
from discord import app_commands
from discord.ext import commands
import requests
import os

# تحميل التوكنات من Secrets
DISCORD_TOKEN = os.getenv("MTM1NzYzMTkxMTA4MTgwNzk2Mw.G8MACo.V1TGERnwUttam0qZpbs8KsFD8MXxTXXXnX3LpE")
DEEPSEEK_API_KEY = os.getenv("sk-0b82e54648b94ceb8b4d674d23096e5b")
YOUTUBE_API_KEY = os.getenv("AIzaSyCCJjW6FpqPumWZW5B7DjVfU7PG9dzMiSQ")

# التحقق من وجود التوكنات
if not DISCORD_TOKEN or not DEEPSEEK_API_KEY or not YOUTUBE_API_KEY:
    raise ValueError("⚠️ تأكد من إضافة التوكنات إلى Secrets!")

# إعداد Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# إنشاء البوت
bot = commands.Bot(command_prefix="/", intents=intents)

# متغير لتخزين ID الروم المحددة
channel_id = None_
