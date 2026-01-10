import telebot
import os
import requests
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from deep_translator import GoogleTranslator

# Bot TOKEN
TOKEN = '8267155928:AAHjwuV8UzktREiy1m36dlL1hU92wvdyLlw'
bot = telebot.TeleBot(TOKEN)

def get_image(query):
    # Render-da rasmlar bloklanmaydi
    url = f"https://source.unsplash.com/featured/800x600?{query.replace(' ', ',')}"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            with open("slayd_img.jpg", "wb") as f:
                f.write(res.content)
            return "slayd_img.jpg"
    except:
        return None
    return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🌟 **Gamma AI Slayd Botga xush kelibsiz!**\nMavzuni yuboring va men 15 sahifali premium slayd tayyorlayman.")

@bot.message_handler(func=lambda m: True)
def create_presentation(message):
    mavzu_uz = message.text
    bot.reply_to(message, f"🚀 '{mavzu_uz}' bo'yicha slayd yaratilmoqda...")
    
    try:
        prs = Presentation()
        prs.slide_width, prs.slide_height = Inches(13.33), Inches(7.5) # 16:9 format
        
        reja = ["Kirish", "Tarixi", "Asosiy qism", "Dolzarbligi", "Innovatsiyalar", "Afzalliklar", "Global tajriba", "Muammolar", "Yechimlar", "Faktlar", "Statistika", "Tahlil", "Kelajak", "Xulosa", "Rahmat"]

        for i, qism in enumerate(reja):
            slide = prs.slides.add_slide(prs.slide_layouts[5])
            # Gamma AI uslubidagi to'q fon
            fill = slide.background.fill
            fill.solid()
            fill.fore_color.rgb = RGBColor(10, 20, 40)

            # Sarlavha
            title = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(1))
            p = title.text_frame.paragraphs[0]
            p.text = f"{i+1}. {qism}: {mavzu_uz}"
            p.font.bold, p.font.size = True, Pt(32)
            p.font.color.rgb = RGBColor(0, 255, 200)

            # Matn
            body = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(6), Inches(5))
            tf = body.text_frame
            tf.word_wrap = True
            cp = tf.paragraphs[0]
            cp.text = f"{mavzu_uz} bo'yicha {qism.lower()} tahlili va muhim ma'lumotlar."
            cp.font.size, cp.font.color.rgb = Pt(22), RGBColor(255, 255, 255)

            # Rasm (O'ngda)
            img = get_image(f"{mavzu_uz} {qism}")
            if img:
                slide.shapes.add_picture(img, Inches(7), Inches(1.2), Inches(5.8), Inches(5.5))

        fayl_nomi = f"Slayd_{message.chat.id}.pptx"
        prs.save(fayl_nomi)
        with open(fayl_nomi, 'rb') as f:
            bot.send_document(message.chat.id, f, caption="✅ Slaydingiz tayyor!")
        os.remove(fayl_nomi)
        if os.path.exists("slayd_img.jpg"): os.remove("slayd_img.jpg")
        
    except Exception as e:
        bot.reply_to(message, "Xatolik yuz berdi, qayta urinib ko'ring.")

print("Bot ishga tushdi...")
bot.infinity_polling()
