import os
from flask import Flask
from threading import Thread
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from playwright.sync_api import sync_playwright

# Servidor Flask para manter o Render vivo
app = Flask('')
@app.route('/')
def home(): return "Bot Aviator Online!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
Thread(target=run).start()

# Botão Pro
def enviar_previsao(bot, chat_id, odd):
    teclado = [[InlineKeyboardButton("GERAR NOVA PREVISÃO", callback_data='gerar')]]
    markup = InlineKeyboardMarkup(teclado)
    bot.send_message(chat_id=chat_id, text=f"🚀 *NOVA PREVISÃO AVIATOR*\n\n🎯 Odd sugerida: {odd}\n⚡️ Confiança: 98%", parse_mode='Markdown', reply_markup=markup)

def main():
    bot = Bot(token=os.getenv("TOKEN"))
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto("https://www.bantubet.co.ao/casino/game/aviator")
        
        print("Bot Aviator Iniciado...")
        while True:
            # Aqui monitorizamos o histórico
            historico = page.query_selector(".payouts-block")
            if historico:
                odd = historico.inner_text().split()[0]
                enviar_previsao(bot, os.getenv("CHAT_ID"), odd)
            page.wait_for_timeout(30000) # Monitoriza a cada 30s

if __name__ == "__main__":
    main()

