import typer
from utils.logger import logger
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

app = typer.Typer()

@app.command()
def scrape():
    logger.info("Running job scrapers...")
    # TODO: Import and run from scrapers/

@app.command()
def filter():
    logger.info("Filtering scraped jobs...")
    # TODO: Import and use filters/

@app.command()
def send():
    logger.info("Sending filtered jobs via WhatsApp...")
    # TODO: Import and use messengers/

if __name__ == "__main__":
    app()
