from python_template.config.container import Container
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .apis import APIProtocol, completion, diagnostics, healthz, hover, word_completion


def create_app() -> FastAPI:
    """Register api routing.
    :return: FastAPI app
    """
    di_modules = [completion, diagnostics, hover, word_completion]
    # DI
    container = Container()
    container.wire(modules=di_modules)

    app = FastAPI(debug=container.settings.DEBUG())
    app.container = container
    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routing
    endpoints: list[APIProtocol] = [completion, diagnostics, healthz, hover, word_completion]
    for route in endpoints:
        app.include_router(route.router)

    return app
