import logging
import logging.config
import os.path

import click
import yaml

from delivery.settings import settings

logger = logging.getLogger(__name__)


@click.group
def cls():
    ...


@click.command()
def run_server():
    import uvicorn

    logger.info("Application start")

    uvicorn.run(
        "delivery.app:create_app",
        reload=settings.DEBUG,
        factory=True,
        host=settings.HOST,
        port=settings.PORT,
        # log_config=None,
        proxy_headers=False,
        log_config=_config,
    )


@click.command()
def load():
    import asyncio

    from scripts.load_all_csv import pipline

    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(pipline())


if __name__ == "__main__":
    with open(os.path.normpath(settings.LOGGING_CONFIG_FILE), "r") as f:
        _config = yaml.load(f, Loader=yaml.FullLoader)

    logging.config.dictConfig(_config)

    cls.add_command(run_server)
    cls.add_command(load)
    cls.main()
