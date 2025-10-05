from typing import Self

import httpx

from scrapy.crawler import Crawler
from scrapy.http import HtmlResponse, JsonResponse, TextResponse
from scrapy.utils.defer import deferred_from_coro


class HTTPXDownloadHandler:
    def __init__(self, settings, crawler=None):
        # self.loop = set_asyncio_event_loop(None)

        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> Self:
        return cls(crawler.settings, crawler)

    def download_request(self, request, spider):
        return deferred_from_coro(self._download(request))

    async def _download(self, request):
        async with httpx.AsyncClient() as client:
            resp = await client.request(
                method=request.method,
                url=str(request.url),
                headers=request.headers.to_unicode_dict(),
                content=request.body or None,
                timeout=10,
            )
            content_type = resp.headers.get("content-type", "").lower()
            # if len(resp.content) > 2:
            #     raise error.ConnectionAborted('Response content was larger than download_maxsize')
            response_cls = TextResponse
            if "text/html" in content_type:
                response_cls = HtmlResponse
            elif "application/json" in content_type or "json" in content_type:
                response_cls = JsonResponse
            return response_cls(
                url=str(request.url),
                status=resp.status_code,
                headers=self._adapt_httpx_headers(resp.headers),
                body=resp.content,
                request=request,
            )

    def _adapt_httpx_headers(self, headers):
        return {h: headers.get_list(h) for h in headers}
