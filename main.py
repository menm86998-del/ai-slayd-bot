import telebot
import os
import requests
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from deep_translator import GoogleTranslator

# BOT SOZLAMALARI
TOKEN = '8267155928:AAFejnBDo_o_KgM3bY5DMzcWSP3ZBseMk9k'
ADMIN_ID = 7291844509 
bot = telebot.TeleBot(TOKEN)

def get_image(query):
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(query)
        search_word = translated.split()[-1]
        url = f"https://source.unsplash.com/1200x800/?{search_word}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=20)
        if res.status_code == 200:
            path = "temp_img.jpg"
            with open(path, "wb") as f: f.write(res.content)
            return path
    except: return None

@bot.message_handler(func=lambda m: True)
def create_ppt(message):
    mavzu = message.text
    try: bot.send_message(ADMIN_ID, f"🔔 15 betlik buyurtma: {mavzu}\n👤 {message.from_user.first_name}")
    except: pass

    bot.reply_to(message, f"🚀 '{mavzu}' bo'yicha 15 betlik premium slayd tayyorlanmoqda. Bu biroz vaqt olishi mumkin...")
    
    try:
        prs = Presentation()
        prs.slide_width, prs.slide_height = Inches(13.33), Inches(7.5)
        
        # 15 ta bo'limdan iborat reja
        reja = [
            "Kirish", "Mavzuning dolzarbligi", "Asosiy maqsadlar", "Tarixiy fon", 
            "Joriy holat tahlili", "Asosiy tushunchalar", "Statistik ma'lumotlar", 
            "Muammolar va to'siqlar", "Innovatsion yechimlar", "Xalqaro tajriba", 
            "Amaliy misollar", "Kelajakdagi istiqbollar", "Kutilayotgan natijalar", 
            "Xulosa", "Foydalanilgan adabiyotlar"
        ]

        for i, qism in enumerate(reja):
            slide = prs.slides.add_slide(prs.slide_layouts[5])
            slide.background.fill.solid()
            slide.background.fill.fore_color.rgb = RGBColor(10, 15, 30) # Gamma AI foni

            # Sarlavha
            title = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(1))
            p = title.text_frame.paragraphs[0]
            p.text = f"{i+1}. {qism}"
            p.font.bold, p.font.size, p.font.color.rgb = True, Pt(36), RGBColor(0, 255, 180)

            # Rasm va Matnni joylashtirish (Har xil uslubda)
            img = get_image(f"{mavzu} {qism}")
            
            if i % 2 == 0: # Juft betlarda: Matn chapda, Rasm o'ngda
                if img: slide.shapes.add_picture(img, Inches(7.2), Inches(1.5), Inches(5.8), Inches(5.0))
                body_pos = (Inches(0.5), Inches(1.8), Inches(6.0), Inches(5))
            else: # Toq betlarda: Rasm chapda, Matn o'ngda
                if img: slide.shapes.add_picture(img, Inches(0.5), Inches(1.5), Inches(5.8), Inches(5.0))
                body_pos = (Inches(6.8), Inches(1.8), Inches(6.0), Inches(5))

            body = slide.shapes.add_textbox(*body_pos)
            btf = body.text_frame
            btf.word_wrap = True
            cp = btf.paragraphs[0]
            cp.text = f"{mavzu} haqida batafsil ma'lumot: {qism.lower()} bo'yicha ilmiy va amaliy tahlillar."
            cp.font.size, cp.font.color.rgb = Pt(22), RGBColor(255, 255, 255)

        name = f"Gamma_15_{message.chat.id}.pptx"
        prs.save(name)
        with open(name, 'rb') as f: bot.send_document(message.chat.id, f, caption=f"✅ '{mavzu}' mavzusida 15 betlik premium slayd tayyor!")
        os.remove(name)
        if os.path.exists("temp_img.jpg"): os.remove("temp_img.jpg")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Xato: {str(e)}")

bot.infinity_polling()





