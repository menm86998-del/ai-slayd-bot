import telebot
import os
import requests
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# Bot TOKEN
TOKEN = '8267155928:AAHjwuV8UzktREiy1m36dlL1hU92wvdyLlw'
bot = telebot.TeleBot(TOKEN)

def get_image(query):
    # So'rovni soddalashtiramiz (faqat oxirgi so'z)
    search_word = query.split()[-1]
    url = f"https://source.unsplash.com/featured/800x600?{search_word}"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=20)
        if res.status_code == 200:
            with open("temp_pic.jpg", "wb") as f:
                f.write(res.content)
            return "temp_pic.jpg"
    except:
        return None
    return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🌟 **Gamma AI Slayd Bot!**\nMavzuni yuboring va men rasmli premium slayd tayyorlayman.")

@bot.message_handler(func=lambda m: True)
def create_presentation(message):
    mavzu = message.text
    bot.reply_to(message, f"🚀 '{mavzu}' bo'yicha slayd yaratilmoqda...")
    
    try:
        prs = Presentation()
        prs.slide_width, prs.slide_height = Inches(13.33), Inches(7.5)
        reja = ["Kirish", "Asosiy tushunchalar", "Tarixi", "Dolzarbligi", "Innovatsiyalar", "Xulosa"]

        for i, qism in enumerate(reja):
            slide = prs.slides.add_slide(prs.slide_layouts[5])
            # To'q fon
            slide.background.fill.solid()
            slide.background.fill.fore_color.rgb = RGBColor(15, 20, 35)

            # Sarlavha
            title = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(1))
            p = title.text_frame.paragraphs[0]
            p.text = f"{i+1}. {qism}"
            p.font.bold, p.font.size = True, Pt(36)
            p.font.color.rgb = RGBColor(0, 255, 200)

            # Rasm (O'ngda)
            img = get_image(f"{mavzu} {qism}")
            if img:
                slide.shapes.add_picture(img, Inches(7.2), Inches(1.2), Inches(5.8), Inches(5.5))
            
            # Matn (Chapda)
            body = slide.shapes.add_textbox(Inches(0.5), Inches(1.8), Inches(6.5), Inches(5))
            tf = body.text_frame
            tf.word_wrap = True
            cp = tf.paragraphs[0]
            cp.text = f"{mavzu} mavzusida {qism.lower()} bo'yicha tahliliy ma'lumotlar."
            cp.font.size, cp.font.color.rgb = Pt(24), RGBColor(255, 255, 255)

        fayl_nomi = f"Slayd_{message.chat.id}.pptx"
        prs.save(fayl_nomi)
        with open(fayl_nomi, 'rb') as f:
            bot.send_document(message.chat.id, f, caption="✅ Slaydingiz rasmlari bilan tayyor!")
        os.remove(fayl_nomi)
        if os.path.exists("temp_pic.jpg"): os.remove("temp_pic.jpg")
    except Exception as e:
        bot.reply_to(message, f"Xato: {e}")

bot.infinity_polling()


