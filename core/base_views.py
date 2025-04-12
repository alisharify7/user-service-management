"""
* users management
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/user-service-management
"""

from core import app
from core.config import get_config


Setting = get_config()


@app.get("/")
def index():
    return {
        "status": "ok",
        "debug": Setting.DEBUG,
        "swagger": Setting.API_SWAGGER_URL,
        "version": Setting.API_ABSOLUTE_VERSION,
        "API-TERM-URL": Setting.API_TERM_URL,
        "redoc": Setting.API_REDOC_URL,
    }
