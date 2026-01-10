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
    """Render-da ishlaydigan va rasmlarni topadigan funksiya"""
    try:
        # Unsplash inglizcha so'rovlarda yaxshi ishlaydi
        translated = GoogleTranslator(source='auto', target='en').translate(query)
        search_word = translated.split()[-1] # Eng muhim so'zni olamiz
        
        # Render-da bloklanmaydigan rasm manbasi
        url = f"https://source.unsplash.com/featured/800x600?{search_word}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        res = requests.get(url, headers=headers, timeout=20)
        if res.status_code == 200:
            file_path = "temp_pic.jpg"
            with open(file_path, "wb") as f:
                f.write(res.content)
            return file_path
    except Exception as e:
        print(f"Rasm yuklashda xato: {e}")
    return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🌟 **Gamma AI Slayd Botga xush kelibsiz!**\nMavzuni yuboring va men rasmli premium slayd tayyorlayman.")

@bot.message_handler(func=lambda m: True)
def create_presentation(message):
    mavzu_uz = message.text
    bot.reply_to(message, f"🚀 '{mavzu_uz}' bo'yicha rasmli slayd yaratilmoqda...")
    
    try:
        prs = Presentation()
        # 16:9 format
        prs.slide_width, prs.slide_height = Inches(13.33), Inches(7.5)
        
        reja = ["Kirish", "Asosiy maqsad", "Tarixi", "Tahlil", "Innovatsiyalar", "Xulosa"]

        for i, qism in enumerate(reja):
            slide = prs.slides.add_slide(prs.slide_layouts[5])
            
            # Gamma AI uslubidagi to'q fon (RGB: 15, 20, 35)
            fill = slide.background.fill
            fill.solid()
            fill.fore_color.rgb = RGBColor(15, 20, 35)

            # Sarlavha (Neon yashil rangda)
            title = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(1))
            p = title.text_frame.paragraphs[0]
            p.text = f"{i+1}. {qism}: {mavzu_uz}"
            p.font.bold, p.font.size = True, Pt(34)
            p.font.color.rgb = RGBColor(0, 255, 180)

            # Rasm qidirish va qo'shish (O'ng tomonda)
            img_path = get_image(f"{mavzu_uz} {qism}")
            if img_path and os.path.exists(img_path):
                slide.shapes.add_picture(img_path, Inches(7.2), Inches(1.2), Inches(5.8), Inches(5.5))

            # Matn (Chap tomonda)
            body = slide.shapes.add_textbox(Inches(0.5), Inches(1.8), Inches(6.5), Inches(5))
            tf = body.text_frame
            tf.word_wrap = True
            cp = tf.paragraphs[0]
            cp.text = f"{mavzu_uz} mavzusining {qism.lower()} qismi bo'yicha muhim faktlar va tahliliy ma'lumotlar."
            cp.font.size, cp.font.color.rgb = Pt(24), RGBColor(255, 255, 255)

        # Faylni saqlash va yuborish
        fayl_nomi = f"Slayd_{message.chat.id}.pptx"
        prs.save(fayl_nomi)
        with open(fayl_nomi, 'rb') as f:
            bot.send_document(message.chat.id, f, caption="✅ Slaydingiz rasmlari bilan tayyor!")
        
        # Tozalash
        os.remove(fayl_nomi)
        if os.path.exists("temp_pic.jpg"): 
            os.remove("temp_pic.jpg")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Xatolik: {str(e)}")

print("Bot Render serverida ishga tushdi...")
bot.infinity_polling()



