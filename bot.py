import os
import time
from flask import Flask
from threading import Thread
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from playwright.sync_api import sync_playwright

# 1. Manter o servidor vivo (Render)
app = Flask('')
@app.route('/')
def home(): return "Bot Aviator Online!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
Thread(target=run).start()

# 2. Lógica do Bot
def main():
    bot = Bot(token=os.getenv("TOKEN"))
    chat_id = os.getenv("CHAT_ID")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page()
        
        print("🔗 Acedendo à BantuBet...")
        page.goto("https://www.bantubet.co.ao/casino/game/aviator")
        page.wait_for_timeout(20000) # Aguarda carregamento do jogo
        
        print("✅ Bot iniciado com sucesso!")
        bot.send_message(chat_id=chat_id, text="🚀 *BOT AVIATOR ATIVO E A MONITORIZAR*")
        
        while True:
            try:
                # Procura por elementos que indicam odds no jogo
                # Nota: Este seletor pode precisar de ajuste dependendo do layout do jogo
                elemento = page.query_selector(".payouts-block")
                if elemento:
                    odd = elemento.inner_text()
                    teclado = [[InlineKeyboardButton("GERAR PREVISÃO", callback_data='gerar')]]
                    markup = InlineKeyboardMarkup(teclado)
                    
                    bot.send_message(
                        chat_id=chat_id, 
                        text=f"📊 *Última Odd:* {odd}\n\n🔍 A analisar próxima rodada...",
                        parse_mode='Markdown',
                        reply_markup=markup
                    )
            except Exception as e:
                print(f"Erro na leitura: {e}")
            
            # Pausa de segurança para não sobrecarregar o site
            page.wait_for_timeout(60000) 

if __name__ == "__main__":
    main()
    
