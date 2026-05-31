import os
import sys
from flask import Flask
from threading import Thread
from telegram import Bot
from playwright.sync_api import sync_playwright

# 1. Servidor Flask para manter o bot "Live"
app = Flask('')
@app.route('/')
def home(): return "Bot Vivo!"
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

def main():
    bot = Bot(token=os.getenv("TOKEN"))
    chat_id = os.getenv("CHAT_ID")
    
    # 2. Inicia o Playwright e encontra o navegador automaticamente
    with sync_playwright() as p:
        # Tenta lançar o navegador sem especificar caminho fixo (o Playwright procura sozinho)
        try:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-gpu"])
            page = browser.new_page()
            
            bot.send_message(chat_id=chat_id, text="✅ Bot ligado! Acedendo à BantuBet...")
            page.goto("https://www.bantubet.co.ao/casino/game/aviator")
            page.wait_for_timeout(10000)
            
            bot.send_message(chat_id=chat_id, text="🚀 Monitorização iniciada com sucesso!")
            
            while True:
                # Loop de monitorização básica
                page.wait_for_timeout(30000)
                
        except Exception as e:
            bot.send_message(chat_id=chat_id, text=f"❌ Erro crítico: {str(e)[:100]}")
            print(f"Erro detalhado: {e}")

if __name__ == "__main__":
    main()
    
