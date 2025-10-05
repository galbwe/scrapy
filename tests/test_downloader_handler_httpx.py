"""Tests for scrapy.core.downloader.handlers.http11.HTTP11DownloadHandler."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from scrapy.core.downloader.handlers.httpx import HTTPXDownloadHandler
from tests.test_downloader_handlers_http_base import (
    TestHttp11Base,
    TestHttpProxyBase,
    TestHttps11Base,
    TestHttpsCustomCiphersBase,
    TestHttpsInvalidDNSIdBase,
    TestHttpsInvalidDNSPatternBase,
    TestHttpsWrongHostnameBase,
    TestHttpWithCrawlerBase,
    TestSimpleHttpsBase,
)

if TYPE_CHECKING:
    from scrapy.core.downloader.handlers import DownloadHandlerProtocol


class HTTPXDownloadHandlerMixin:
    @property
    def download_handler_cls(self) -> type[DownloadHandlerProtocol]:
        return HTTPXDownloadHandler


class TestHttp11(HTTPXDownloadHandlerMixin, TestHttp11Base):
    pass


class TestHttps11(HTTPXDownloadHandlerMixin, TestHttps11Base):
    pass


class TestSimpleHttps(HTTPXDownloadHandlerMixin, TestSimpleHttpsBase):
    pass


class TestHttps11WrongHostname(HTTPXDownloadHandlerMixin, TestHttpsWrongHostnameBase):
    pass


class TestHttps11InvalidDNSId(HTTPXDownloadHandlerMixin, TestHttpsInvalidDNSIdBase):
    pass


class TestHttps11InvalidDNSPattern(
    HTTPXDownloadHandlerMixin, TestHttpsInvalidDNSPatternBase
):
    pass


class TestHttps11CustomCiphers(HTTPXDownloadHandlerMixin, TestHttpsCustomCiphersBase):
    pass


class TestHttp11WithCrawler(TestHttpWithCrawlerBase):
    @property
    def settings_dict(self) -> dict[str, Any] | None:
        return None  # default handler settings


class TestHttp11Proxy(HTTPXDownloadHandlerMixin, TestHttpProxyBase):
    pass
