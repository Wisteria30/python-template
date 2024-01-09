import datetime
import json
import logging
import time

from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute

logger = logging.getLogger(__name__)


class LoggingContextRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            """
            時間計測
            """
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = round(time.time() - before, 4)

            record = {}
            time_local = datetime.datetime.fromtimestamp(before)
            record["time_local"] = time_local.strftime("%Y/%m/%d %H:%M:%S%Z")
            if await request.body():
                record["request_body"] = (await request.body()).decode("utf-8")
            record["request_headers"] = {
                k.decode("utf-8"): v.decode("utf-8") for (k, v) in request.headers.raw
            }
            record["remote_addr"] = request.client.host
            record["request_uri"] = request.url.path
            record["request_method"] = request.method
            record["request_time"] = str(duration)
            record["status"] = response.status_code
            record["response_body"] = response.body.decode("utf-8")
            record["response_headers"] = {
                k.decode("utf-8"): v.decode("utf-8") for (k, v) in response.headers.raw
            }
            logger.info(json.dumps(record, ensure_ascii=False))
            return response

        return custom_route_handler
