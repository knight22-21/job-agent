from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from utils.logger import logger
import time

def scrape_ai_jobs_net():
    url = "https://aijobs.net/"
    logger.info(f"Scraping {url}")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    jobs = []

    try:
        driver.get(url)

        logger.info("Waiting for job listings to load...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.col.py-2"))
        )

        driver.save_screenshot("aijobs_debug.png")
        logger.info("Saved screenshot to aijobs_debug.png")

        listings = driver.find_elements(By.CSS_SELECTOR, "a.col.py-2")

        logger.info(f"Found {len(listings)} job listings.")

        for job in listings:
            try:
                title = job.find_element(By.CSS_SELECTOR, "h5").text.strip()
                company = job.find_element(By.CSS_SELECTOR, "span.text-muted").text.strip()
        
                # Try getting desktop-first location, fall back to mobile version
                try:
                    location = job.find_element(By.CSS_SELECTOR, "span.d-none.d-md-block.text-break").text.strip()
                except:
                    try:
                        location = job.find_element(By.CSS_SELECTOR, "span.d-block.d-md-none.text-break").text.strip()
                    except:
                        location = ""
        
                link = job.get_attribute("href")

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "url": link
                })
            except Exception as e:
                logger.warning(f"Error parsing a job listing: {e}")


    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
    finally:
        driver.quit()

    logger.info(f"Scraped {len(jobs)} jobs.")
    return jobs
