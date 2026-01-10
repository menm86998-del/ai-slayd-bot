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
    """Render-da rasmlarni qidirish funksiyasi"""
    try:
        # Unsplash inglizcha so'rovlarda yaxshi ishlaydi
        translated = GoogleTranslator(source='auto', target='en').translate(query)
        search_word = translated.split()[-1]
        
        # Render-da bloklanmaydigan rasm manbasi
        url = f"https://source.unsplash.com/featured/800x600?{search_word}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        res = requests.get(url, headers=headers, timeout=20)
        if res.status_code == 200:
            file_path = "temp_pic.jpg"
            with open(file_path, "wb") as f:
                f.write(res.content)
            return file_path
    except:
        return None
    return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🌟 **Gamma AI Slayd Botga xush kelibsiz!**\nMavzuni yuboring va men rasmli premium slayd tayyorlayman.")

@bot.message_handler(func=lambda m: True)
def create_presentation(message):
    mavzu_uz = message.text
    
    # ADMINGA BILDIRISHNOMA (Sizga xabar yuboradi)
    try:
        user_info = f"👤 Foydalanuvchi: {message.from_user.first_name}\n🆔 ID: {message.from_user.id}\n📝 Mavzu: {mavzu_uz}"
        bot.send_message(ADMIN_ID, f"🔔 **Yangi buyurtma keldi:**\n\n{user_info}")
    except:
        pass

    bot.reply_to(message, f"🚀 '{mavzu_uz}' bo'yicha rasmli slayd yaratilmoqda...")
    
    try:
        prs = Presentation()
        # 16:9 format
        prs.slide_width, prs.slide_height = Inches(13.33), Inches(7.5)
        
        reja = ["Kirish", "Asosiy tushunchalar", "Tarixi", "Innovatsiyalar", "Xulosa"]

        for i, qism in enumerate(reja):
            slide = prs.slides.add_slide(prs.slide_layouts[5])
            
            # Gamma AI uslubidagi to'q fon
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
            cp.text = f"{mavzu_uz} haqida {qism.lower()} tahlili va muhim faktlar."
            cp.font.size, cp.font.color.rgb = Pt(24), RGBColor(255, 255, 255)

        # Faylni saqlash va yuborish
        fayl_nomi = f"Slayd_{message.chat.id}.pptx"
        prs.save(fayl_nomi)
        with open(fayl_nomi, 'rb') as f:
            bot.send_document(message.chat.id, f, caption="✅ Slaydingiz tayyor!")
        
        # Tozalash
        os.remove(fayl_nomi)
        if os.path.exists("temp_pic.jpg"): os.remove("temp_pic.jpg")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Xatolik yuz berdi: {str(e)}")

print("Bot Render serverida muvaffaqiyatli ishga tushdi...")
bot.infinity_polling()





