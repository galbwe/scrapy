# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Scrapy is a production-grade web scraping and crawling framework for Python 3.10+. It uses Twisted for asynchronous I/O and supports both traditional Deferred-based and modern async/await patterns.

## Common Commands

### Testing
```bash
# Run full test suite with coverage
pytest --cov=scrapy --cov-report=term-missing scrapy tests

# Run a single test file
pytest tests/test_spider.py

# Run a specific test
pytest tests/test_spider.py::SpiderTest::test_name -v

# Run tests with default (non-asyncio) reactor
pytest --reactor=default tests/

# Run tests matching a pattern
pytest -k "test_download" tests/
```

### Linting and Type Checking
```bash
# Run all pre-commit hooks (ruff, formatting, etc.)
pre-commit run --all-files

# Run ruff linter only
ruff check scrapy tests

# Run ruff with auto-fix
ruff check --fix scrapy tests

# Run type checking
mypy scrapy tests

# Run pylint
pylint scrapy tests
```

### Tox Environments
```bash
tox -e py           # Run tests on default Python
tox -e typing       # Run mypy type checking
tox -e pre-commit   # Run all pre-commit hooks
tox -e pylint       # Run pylint
tox -e docs         # Build and test documentation
tox -e pinned       # Test with minimum supported dependency versions
tox -e extra-deps   # Test with optional dependencies (Pillow, boto3, etc.)
```

## Architecture

### Core Request/Response Flow

```
Spider.start() → Scheduler → Downloader → Spider.parse() → Item Pipeline
                    ↑                           │
                    └───── new Requests ────────┘
```

### Key Components

**ExecutionEngine** (`scrapy/core/engine.py`) - Orchestrates the crawl loop, coordinates all components, manages backpressure.

**Crawler/CrawlerProcess** (`scrapy/crawler.py`) - Entry point that creates spiders and engines. CrawlerProcess manages the Twisted reactor.

**Scheduler** (`scrapy/core/scheduler.py`) - Queues requests with deduplication via DupeFilter.

**Downloader** (`scrapy/core/downloader/`) - Fetches URLs via protocol handlers (HTTP, FTP, etc.).

**Scraper** (`scrapy/core/scraper.py`) - Calls spider callbacks and processes yielded items/requests.

### Middleware Pattern

Three middleware pipelines with reverse-order response processing:

1. **Downloader Middleware** (`scrapy/downloadermiddlewares/`) - Processes requests before download, responses after. Methods: `process_request`, `process_response`, `process_exception`.

2. **Spider Middleware** (`scrapy/spidermiddlewares/`) - Wraps spider input/output. Methods: `process_spider_input`, `process_spider_output`, `process_spider_exception`.

3. **Item Pipeline** (`scrapy/pipelines/`) - Processes scraped items. Methods: `open_spider`, `close_spider`, `process_item`.

### Signal System

`SignalManager` (`scrapy/signalmanager.py`) provides event-driven hooks. Key signals in `scrapy/signals.py`: `spider_opened`, `spider_closed`, `spider_idle`, `request_scheduled`, `response_received`, `item_scraped`.

### Settings Priority

Settings are layered (lowest to highest priority):
- `default` (0) - Built-in defaults
- `command` (10) - Command defaults
- `addon` (15) - Addon-provided
- `project` (20) - settings.py
- `spider` (30) - spider.custom_settings
- `cmdline` (40) - `-s KEY=VALUE`

### Dependency Injection

Components are instantiated via `build_from_crawler()` (`scrapy/utils/misc.py`). If a class has `from_crawler(cls, crawler)` classmethod, it receives the full Crawler context; otherwise plain `__init__()` is used.

## Key Patterns

- **Async/Deferred dual support**: Code paths detect asyncio availability and use appropriate primitives. Modern methods end in `_async` (e.g., `process_item_async`).
- **Backpressure**: Engine checks `needs_backout()` before scheduling more requests to prevent memory exhaustion.
- **Per-domain rate limiting**: Downloader maintains separate slots per domain with configurable concurrency and delays.
- **Late binding**: Spider can modify settings before they're frozen when the engine starts.

## Test Markers

- `@pytest.mark.only_asyncio` - Only runs with --reactor=asyncio
- `@pytest.mark.only_not_asyncio` - Only runs without --reactor=asyncio
- `@pytest.mark.requires_uvloop` - Requires uvloop
- `@pytest.mark.requires_botocore` - Requires botocore
- `@pytest.mark.requires_boto3` - Requires boto3
- `@pytest.mark.requires_mitmproxy` - Requires mitmproxy

## Module-Level Import Restrictions

These modules must not be imported at module level (enforced by ruff):
- `twisted.internet.reactor`
- `twisted.conch.manhole`
- `twisted.protocols.ftp`
