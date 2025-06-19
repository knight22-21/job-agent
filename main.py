import typer
from utils.logger import logger
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from filters.ollama_filter import filter_jobs_with_ollama
from scrapers.ai_jobs_scraper import scrape_ai_jobs_net
import subprocess

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

@app.command()
def filter():
    logger.info("Filtering scraped jobs...")
    filter_jobs_with_ollama()
    
@app.command()
def scrape():
    logger.info("Running job scrapers...")
    all_jobs = scrape_ai_jobs_net()
    logger.info(f"Scraped {len(all_jobs)} jobs.")
    
    with open("data/jobs_raw.json", "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=2)
    
@app.command()
def message():
    logger.info("Sending messages to WhatsApp group...")
    subprocess.run(["node", "messenger/send_jobs.js"])
    

if __name__ == "__main__":
    app()
