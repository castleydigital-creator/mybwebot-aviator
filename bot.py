import os
import asyncio
import logging
from telegram import Bot
from playwright.async_api import async_playwright

# Configuração de logs para diagnóstico rápido no console da Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    token = os.getenv("TOKEN")
    chat_id = os.getenv("CHAT_ID")
    
    if not token or not chat_id:
        logger.error("Token ou Chat ID em falta nas variáveis de ambiente!")
        return

    bot = Bot(token=token)
    
    try:
        logger.info("A iniciar o Playwright...")
        async with async_playwright() as p:
            # Lançamento padrão otimizado para a Render
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
            )
            page = await browser.new_page()
            
            logger.info("Acedendo ao site...")
            await page.goto("https://www.bantubet.co.ao/casino/game/aviator", timeout=60000)
            
            await bot.send_message(chat_id=chat_id, text="✅ Bot ligado e página carregada!")
            
            # Manter o processo ativo
            while True:
                await asyncio.sleep(60)
                
    except Exception as e:
        logger.error(f"Erro crítico: {str(e)}")
        # Tenta avisar no Telegram caso ocorra um erro
        try:
            await bot.send_message(chat_id=chat_id, text=f"❌ Erro: {str(e)[:50]}")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(main())
