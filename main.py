import telebot
import os
import requests
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from transformers import pipeline
from deep_translator import GoogleTranslator

# Sozlamalar
TOKEN = '8267155928:AAHjwuV8UzktREiy1m36dlL1hU92wvdyLlw'
bot = telebot.TeleBot(TOKEN)

print("Gamma AI tizimi yuklanmoqda...")
generator = pipeline('text-generation', model='distilgpt2')
translator_to_en = GoogleTranslator(source='uz', target='en')
translator_to_uz = GoogleTranslator(source='en', target='uz')

def get_image(query):
    """Mavzuga mos HD rasm topish"""
    url = f"https://source.unsplash.com/1600x900/?{query.replace(' ', ',')}"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            with open("gamma_img.jpg", "wb") as f:
                f.write(res.content)
            return "gamma_img.jpg"
    except: return None
    return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🌟 **Gamma AI Slayd Botga xush kelibsiz!**\nMavzuni yuboring, men sizga 15 sahifali premium taqdimot tayyorlab beraman.")

@bot.message_handler(func=lambda m: True)
def generate_presentation(message):
    mavzu_uz = message.text
    bot.reply_to(message, f"🚀 '{mavzu_uz}' mavzusida Gamma AI uslubida slayd yaratilmoqda...")

    try:
        prs = Presentation()
        # Slayd o'lchamini 16:9 (keng ekran) qilish
        prs.slide_width = Inches(13.33)
        prs.slide_height = Inches(7.5)

        reja = ["Kirish", "Asosiy tushunchalar", "Strategiya", "Tahlil", "Innovatsiya", "Global tajriba", "Afzalliklar", "Kamchiliklar", "Yechimlar", "Statistika", "Kelajak", "Xulosa", "Savollar", "Kontaktlar", "Rahmat"]

        for i, qism in enumerate(reja):
            slide = prs.slides.add_slide(prs.slide_layouts[5]) # Bo'sh layout (Blank)
            
            # 1. Premium Fon (Gradient ko'rinishida to'q rang)
            fill = slide.background.fill
            fill.solid()
            fill.fore_color.rgb = RGBColor(15, 20, 35)

            # 2. Sarlavha (Gamma uslubida)
            title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(1))
            tf = title_box.text_frame
            p = tf.paragraphs[0]
            p.text = f"{i+1}. {qism}: {mavzu_uz}"
            p.font.bold = True
            p.font.size = Pt(32)
            p.font.color.rgb = RGBColor(0, 200, 255) # Neon ko'k

            # 3. AI Matn (Qisqa va lo'nda)
            mavzu_en = translator_to_en.translate(f"Key points about {mavzu_uz} in {qism}")
            res = generator(mavzu_en, max_new_tokens=50, num_return_sequences=1)
            matn_uz = translator_to_uz.translate(res[0]['generated_text'])

            content_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(6), Inches(5))
            ctf = content_box.text_frame
            ctf.word_wrap = True
            cp = ctf.paragraphs[0]
            cp.text = matn_uz
            cp.font.size = Pt(18)
            cp.font.color.rgb = RGBColor(255, 255, 255)

            # 4. HD Rasm (O'ng tomonda katta)
            img = get_image(f"{mavzu_uz} {qism}")
            if img:
                slide.shapes.add_picture(img, Inches(7), Inches(1.2), Inches(5.5), Inches(5.5))

        fayl = f"Gamma_{message.chat.id}.pptx"
        prs.save(fayl)
        with open(fayl, 'rb') as f:
            bot.send_document(message.chat.id, f, caption="✅ Gamma AI darajasidagi taqdimotingiz tayyor!")
        os.remove(fayl)

    except Exception as e:
        bot.reply_to(message, "Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")

bot.infinity_polling()