import asyncio
import logging
from typing import Union
import logfire
from logfire import ConsoleOptions

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app.mcp_clients import scrape_website_from_similarweb

logfire.configure(
    send_to_logfire=False,
    console=ConsoleOptions(
        colors="auto",
        include_timestamps=True,
        include_tags=True,
        verbose=True,
    ),
)
logfire.instrument_pydantic_ai(event_mode="logs")
logfire.instrument_httpx(capture_all=True)

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=getattr(logging, "INFO", logging.INFO),
    format="%(asctime)s :: %(levelname)s :: %(processName)s :: %(threadName)s :: %(filename)s :: %(funcName)s :: %(message)s",
)
app = FastAPI()

DATA_FETCH_TIMEOUT = 300


@app.get("/scrape/{website_name}")
async def scrape_website(website_name: str, q: Union[str, None] = None):
    logger.info(f"Starting scraping for: {website_name}")
    try:
        tasks = {
            website_name: asyncio.create_task(
                scrape_website_from_similarweb(website_name)
            ),
        }

        done, pending = await asyncio.wait(tasks.values(), timeout=DATA_FETCH_TIMEOUT)

        results = {}
        for key, task in tasks.items():
            if task in done:
                try:
                    results[key] = await task
                    logger.info(f"{key} task completed")
                except Exception as e:
                    results[key] = None
                    logger.warning(f"{key} failed: {e}")
            else:
                task.cancel()
                results[key] = None
                logger.warning(f"{key} task timed out and was cancelled")

        company_result = results[website_name]

        logger.info(f"Result {company_result}")
        return company_result
    except Exception as e:
        logger.error(f"Error analyzing company {website_name}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while analyzing the company: {str(e)}",
        )
