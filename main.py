import logging

import click

logger = logging.getLogger(__name__)


@click.group
def cls():
    ...


@click.command()
def run_server():
    import uvicorn

    from delivery.settings import settings

    logger.info("Application start")

    uvicorn.run(
        "delivery.app:create_app",
        reload=settings.DEBUG,
        factory=True,
        host=settings.HOST,
        port=settings.PORT,
        # log_config=None,
        proxy_headers=False,
    )


@click.command()
def load():
    import asyncio

    from scripts.load_all_csv import pipline

    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(pipline())


if __name__ == "__main__":
    cls.add_command(run_server)
    cls.add_command(load)
    cls.main()
