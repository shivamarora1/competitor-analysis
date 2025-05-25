import asyncio
import logging
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
import os
from pydantic_ai.exceptions import ModelHTTPError
from pydantic_ai.settings import ModelSettings

load_dotenv()
REQUEST_TIMEOUT = 240
logger = logging.getLogger(__name__)


class CompanyDescription(BaseModel):
    description: str
    category: str
    year_founded: int
    employees: str
    annual_revenue: str
    global_rank: int
    visits: str
    bounce_rate: str
    avg_visit_duration: str
    competitors: List[str]


similarweb_scrapper_server = MCPServerStdio(
    command="npx",
    args=["@brightdata/mcp"],
    env={
        "API_TOKEN": os.getenv("API_TOKEN", ""),
        "WEB_UNLOCKER_ZONE": os.getenv("WEB_UNLOCKER_ZONE", ""),
        "BROWSER_AUTH": os.getenv("BROWSER_AUTH", ""),
    },
)

similarweb_scrapper_agent = Agent(
    # "openai:gpt-4o-mini",
    "openai:gpt-4o",
    output_type=CompanyDescription,
    mcp_servers=[similarweb_scrapper_server],
    retries=1,
    system_prompt="Strictly follow these steps:"
    "1. `scraping_browser_navigate`: To navigate to given url"
    "2. `scraping_browser_get_text`: To extract textual content"
    "Don't use any other tool to scrape information",
    model_settings=ModelSettings(request_timeout=REQUEST_TIMEOUT, max_tokens=2048),
)


async def scrape_website_data(prompt):
    async with similarweb_scrapper_agent.run_mcp_servers():
        result = await asyncio.wait_for(
            similarweb_scrapper_agent.run(prompt), timeout=REQUEST_TIMEOUT
        )
        return result


async def scrape_website_from_similarweb(website: str):
    prompt = lambda website: f"website: https://www.similarweb.com/website/{website}"

    try:
        result = await scrape_website_data(prompt(website))
        logger.info(f"successfully scrapped data for {website}")
        logger.info(result.output)

        competitors = []
        for c in result.output.competitors:
            logger.info(f"fetching data for {c}")
            competitor_result = await scrape_website_data(prompt(c))
            competitors.append(competitor_result.output)
        return {"company": result.output, "competitors": competitors}
    except ModelHTTPError as e:
        logger.error(f"API error for {website}: {str(e)}", exc_info=True)
        return None
    except Exception as e:
        logger.error(
            f"Unexpected error fetching data for {website}: {str(e)}",
            exc_info=True,
        )
        return None
