import re
import aiohttp
import asyncio
import json
from datetime import datetime
from bs4 import BeautifulSoup, Tag
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YandexRealtyScraper:
    def __init__(self, output_file="yandex_realty.json"):
        self.output_file = output_file
        self.seen_ads = set()
        self.load_existing_data()

    def load_existing_data(self):
        if os.path.exists(self.output_file):
            with open(self.output_file, "r") as f:
                data = json.load(f)
                self.seen_ads = {ad["id"] for ad in data}
        else:
            self.seen_ads = set()

    async def scrape_page(self, session: aiohttp.ClientSession, page=1):
        url = f"https://realty.yandex.ru/moskva/snyat/kvartira/?page={page}"
        try:
            async with session.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    return self.parse_page(soup)
        except Exception as e:
            logger.error(f"Error scraping page {page}: {e}")
            return []

    def parse_page(self, soup: BeautifulSoup):
        ads = []
        for item in soup.select(".OffersSerpItem"):
            try:
                link = item.find("a", class_="OffersSerpItem__link")["href"]
                ad_id = re.search(r"offer/(\d+)", link).group(1)

                if ad_id in self.seen_ads:
                    continue

                description = self.get_text(item, ".OffersSerpItem__description")
                price = self.get_text(item, ".OffersSerpItem__price")
                url = (
                    "https://realty.yandex.ru"
                    + item.select_one(".OffersSerpItem__link")["href"]
                )

                ads.append(
                    {
                        "id": ad_id,
                        "price": price,
                        "description": description,
                        "url": url,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Error parsing ad: {e}")
        return ads

    def get_text(self, element: Tag, selector: str):
        found = element.select_one(selector)
        text: str = found.text if found else ""
        return text.strip()

    async def save_data(self, new_ads):
        if not new_ads:
            return

        existing_data = []
        if os.path.exists(self.output_file):
            with open(self.output_file, "r") as f:
                existing_data = json.load(f)

        updated_data = existing_data + new_ads

        with open(self.output_file, "w") as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=2)

        self.seen_ads.update(ad["id"] for ad in new_ads)
        logger.info(f"Saved {len(new_ads)} new ads")

    async def scrape(self, pages=5):
        async with aiohttp.ClientSession() as session:
            tasks = [self.scrape_page(session, page) for page in range(1, pages + 1)]
            results = await asyncio.gather(*tasks)
            new_ads = [ad for page_ads in results for ad in page_ads]
            await self.save_data(new_ads)
            return new_ads


async def periodic_scrape(interval=3600, pages=5):
    scraper = YandexRealtyScraper()
    while True:
        logger.info(f"Starting new scraping cycle at {datetime.now()}")
        try:
            await scraper.scrape(pages)
        except Exception as e:
            logger.error(f"Scraping error: {e}")

        logger.info(f"Waiting {interval} seconds before next cycle")
        await asyncio.sleep(interval)


if __name__ == "__main__":
    # asyncio.run(YandexRealtyScraper().scrape())
    asyncio.run(periodic_scrape(interval=3600))
