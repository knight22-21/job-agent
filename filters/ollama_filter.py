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
        f"Title: {job.get('title', '')}\n"
        f"Company: {job.get('company', '')}\n"
        f"Location: {job.get('location', '')}\n"
        f"URL: {job.get('url', '')}\n"
        f"Desc: {job.get('description', '')}"
        for job in job_list
    ])

    system_prompt = (
        "You are an AI job filtering assistant.\n\n"
        "Your task is to filter jobs that match the following HARD conditions:\n\n"
        "1. The `location` field must contain one of these (case-insensitive):\n"
        "   - 'Remote'\n"
        "   - 'Hybrid'\n"
        "   - 'India'\n\n"
        "2. The `title` must clearly be related to AI — including fields like:\n"
        "   - AI / Artificial Intelligence\n"
        "   - Machine Learning (ML)\n"
        "   - Deep Learning (DL)\n"
        "   - NLP / Natural Language Processing\n"
        "   - LLMs / Large Language Models\n"
        "   - Computer Vision (CV)\n"
        "   - Generative AI\n\n"
        "3. Any experience level is acceptable.\n\n"
        "**Important Rules:**\n"
        "- Reject all jobs that do not meet location requirement in point #1.\n"
        "- If a job seems data-related or software-related, keep it ONLY if it is clearly AI-focused.\n"
        "- Do not include jobs that are in the US, Europe, or Israel unless 'Remote' or 'Hybrid' is in the location.\n"
        "- Do not assume 'Remote-friendly' — match exact words: 'Remote', 'Hybrid', or 'India'.\n\n"
        "Return only a JSON list of valid jobs. Each job must include:\n"
        "IMPORTANT: Do NOT include any explanation or markdown (like ```json). Respond with raw JSON only."
        "`title`, `company`, `location`, and `url`.\n\n"
        "Here is the job list:\n"
)



    return system_prompt + prompt_text

def extract_json_array(text):
    """Extracts the first JSON array found in the text string."""
    try:
        start = text.index("[")
        end = text.rindex("]") + 1
        return text[start:end]
    except ValueError:
        return None

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
        content = response["message"]["content"]
        

        json_string = extract_json_array(content)
        if not json_string:
            raise ValueError("No JSON array found in the response.")

        filtered_jobs = json.loads(json_string)
        save_filtered_jobs(filtered_jobs)

    except Exception as e:
        logger.error(f"Ollama filtering failed: {e}")
        print("❌ Failed to parse Ollama response.")