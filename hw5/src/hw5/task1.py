import aiohttp
import asyncio
import os
from urllib.parse import urljoin
import time


async def download_image(
    session: aiohttp.ClientSession,
    url: str,
    save_path: str,
    semaphore: asyncio.Semaphore,
):
    async with semaphore:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()
                    with open(save_path, "wb") as f:
                        f.write(content)
                    print(f"Downloaded: {save_path}")
                    return True
                else:
                    print(f"Failed to download {url}: HTTP {response.status}")
        except Exception as e:
            print(f"Error downloading {url}: {str(e)}")
        return False


async def download_images_async(num_images, output_dir, max_concurrent=10):
    os.makedirs(output_dir, exist_ok=True)

    semaphore = asyncio.Semaphore(max_concurrent)

    base_url = "https://picsum.photos/"

    urls = []
    for i in range(num_images):
        width = 800 + (i % 20)
        height = 600 + (i % 15)
        image_url = urljoin(base_url, f"{width}/{height}?random={i}")
        filename = os.path.join(output_dir, f"image_{i+1}.jpg")
        urls.append((image_url, filename))

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [
            download_image(session, url, filename, semaphore) for url, filename in urls
        ]
        results = await asyncio.gather(*tasks)

    success = sum(results)
    elapsed = time.time() - start_time
    print(f"\nDownloaded {success}/{num_images} images in {elapsed:.2f} seconds")
    print(f"Average speed: {num_images/elapsed:.2f} images/sec")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Асинхронный загрузчик изображений с picsum.photos"
    )
    parser.add_argument(
        "num_images", type=int, help="Количество изображений для загрузки"
    )
    parser.add_argument(
        "output_dir", type=str, help="Директория для сохранения изображений"
    )
    parser.add_argument(
        "--concurrent",
        type=int,
        default=10,
        help="Максимальное количество одновременных загрузок",
    )

    args = parser.parse_args()

    asyncio.run(
        download_images_async(args.num_images, args.output_dir, args.concurrent)
    )
