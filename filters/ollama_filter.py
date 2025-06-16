import json
import ollama
from utils.logger import logger
from config.settings import OLLAMA_MODEL

RAW_JOBS_FILE = "data/jobs_raw.json"
FILTERED_JOBS_FILE = "data/jobs_filtered.json"

def load_jobs():
    try:
        with open(RAW_JOBS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading raw jobs: {e}")
        return []

def save_filtered_jobs(jobs):
    try:
        with open(FILTERED_JOBS_FILE, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2)
        logger.info(f"Saved {len(jobs)} filtered jobs.")
    except Exception as e:
        logger.error(f"Error saving filtered jobs: {e}")

def build_prompt(job_list):
    # Flatten jobs into text blocks
    prompt_text = "\n\n".join([
        f"Title: {job.get('title', '')}\nCompany: {job.get('company', '')}\nLocation: {job.get('location', '')}\nDesc: {job.get('description', '')}"
        for job in job_list
    ])
    
    system_prompt = (
        "You are an expert job recommender. From the list of jobs below, "
        "filter out only those that are:\n"
        "- Remote or Hybrid\n"
        "- Entry-level or Junior ML/AI roles\n"
        "- Preferably Python-based\n\n"
        "Respond ONLY in JSON list format with fields: title, company, location, url.\n"
        "Here are the jobs:\n\n"
    )
    return system_prompt + prompt_text

def filter_jobs_with_ollama():
    logger.info("Loading jobs...")
    jobs = load_jobs()
    if not jobs:
        logger.warning("No jobs to filter.")
        return

    logger.info(f"Filtering {len(jobs)} jobs with Ollama model: {OLLAMA_MODEL}")
    prompt = build_prompt(jobs)
    
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        filtered_jobs = json.loads(response["message"]["content"])
        save_filtered_jobs(filtered_jobs)
    except Exception as e:
        logger.error(f"Ollama filtering failed: {e}")
