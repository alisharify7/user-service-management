from fastapi import FastAPI
from core.config import get_config


Settings = get_config()

def create_app(config_class: object) -> FastAPI:
    """main factory function for generation fastapi application """
    return FastAPI(
        debug=config_class.debug,
        title=config_class.API_NAME,
        summary=config_class.API_SUMMERY,
        description=config_class.API_DESCRIPTION,
        version=config_class.API_ABSOLUTE_VERSION,
        docs_url=config_class.API_SWAGGER_URL,
        redoc_url=config_class.API_REDOC_URL,
        terms_of_service=config_class.API_TERM_URL,
    )