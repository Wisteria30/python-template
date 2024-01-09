import uvicorn

from python_template.config.settings import Settings
from python_template.presentations.application import create_app


def serve():
    app = create_app()
    for route in app.routes:
        print(route)
    return app


if __name__ == "__main__":
    """uvicornを使用する場合は使う、gunicornはserveを直接使用する"""
    # dev
    uvicorn.run(
        "main:serve",
        host="0.0.0.0",
        port=Settings().PORT,
        log_level=Settings().LOG_LEVEL,
        reload=True,
        factory=True,
    )
