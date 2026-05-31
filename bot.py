import os
import asyncio
import logging
from telegram import Bot
from playwright.async_api import async_playwright

# Configuração de logs para diagnóstico no console da Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define o caminho local dentro do diretório do projeto
# O Playwright instalará os binários aqui durante o Build
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "./ms-playwright"

async def main():
    token = os.getenv("TOKEN")
    chat_id = os.getenv("CHAT_ID")
    
    if not token or not chat_id:
        logger.error("TOKEN ou CHAT_ID em falta nas Variáveis de Ambiente!")
        return

    bot = Bot(token=token)
    
    try:
        logger.info("A iniciar o Playwright...")
        async with async_playwright() as p:
            # Lançamento otimizado para ambientes em nuvem
            # Removemos qualquer executable_path fixo para deixar o Playwright usar o que instalámos
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
            )
            page = await browser.new_page()
            
            logger.info("A aceder ao site da BantuBet...")
            # Aumentámos o tempo limite para evitar erros de carga
            await page.goto("https://www.bantubet.co.ao/casino/game/aviator", timeout=60000)
            
            await bot.send_message(chat_id=chat_id, text="✅ Bot ligado com sucesso!")
            
            # Loop de monitorização - manter o bot vivo
            while True:
                await asyncio.sleep(60)
                
    except Exception as e:
        logger.error(f"Erro crítico no bot: {str(e)}")
        try:
            await bot.send_message(chat_id=chat_id, text=f"❌ Erro crítico: {str(e)[:50]}")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(main())
