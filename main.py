import telebot
import os
import requests
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from deep_translator import GoogleTranslator

# YANGI TOKEN
TOKEN = '8267155928:AAE-eFbk4is17eVcppcvxINEWEXUgZVYI9o'
ADMIN_ID = 6876356711 
bot = telebot.TeleBot(TOKEN)

def get_image(query):
    """Render-da ishlaydigan va rasmlarni topadigan funksiya"""
    try:
        # Unsplash uchun qidiruvni inglizchaga o'giramiz
        translated = GoogleTranslator(source='auto', target='en').translate(query)
        search_word = translated.split()[-1]
        
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
    bot.reply_to(message, "🌟 **Gamma AI Slayd Bot!**\nMavzuni yuboring va men rasmli premium slayd tayyorlayman.")

@bot.message_handler(func=lambda m: True)
def create_presentation(message):
    mavzu_uz = message.text
    
    # ADMINGA BILDIRISHNOMA YUBORISH
    try:
        user_info = f"👤 Ism: {message.from_user.first_name}\n" \
                    f"🆔 ID: {message.from_user.id}\n" \
                    f"📝 Mavzu: {mavzu_uz}"
        bot.send_message(ADMIN_ID, f"🔔 **Yangi buyurtma:**\n\n{user_info}")
    except:
        pass

    bot.reply_to(message, f"🚀 '{mavzu_uz}' bo'yicha rasmli slayd yaratilmoqda...")
    
    try:
        prs = Presentation()
        prs.slide_width, prs.slide_height = Inches(13.33), Inches(7.5)
        
        # Slayd rejalari
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
                slide.





