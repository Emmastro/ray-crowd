import logging
from app import create_app

app = create_app()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import hypercorn.asyncio
    import asyncio

    config = hypercorn.Config()
    config.bind = ["0.0.0.0:5000"]

    logger.info("Starting server...")
    print("Starting server...")
    asyncio.run(hypercorn.asyncio.serve(app, config))