import os
import asyncio
from telegram import Bot
from playwright.async_api import async_playwright

async def main():
    bot = Bot(token=os.getenv("TOKEN"))
    chat_id = os.getenv("CHAT_ID")
    
    await bot.send_message(chat_id=chat_id, text="🚀 BOT ATIVO: Monitorização de Sinais...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page()
        
        # Acede ao site
        await page.goto("https://www.bantubet.co.ao/casino/game/aviator")
        
        # O loop principal agora é mais "calmo"
        last_odd = None
        while True:
            try:
                # Aqui entra a tua lógica de "scraping"
                # Exemplo: vamos esperar pelo elemento que mostra a odd
                # Ajusta o seletor (ex: '.payout') conforme o elemento real do site
                odd_element = await page.query_selector(".payout") 
                
                if odd_element:
                    current_odd = await odd_element.inner_text()
                    
                    # Só envia mensagem se a odd mudar (para evitar spam)
                    if current_odd != last_odd:
                        await bot.send_message(chat_id=chat_id, text=f"📊 Nova Odd: {current_odd}")
                        last_odd = current_odd
                
            except Exception as e:
                print(f"Erro na monitorização: {e}")
            
            # Espera 10 segundos antes de verificar novamente
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
    
