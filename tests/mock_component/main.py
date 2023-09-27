import asyncio
import os
from src import a
from src.app import Application
from src.config import Config


async def run() -> None:
    config = Config()
    application = Application.from_config(config)
    await application.start()


def main() -> None:
    asyncio.run(run())
    exit(os.EX_OK)


if __name__ == "__main__":
    main()
