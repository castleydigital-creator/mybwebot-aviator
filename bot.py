import os
import asyncio
from telegram import Bot
from playwright.async_api import async_playwright

async def main():
    bot = Bot(token=os.getenv("TOKEN"))
    chat_id = os.getenv("CHAT_ID")
    
    await bot.send_message(chat_id=chat_id, text="🚀 BOT INICIADO EM MODO ASSÍNCRONO")
    
    async with async_playwright() as p:
        # A chave para a Render: não especificar path fixo e usar as flags corretas
        browser = await p.chromium.launch(
            headless=True, 
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page()
        await page.goto("https://www.bantubet.co.ao/casino/game/aviator")
        await page.wait_for_timeout(10000)
        
        await bot.send_message(chat_id=chat_id, text="✅ Página da BantuBet carregada!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
    
