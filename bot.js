const { Client, GatewayIntentBits } = require('discord.js');
const { OpenAI } = require('openai');

// ✅ أدخل المفاتيح هنا مباشرة (غير آمن، لكن حسب طلبك)
const DISCORD_TOKEN = 'ضع_توكن_Discord_هنا';
const OPENAI_API_KEY = 'ضع_مفتاح_OpenAI_هنا';

// إعداد البوت
const client = new Client({
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent]
});

// إعداد OpenAI
const openai = new OpenAI({ apiKey: OPENAI_API_KEY });

// عند تشغيل البوت
client.once('ready', () => {
  console.log(`✅ البوت شغّال: ${client.user.tag}`);
});

// الرد على الرسائل
client.on('messageCreate', async message => {
  if (message.author.bot) return;
  if (!message.content.startsWith('!ai')) return;

  const prompt = message.content.slice(3).trim();
  if (!prompt) return message.reply("📝 اكتب شيئًا بعد !ai");

  await message.channel.send("🤖 جارٍ التفكير...");

  try {
    const chatCompletion = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: [{ role: 'user', content: prompt }]
    });

    const reply = chatCompletion.choices[0].message.content;
    message.reply(reply);
  } catch (err) {
    console.error(err);
    message.reply("❌ حدث خطأ أثناء الاتصال بـ OpenAI");
  }
});

// تشغيل البوت
client.login(DISCORD_TOKEN);
