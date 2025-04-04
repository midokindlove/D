import discord
from discord import app_commands
from discord.ext import commands
import os
from deepseek_api import DeepSeekAPI  # ستحتاج لتنفيذ هذه الواجهة

# تحميل المتغيرات السرية من Secrets
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', None)  # اختياري

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# تهيئة واجهة DeepSeek
deepseek = DeepSeekAPI(DEEPSEEK_API_KEY)

@bot.event
async def on_ready():
    print(f'تم تسجيل الدخول كـ {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"تم مزامنة {len(synced)} أوامر.")
    except Exception as e:
        print(f"خطأ في مزامنة الأوامر: {e}")

@bot.tree.command(name="ask", description="اطرح سؤالاً على الذكاء الاصطناعي")
@app_commands.describe(question="السؤال الذي تريد طرحه")
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer()
    try:
        response = deepseek.ask_question(question)
        await interaction.followup.send(f"**سؤال:** {question}\n**إجابة:** {response}")
    except Exception as e:
        await interaction.followup.send(f"حدث خطأ أثناء معالجة سؤالك: {str(e)}")

# أوامر للمسؤولين فقط
@bot.tree.command(name="setup", description="إعداد البوت للروم الحالي (للمسؤولين فقط)")
@app_commands.default_permissions(administrator=True)
async def setup(interaction: discord.Interaction):
    try:
        # هنا يمكنك إضافة أي إعدادات مخصصة
        await interaction.response.send_message("تم إعداد البوت لهذه الغرفة بنجاح!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"حدث خطأ: {str(e)}", ephemeral=True)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
