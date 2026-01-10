import telebot
import os
import requests
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from deep_translator import GoogleTranslator

# BOT SOZLAMALARI
TOKEN = '8267155928:AAE-eFbk4is17eVcppcvxINEWEXUgZVYI9o'
ADMIN_ID = 7291844509 
bot = telebot.TeleBot(TOKEN)

def get_image(query):
    """Mavzuga mos yuqori sifatli rasm topish"""
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(query)
        search_word = translated.split()[-1]
        # Unsplash API orqali professional fotosuratlar
        url = f"https://source.unsplash.com/1200x800/?{search_word}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=20)
        if res.status_code == 200:
            path = "temp_img.jpg"
            with open(path, "wb") as f: f.write(res.content)
            return path
    except: return None
    return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🌟 **Gamma AI Slayd Bot!**\nMavzuni yuboring va men professional dizayndagi rasmli slayd tayyorlayman.")

@bot.message_handler(func=lambda m: True)
def create_ppt(message):
    mavzu = message.text
    # Adminga bildirishnoma
    try: bot.send_message(ADMIN_ID, f"🔔 **Yangi slayd:**\n👤 {message.from_user.first_name}\n📝 Mavzu: {mavzu}")
    except: pass

    bot.reply_to(message, f"🚀 '{mavzu}' ustida Gamma AI uslubida ishlayapman...")
    
    try:
        prs = Presentation()
        prs.slide_width, prs.slide_height = Inches(13.33), Inches(7.5) # 16:9 keng format
        
        reja = ["Kirish va Umumiy tahlil", "Tarixiy rivojlanish", "Asosiy xususiyatlar", "Innovatsion yechimlar", "Xulosa va Istiqbollar"]

        for i, qism in enumerate(reja):
            slide = prs.slides.add_slide(prs.slide_layouts[5])
            
            # Gamma AI kabi to'q va zamonaviy fon
            bg = slide.background.fill
            bg.solid()
            bg.fore_color.rgb = RGBColor(10, 15, 30)

            # Sarlavha (Neon dizayn)
            title = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(1))
            tf = title.text_frame
            p = tf.paragraphs[0]
            p.text = f"{i+1}. {qism}"
            p.font.bold, p.font.size = True, Pt(40)
            p.font.color.rgb = RGBColor(0, 255, 180) # Neon yashil

            # Rasm (Gamma kabi o'ng tomonda katta va sifatli)
            img = get_image(f"{mavzu} {qism}")
            if img:
                slide.shapes.add_picture(img, Inches(7.0), Inches(1.2), Inches(6.0), Inches(5.8))

            # Matn bloklari (Chap tomonda)
            body = slide.shapes.add_textbox(Inches(0.5), Inches(1.8), Inches(6.0), Inches(5))
            btf = body.text_frame
            btf.word_wrap = True
            cp = btf.paragraphs[0]
            cp.text = f"➤ {mavzu} mavzusining {qism.lower()} qismi bo'yicha tahliliy ma'lumotlar.\n\n➤ Ushbu sohadagi eng so'nggi yangiliklar va faktlar to'plami."
            cp.font.size, cp.font.color.rgb = Pt(26), RGBColor(240, 240, 240)

        name = f"Gamma_{message.chat.id}.pptx"
        prs.save(name)
        with open(name, 'rb') as f:
            bot.send_document(message.chat.id, f, caption=f"✅ '{mavzu}' bo'yicha professional slayd tayyor!")
        
        os.remove(name)
        if os.path.exists("temp_img.jpg"): os.remove("temp_img.jpg")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Xato: {str(e)}")

print("Bot Render-da Gamma AI rejimida ishga tushdi...")
bot.infinity_polling()





