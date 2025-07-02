# Crawl4AI Custom LLM Context
Generated on: 2025-06-04T17:19:58.932Z
Total files: 1

---

## Unknown Component - Complete Context
Source: crawl4ai_vibe.llm.full.md

# Crawl4ai - AI Friendly Documentation (aka LLM.TXT)

This document provides AI-friendly documentation for the Crawl4ai library. It contains three types of content:

**Memory (Facts)**: Similar to traditional LLM.txt files, this section contains factual information about the library - what it is, what it does, its components, APIs, and capabilities. This is the reference knowledge that an AI needs to understand the library.

**Reasoning (Instructions)**: This section instructs AI models on how to use the factual knowledge, think about problems in the way the library authors intended, and provide solutions that align with the library's design philosophy. It guides the AI's problem-solving approach when working with Crawl4ai.

**Examples**: Practical code examples demonstrating how to use the library's features in real-world scenarios. These examples help AI models understand the practical application of the concepts.

## Content (Memory)

Okay, I have read the "vibe" description for `crawl4ai`. Based on this, and adhering to the "memory" document type requirements, here is the detailed Markdown outline:

```markdown
# Detailed Outline for crawl4ai - vibe Component

**Target Document Type:** memory
**Target Output Filename Suggestion:** `llm_memory_vibe_coding.md`
**Library Version Context:** 0.6.3
**Outline Generation Date:** 2025-05-24
---

## 1. Vibe Coding with Crawl4AI: Core Concept

*   1.1. Purpose:
    *   Provides a conceptual framework for interacting with the `crawl4ai` library, particularly when using AI coding assistants.
    *   Aims to simplify the process of building web data applications by focusing on high-level capabilities and key building blocks, enabling users to guide AI assistants effectively even with limited direct `crawl4ai` API knowledge.
*   1.2. Principle:
    *   Describes how users can communicate their web scraping and data extraction goals to an AI assistant, which then translates these "vibes" or high-level intentions into `crawl4ai` Python code by leveraging knowledge of the library's core components and configurations.

## 2. `crawl4ai` High-Level Capabilities (for Vibe Prompts)

*   2.1. Fetching Webpages
    *   2.1.1. Description: The library can retrieve content from specified web URLs.
*   2.2. Converting Web Content to Clean Markdown
    *   2.2.1. Description: The library can process raw HTML content and convert it into a cleaned, structured Markdown format.
    *   2.2.2. Applications: Suitable for content summarization, input for Question & Answering systems, and as a pre-processing step for other LLMs.
*   2.3. Extracting Specific Information (JSON)
    *   2.3.1. Description: The library can extract targeted data elements from webpages and organize them into a JSON structure.
    *   2.3.2. Examples: Can be used to extract product names, prices from e-commerce sites, article headlines, author names, etc.
*   2.4. Crawling Multiple Pages
    *   2.4.1. Description: The library supports concurrent fetching and processing of a list of URLs.
*   2.5. Taking Screenshots and Generating PDFs
    *   2.5.1. Description: The library can capture visual representations of webpages as PNG screenshots or generate PDF documents.
*   2.6. Handling Simple Page Interactions
    *   2.6.1. Description: The library can execute JavaScript to simulate basic user interactions on a webpage, such as clicking buttons (e.g., "load more") or scrolling.

## 3. Key `crawl4ai` Building Blocks (API Reference for Vibe Coding Context)

*   3.1. Class `AsyncWebCrawler`
    *   3.1.1. Purpose: The primary entry point and main tool within `crawl4ai` for orchestrating web crawling and data extraction tasks.
    *   3.1.2. Initialization (`__init__`):
        *   Signature: `AsyncWebCrawler(self, crawler_strategy: Optional[AsyncCrawlerStrategy] = None, config: Optional[BrowserConfig] = None, base_directory: str = ..., thread_safe: bool = False, logger: Optional[AsyncLoggerBase] = None, **kwargs)`
        *   Parameters:
            *   `crawler_strategy (Optional[AsyncCrawlerStrategy])`: The underlying strategy for web crawling (e.g., `AsyncPlaywrightCrawlerStrategy`). Defaults to `AsyncPlaywrightCrawlerStrategy`.
            *   `config (Optional[BrowserConfig])`: Configuration for the browser instance. See section 3.5 for details.
            *   Other parameters are generally handled by defaults for vibe coding.
*   3.2. Method `AsyncWebCrawler.arun()`
    *   3.2.1. Purpose: Executes a crawl operation on a single URL or resource.
    *   3.2.2. Signature: `async def arun(self, url: str, config: Optional[CrawlerRunConfig] = None, **kwargs) -> RunManyReturn`
    *   3.2.3. Parameters:
        *   `url (str)`: The target resource.
            *   Description: Can be a standard web URL (e.g., "https://example.com"), a local file path (e.g., "file:///path/to/file.html"), or raw HTML content (e.g., "raw:<html>...</html>").
        *   `config (Optional[CrawlerRunConfig])`: An instance of `CrawlerRunConfig` specifying how this particular crawl run should be executed. See section 3.4 for details.
*   3.3. Method `AsyncWebCrawler.arun_many()`
    *   3.3.1. Purpose: Executes crawl operations on a list of URLs or resources, often concurrently.
    *   3.3.2. Signature: `async def arun_many(self, urls: List[str], config: Optional[CrawlerRunConfig] = None, dispatcher: Optional[BaseDispatcher] = None, **kwargs) -> RunManyReturn`
    *   3.3.3. Parameters:
        *   `urls (List[str])`: A list of target resources (URLs, file paths, raw HTML strings).
        *   `config (Optional[CrawlerRunConfig])`: An instance of `CrawlerRunConfig` applied to all URLs in the list. See section 3.4 for details.
*   3.4. Class `CrawlerRunConfig`
    *   3.4.1. Purpose: Configuration object for individual crawl runs, controlling aspects like content extraction, page interaction, and output formats.
    *   3.4.2. Key Parameters for Vibe Coding Context:
        *   `markdown_generator (Optional[MarkdownGenerationStrategy])`:
            *   Description: Specifies the strategy for generating Markdown.
            *   Default: An instance of `DefaultMarkdownGenerator`.
            *   Note for Vibe Coding: Can be `DefaultMarkdownGenerator(content_filter=PruningContentFilter())` for cleaner output.
        *   `extraction_strategy (Optional[ExtractionStrategy])`:
            *   Description: Specifies the strategy for extracting structured data.
            *   Supported Strategies (for Vibe Coding):
                *   `JsonCssExtractionStrategy`: For extracting data based on CSS selectors from structured HTML. Requires a `schema` dictionary.
                *   `LLMExtractionStrategy`: For extracting data using an LLM, often for complex or unstructured HTML. Requires an `LLMConfig` and an `instruction` or Pydantic model defining the desired output.
        *   `js_code (Optional[Union[str, List[str]]])`:
            *   Description: JavaScript code (or a list of code snippets) to be executed on the page after it loads.
        *   `wait_for (Optional[str])`:
            *   Description: A CSS selector or JavaScript expression. The crawler will wait for this condition to be met after `js_code` execution before proceeding.
        *   `session_id (Optional[str])`:
            *   Description: An identifier used to maintain the state of a browser page across multiple `arun` calls. Essential for multi-step interactions on the same page.
        *   `js_only (bool)`:
            *   Description: If `True` (and `session_id` is used), only executes `js_code` on the existing page without a full navigation/reload. Default is `False`.
        *   `screenshot (bool)`:
            *   Description: If `True`, captures a screenshot of the page. Result in `CrawlResult.screenshot`. Default is `False`.
        *   `pdf (bool)`:
            *   Description: If `True`, generates a PDF of the page. Result in `CrawlResult.pdf`. Default is `False`.
        *   `cache_mode (Optional[CacheMode])`:
            *   Description: Controls caching behavior.
            *   Type: `crawl4ai.cache_context.CacheMode` (Enum).
            *   Common Values: `CacheMode.ENABLED`, `CacheMode.BYPASS`.
*   3.5. Class `BrowserConfig`
    *   3.5.1. Purpose: Configures persistent browser-level settings for an `AsyncWebCrawler` instance.
    *   3.5.2. Key Parameters for Vibe Coding Context:
        *   `headless (bool)`:
            *   Description: If `True`, the browser runs without a visible UI. If `False`, the browser UI is shown.
            *   Default: `True`.
        *   `proxy_config (Optional[Union[ProxyConfig, Dict[str, str]]])`:
            *   Description: Configuration for using a proxy server.
            *   Structure (if dict): `{"server": "http://<host>:<port>", "username": "<user>", "password": "<pass>"}`.
        *   `user_agent (Optional[str])`:
            *   Description: Custom User-Agent string to be used by the browser.
*   3.6. Class `LLMConfig`
    *   3.6.1. Purpose: Configures settings for interacting with Large Language Models, used by `LLMExtractionStrategy`.
    *   3.6.2. Key Parameters:
        *   `provider (str)`:
            *   Description: Specifies the LLM provider and model identifier.
            *   Examples: "openai/gpt-4o-mini", "ollama/llama3", "anthropic/claude-3-opus-20240229".
        *   `api_token (Optional[str])`:
            *   Description: API key for the LLM provider. Can be the actual key or an environment variable reference (e.g., "env:OPENAI_API_KEY").
*   3.7. Class `CrawlResult`
    *   3.7.1. Purpose: The data object returned by `crawl4ai` operations, containing the results and metadata of a crawl.
    *   3.7.2. Key Attributes:
        *   `success (bool)`: `True` if the crawl was successful, `False` otherwise.
        *   `markdown (MarkdownGenerationResult)`: Object containing Markdown representations.
            *   `markdown.raw_markdown (str)`: Markdown generated directly from the cleaned HTML.
            *   `markdown.fit_markdown (str)`: Markdown potentially further processed by content filters.
        *   `extracted_content (Optional[str])`: JSON string of structured data if an `ExtractionStrategy` was used and successful.
        *   `links (Links)`: Object containing `internal` and `external` lists of `Link` objects. Each `Link` object has `href`, `text`, `title`.
        *   `media (Media)`: Object containing lists of `MediaItem` for `images`, `videos`, `audios`, and `tables`. Each `MediaItem` has `src`, `alt`, `score`, etc.
        *   `screenshot (Optional[str])`: Base64 encoded string of the PNG screenshot, if `screenshot=True`.
        *   `pdf (Optional[bytes])`: Raw bytes of the PDF document, if `pdf=True`.
        *   `error_message (Optional[str])`: Description of the error if `success` is `False`.

## 4. Common `crawl4ai` Usage Patterns (Vibe Recipes Mapped to Components)

*   4.1. Task: Get Clean Markdown from a Page
    *   4.1.1. Description: Fetch a single webpage and convert its main content into clean Markdown.
    *   4.1.2. Key `crawl4ai` elements:
        *   `AsyncWebCrawler`
        *   `arun()` method.
        *   `CrawlerRunConfig`:
            *   `markdown_generator`: Typically `DefaultMarkdownGenerator()`. For very clean output, `DefaultMarkdownGenerator(content_filter=PruningContentFilter())`.
*   4.2. Task: Extract All Product Names and Prices from an E-commerce Category Page
    *   4.2.1. Description: Scrape structured data (e.g., product names, prices) from a page with repeating elements.
    *   4.2.2. Key `crawl4ai` elements:
        *   `AsyncWebCrawler`
        *   `arun()` method.
        *   `CrawlerRunConfig`:
            *   `extraction_strategy`: `JsonCssExtractionStrategy(schema={"name_field": "h2.product-title", "price_field": "span.price"})`. The schema's CSS selectors identify where to find the data.
*   4.3. Task: Extract Key Information from an Article using an LLM
    *   4.3.1. Description: Use an LLM to parse an article and extract specific fields like author, date, and a summary into a JSON format.
    *   4.3.2. Key `crawl4ai` elements:
        *   `AsyncWebCrawler`
        *   `arun()` method.
        *   `CrawlerRunConfig`:
            *   `extraction_strategy`: `LLMExtractionStrategy(llm_config=..., instruction=..., schema=...)`.
        *   `LLMConfig`: Instance specifying `provider` (e.g., "openai/gpt-4o-mini") and `api_token`.
        *   Schema for `LLMExtractionStrategy`: Can be a Pydantic model definition or a dictionary describing the target JSON structure.
*   4.4. Task: Crawl Multiple Pages of a Blog (Clicking "Next Page")
    *   4.4.1. Description: Navigate through paginated content by simulating clicks on "Next Page" or similar links, collecting data from each page.
    *   4.4.2. Key `crawl4ai` elements:
        *   `AsyncWebCrawler`
        *   Multiple sequential calls to `arun()` (typically in a loop).
        *   `CrawlerRunConfig` (reused or cloned for each step):
            *   `session_id`: A consistent identifier (e.g., "blog_pagination_session") to maintain the browser state across `arun` calls.
            *   `js_code`: JavaScript to trigger the "Next Page" action (e.g., `document.querySelector('a.next-page-link').click();`).
            *   `wait_for`: A CSS selector or JavaScript condition to ensure the new page content has loaded before proceeding.
            *   `js_only=True`: For subsequent `arun` calls after the initial page load to indicate only JS interaction without full navigation.
*   4.5. Task: Get Screenshots of a List of URLs
    *   4.5.1. Description: Capture screenshots for a batch of URLs.
    *   4.5.2. Key `crawl4ai` elements:
        *   `AsyncWebCrawler`
        *   `arun_many()` method.
        *   `CrawlerRunConfig`:
            *   `screenshot=True`.

## 5. Key Input Considerations for `crawl4ai` Operations (Inferred from Vibe Prompting Tips)

*   5.1. Clear Objective: `crawl4ai` operations are guided by the configuration. The configuration should reflect the user's goal (e.g., Markdown generation, specific data extraction, media capture).
*   5.2. URL Input: The `arun` method requires a single `url` string. `arun_many` requires a `List[str]` of URLs.
*   5.3. Structured Data Extraction Guidance:
    *   For `JsonCssExtractionStrategy`, the `schema` parameter (a dictionary mapping desired field names to CSS selectors) is essential.
    *   For `LLMExtractionStrategy`, the `instruction` parameter (natural language description of desired data) and/or a `schema` (Pydantic model or dictionary) are crucial, along with a configured `LLMConfig`.
*   5.4. LLM Configuration: When `LLMExtractionStrategy` is used, an `LLMConfig` instance specifying `provider` and `api_token` (if applicable) must be provided.
*   5.5. Dynamic Page Handling: For pages requiring interaction, `CrawlerRunConfig` parameters like `js_code`, `wait_for`, `session_id`, and `js_only` are used.

## 6. Expected Output Data from `crawl4ai` Operations (Accessing `CrawlResult`)

*   6.1. Generated Python Code: When using an AI assistant with `crawl4ai` context, the AI is expected to generate Python code that utilizes `crawl4ai` classes and methods.
*   6.2. `CrawlResult` Object: The primary output of `arun()` and `arun_many()` calls.
    *   `result.success (bool)`: Indicates if the individual crawl operation was successful.
    *   `result.markdown.raw_markdown (str)` / `result.markdown.fit_markdown (str)`: Contains the generated Markdown content.
    *   `result.extracted_content (Optional[str])`: Contains the JSON string of structured data if an extraction strategy was successful.
    *   `result.links (Links)`: Provides access to lists of internal and external links.
    *   `result.media (Media)`: Provides access to lists of images, videos, audio files, and tables.
    *   `result.screenshot (Optional[str])`: Base64 encoded screenshot data.
    *   `result.pdf (Optional[bytes])`: Raw PDF data.
    *   `result.error_message (Optional[str])`: Error details if `success` is `False`.
*   6.3. Files on Disk: Operations like screenshot or PDF generation, or custom code within an AI-generated script, might save files to the local disk (e.g., PNGs, PDFs, JSON files). The paths depend on the configuration or the custom code.

```

## Content (Reasoning)

```markdown
# Detailed Outline for crawl4ai - vibe Component

**Target Document Type:** reasoning
**Target Output Filename Suggestion:** `llm_reasoning_vibe.md`
**Library Version Context:** 0.6.3
**Outline Generation Date:** 2025-05-24
---

# Vibe Coding with Crawl4AI: A Guide for AI Coding Assistants

## 1. Introduction: What is "Vibe Coding" with Crawl4AI?

*   **1.1. Explaining the Core Idea:**
    "Vibe Coding" with Crawl4AI is about empowering users, even those with limited direct coding experience, to build powerful web data applications. Instead of meticulously writing every line of Python, you focus on clearly describing your data extraction or web interaction goals to an AI coding assistant. This guide teaches you how to provide that AI assistant with the *right context* about Crawl4AI, so it can generate effective and efficient code for you. The goal is to translate your "vibe" – your high-level intent – into working Crawl4AI solutions quickly.

*   **1.2. Who is this Guide For?**
    This guide is designed for:
    *   **Users new to web scraping or `crawl4ai`:** If you prefer to articulate your needs in natural language and have an AI assistant handle the code generation, this guide is for you.
    *   **Data analysts, researchers, and product managers:** Anyone who needs web data but doesn't want to get bogged down in the intricacies of web scraping libraries.
    *   **Developers looking for rapid prototyping:** Even experienced developers can use "vibe coding" to quickly generate boilerplate or test ideas with `crawl4ai` before refining the code.
    *   **AI Coding Assistant Users:** This guide helps you understand what information to feed your AI to get the best `crawl4ai` code.

*   **1.3. How this Guide Helps You (and Your AI Assistant):**
    By understanding the concepts in this guide, you (and by extension, your AI assistant) will:
    *   Grasp the high-level capabilities of `crawl4ai` that are most relevant for prompting an AI.
    *   Learn the key terminology and building blocks of `crawl4ai` to include in your prompts for precise code generation.
    *   Discover common "vibe recipes" – typical data extraction tasks and how to prompt an AI to solve them using `crawl4ai`.
    *   Pick up effective prompting patterns to maximize the quality of AI-generated `crawl4ai` code.

## 2. High-Level Capabilities of Crawl4AI (What to Tell Your AI Assistant Crawl4AI Can Do)

When you're "vibe coding" with your AI assistant, you don't need to explain every nuance of `crawl4ai`. Instead, focus on what it *can do* for you. Here's a high-level overview of capabilities you can confidently tell your AI assistant about:

*   **2.1. Fetching Any Webpage:**
    *   **How to tell your AI:** "Crawl4AI can fetch the content of any webpage, whether it's a simple static page or a complex JavaScript-heavy application."
    *   **Why it's important:** This establishes the fundamental capability – getting the raw HTML from a target URL.

*   **2.2. Converting Web Content into Clean Markdown:**
    *   **How to tell your AI:** "Crawl4AI is great at turning messy web pages into clean, readable Markdown. This is perfect if I need to summarize an article, feed content into another LLM for Q&A, or just get the main text."
    *   **Why it's important:** Markdown is often the desired end-format for LLM-based tasks, and `crawl4ai` simplifies this conversion.

*   **2.3. Extracting Specific Pieces of Information (Structured Data/JSON):**
    *   **How to tell your AI:** "If I need specific data from a page, like all the product names and prices from an e-commerce site, or all the headlines from a news page, Crawl4AI can extract that and give it to me as structured JSON."
    *   **Why it's important:** This highlights `crawl4ai`'s ability to go beyond simple text extraction and pull out specific, targeted information.

*   **2.4. Crawling Multiple Pages at Once:**
    *   **How to tell your AI:** "If I have a list of URLs, Crawl4AI can process them all efficiently, often in parallel, instead of me having to do them one by one."
    *   **Why it's important:** This points to the library's capability for batch processing, saving significant time for larger tasks.

*   **2.5. Taking Screenshots or Making PDFs of Pages:**
    *   **How to tell your AI:** "Crawl4AI can take a screenshot of a webpage or save it as a PDF document. This is useful for archiving, visual checks, or sharing."
    *   **Why it's important:** Visual capture and PDF generation are common requirements that `crawl4ai` handles easily.

*   **2.6. Handling Simple Page Interactions:**
    *   **How to tell your AI:** "For pages that need a bit of interaction, like clicking a 'load more' button to reveal more content or scrolling down, Crawl4AI can execute JavaScript to do that."
    *   **Why it'S important:** This shows that `crawl4ai` isn't limited to static content and can handle basic dynamic page elements to access more data.

## 3. Key Building Blocks: Communicating Crawl4AI Concepts to Your AI Assistant

To get the best results from your AI assistant, you'll want to mention the key components of `crawl4ai` it should use. Think of these as the essential vocabulary for your "vibe" prompts.

*   **3.1. `AsyncWebCrawler`**: The Main Tool
    *   **3.1.1. Explaining its Role:**
        *   **What to tell your AI:** "The main tool we'll use in `crawl4ai` is called `AsyncWebCrawler`. We always need to create an instance of this first. It's best to use it with an `async with` statement to make sure resources are managed correctly."
        *   **Why it's important for the AI:** This directs the AI to the central class for all crawling operations and hints at the asynchronous nature and proper resource management.
    *   **3.1.2. Basic Usage Pattern:**
        *   **Vibe Prompt:** "Let's start a `crawl4ai` script. We'll need an `AsyncWebCrawler`."
        *   **Expected AI action:** The AI should generate the basic setup:
            ```python
            import asyncio
            from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig # Common imports

            async def main():
                # browser_config = BrowserConfig(...) # Optional, if needed
                async with AsyncWebCrawler(# config=browser_config
                                          ) as crawler:
                    # ... your crawl logic will go here ...
                    pass

            if __name__ == "__main__":
                asyncio.run(main())
            ```

*   **3.2. `arun(url, config)`**: Crawling a Single Page
    *   **3.2.1. Explaining its Purpose:**
        *   **What to tell your AI:** "To crawl a single page, we'll use the `arun` method of the `AsyncWebCrawler` instance. It takes the URL and an optional configuration object."
        *   **Why it's important for the AI:** This points to the primary method for individual page crawls.
    *   **3.2.2. Guiding the AI on `url` Specification:**
        *   **What to tell your AI:** "The `url` for `arun` can be a regular web address (like 'https://example.com'), a local file path (if it starts with `file://`), or even raw HTML content (if it starts with `raw:`)."
        *   **Vibe Prompts & AI Interpretation:**
            *   "Crawl this URL: https://my-target-site.com" -> AI uses `url="https://my-target-site.com"`
            *   "Process this local HTML file: /path/to/my/page.html" -> AI uses `url="file:///path/to/my/page.html"`
            *   "I have some raw HTML I want to parse: `<html><body><h1>Test</h1></body></html>`" -> AI uses `url="raw:<html><body><h1>Test</h1></body></html>"`
    *   **3.2.3. Emphasizing `config` (`CrawlerRunConfig`):**
        *   **What to tell your AI:** "The most important part for customizing a crawl is the `config` parameter of `arun`. This is where we'll use `CrawlerRunConfig` to tell `crawl4ai` *how* to crawl, what to extract, and what to do with the page."
        *   **Vibe Prompt:** "...and when you call `arun`, pass in a `CrawlerRunConfig` object with these settings: [describe settings]."

*   **3.3. `arun_many(urls, config)`**: Crawling Multiple Pages
    *   **3.3.1. Explaining its Purpose:**
        *   **What to tell your AI:** "If I have a list of URLs, we should use `arun_many` instead of calling `arun` in a loop. It's more efficient for batch crawling."
        *   **Why it's important for the AI:** Guides the AI to use the optimized method for multiple URLs, which handles concurrency internally.
    *   **3.3.2. Vibe Prompt:**
        *   "Crawl all these pages: https://example.com/page1, https://example.com/page2, https://example.com/page3."
        *   **Expected AI action:**
            ```python
            # ... inside async def main() and async with AsyncWebCrawler ...
            list_of_urls = [
                "https://example.com/page1",
                "https://example.com/page2",
                "https://example.com/page3"
            ]
            # run_config = CrawlerRunConfig(...) # Define config for all URLs
            results = await crawler.arun_many(urls=list_of_urls, config=run_config)
            for result in results:
                # process each result
                pass
            ```

*   **3.4. `CrawlerRunConfig`**: Tailoring the Crawl (Simplified for Vibe Coding)
    *   **3.4.1. Getting Markdown:**
        *   **Basic Request Vibe:** "Get the Markdown for this page [URL]."
            *   **AI's understanding:** The AI should know that `crawl4ai` produces Markdown by default, so a very simple `CrawlerRunConfig()` or even `None` might suffice if no other settings are needed.
        *   **For Cleaner Markdown Vibe:** "I need very clean Markdown from [URL], suitable for feeding into another LLM. Remove boilerplate like headers, footers, and navigation."
            *   **AI's understanding:** "Ah, the user wants cleaner output. I should suggest or use `DefaultMarkdownGenerator` combined with `PruningContentFilter`. The `PruningContentFilter` heuristically tries to remove common non-content sections."
            *   **Code Snippet AI might generate:**
                ```python
                from crawl4ai import CrawlerRunConfig, DefaultMarkdownGenerator
                from crawl4ai.content_filter_strategy import PruningContentFilter

                markdown_generator = DefaultMarkdownGenerator(
                    content_filter=PruningContentFilter()
                )
                run_config = CrawlerRunConfig(
                    markdown_generator=markdown_generator
                )
                # result = await crawler.arun(url="...", config=run_config)
                # print(result.markdown.fit_markdown) # Access the filtered markdown
                ```
            *   **Reasoning to convey (implicitly or explicitly):** `PruningContentFilter` is a good first step for general boilerplate removal. `DefaultMarkdownGenerator` then converts the filtered HTML to Markdown. Accessing `result.markdown.fit_markdown` gives this cleaner version.
    *   **3.4.2. Extracting Specific Data (JSON):**
        *   **3.4.2.1. Using `JsonCssExtractionStrategy` for Structured Pages:**
            *   **When to suggest it (Vibe):** "The page I want to crawl ([URL]) has a list of items, like products on an e-commerce category page, and each item has a similar layout. I want to extract these repeating items into a JSON list."
            *   **Information to provide the AI (Vibe):** "For each item, I want to get the 'product_name', which is usually in an `<h2>` tag, and the 'price', which seems to be in a `<span>` tag with a class like 'price-tag' or 'current-price'."
            *   **AI's Role & Reasoning:** The AI should recognize this pattern and suggest `JsonCssExtractionStrategy`. It understands that the user is describing a schema. The AI's job is to translate "name from h2" into `{"name": "product_name", "selector": "h2", "type": "text"}` within the `fields` list of a schema dictionary, and the overall repeating item selector into `baseSelector`. The AI should also know to set `extraction_type="schema"` on `LLMExtractionStrategy` if it were using that for schema generation, but here it's direct CSS.
            *   **Code Snippet AI might generate:**
                ```python
                from crawl4ai import CrawlerRunConfig
                from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

                # AI would help construct this schema based on user's description
                schema = {
                    "name": "ProductList",
                    "baseSelector": "div.product-item", # Example selector for each product block
                    "fields": [
                        {"name": "product_name", "selector": "h2.product-title", "type": "text"},
                        {"name": "price", "selector": "span.price-tag", "type": "text"}
                    ]
                }
                extraction_strategy = JsonCssExtractionStrategy(schema=schema)
                run_config = CrawlerRunConfig(extraction_strategy=extraction_strategy)
                # result = await crawler.arun(url="...", config=run_config)
                # if result.success and result.extracted_content:
                #     products = json.loads(result.extracted_content)
                #     for product in products:
                #         print(f"Name: {product.get('product_name')}, Price: {product.get('price')}")
                ```
        *   **3.4.2.2. Using `LLMExtractionStrategy` for Complex/Unclear Structures:**
            *   **When to suggest it (Vibe):** "The page ([URL]) has the information I want, but it's not in a clear, repeating list, or it's mixed in with a lot of text. I need the AI to understand the content to pull out specific details." Or, "I want to extract information that requires some interpretation, like summarizing a paragraph."
            *   **Information to provide the AI (Vibe):**
                *   "Use `LLMExtractionStrategy` for this."
                *   "The LLM I want to use is [LLM provider/model, e.g., 'openai/gpt-4o-mini'] and my API key is [YOUR_API_KEY_OR_ENV_VAR_NAME] (or tell it to look for an env var)."
                *   **Option A (Describing fields):** "I need a JSON object with the following fields: 'author_name', 'article_publish_date', and a 'short_summary' (about 2 sentences)."
                *   **Option B (Example JSON):** "The JSON output should look something like this: `{\"author\": \"Jane Doe\", \"published_on\": \"2024-05-23\", \"summary\": \"This article discusses...\"}`."
                *   **Option C (Pydantic Model - more advanced but best for AI):** "Here's a Pydantic model that defines the structure I want: [Pydantic Class Code Snippet]. Use this for the schema."
            *   **AI's Role & Reasoning:** The AI needs to construct an `LLMConfig` and an `LLMExtractionStrategy`. If the user provides field descriptions or an example JSON, the AI can generate a simple schema dictionary. If a Pydantic model is provided, the AI should use `MyPydanticModel.model_json_schema()` to create the schema for `LLMExtractionStrategy`. This strategy is powerful because it leverages the LLM's understanding.
            *   **Code Snippet AI might generate (with Pydantic example):**
                ```python
                from crawl4ai import CrawlerRunConfig, LLMConfig
                from crawl4ai.extraction_strategy import LLMExtractionStrategy
                from pydantic import BaseModel, Field # Assuming user might provide this

                # User might provide this, or AI generates it from description
                class ArticleInfo(BaseModel):
                    author_name: str = Field(description="The main author of the article")
                    publication_date: str = Field(description="The date the article was published, e.g., YYYY-MM-DD")
                    short_summary: str = Field(description="A concise 2-3 sentence summary of the article")

                llm_config = LLMConfig(
                    provider="openai/gpt-4o-mini", # Or user's choice
                    api_token="env:OPENAI_API_KEY" # Or direct key if user insists and understands risk
                )
                extraction_strategy = LLMExtractionStrategy(
                    llm_config=llm_config,
                    schema=ArticleInfo.model_json_schema(),
                    # instruction="Extract author, publication date, and a summary." # Could also be used
                    extraction_type="schema" # Important for Pydantic/JSON schema
                )
                run_config = CrawlerRunConfig(extraction_strategy=extraction_strategy)
                # result = await crawler.arun(url="...", config=run_config)
                # if result.success and result.extracted_content:
                #     article_data = json.loads(result.extracted_content) # Or ArticleInfo.model_validate_json(result.extracted_content)
                #     print(article_data)
                ```
    *   **3.4.3. Interacting with Pages (Dynamic Content):**
        *   **How to tell your AI (Vibe):** "This page ([URL]) loads more content when you scroll down, or when you click a 'Show More' button. `crawl4ai` needs to perform this interaction."
        *   **For clicking (Vibe):** "To get all the data, we need to click the button with text 'Load All Comments'."
            *   **AI's understanding:** This requires `js_code` to find and click the button. The AI should be guided that finding elements by text might involve more complex JS like `Array.from(document.querySelectorAll('button')).find(btn => btn.textContent.includes('Load All Comments')).click();`.
        *   **For scrolling (Vibe):** "Scroll to the bottom of the page to make sure everything loads."
            *   **AI's understanding:** `js_code` like `window.scrollTo(0, document.body.scrollHeight);`
        *   **Ensuring actions complete (Vibe):** "After clicking 'Load More', wait for the new items to appear. They usually show up in a `div` with class `comment-list` and we expect more than 10 comments."
            *   **AI's understanding:** Use `wait_for`. This can be a CSS selector (e.g., `wait_for="css:.comment-list .comment-item:nth-child(11)"`) or a JS condition (e.g., `wait_for="js:() => document.querySelectorAll('.comment-item').length > 10"`).
        *   **For multi-step interactions on the same page (Vibe):** "I need to first click 'Agree to Cookies', then click 'Show Details', then extract the text. Make sure these happen on the same page view."
            *   **AI's understanding:** "This requires a `session_id` to persist the page state across multiple `arun` calls. Each `arun` call will perform one step of the interaction."
        *   **If only JS interaction is needed (Vibe):** "After the first page load, the next actions (like clicking 'Next Page') only update part of the page with JavaScript, they don't reload everything."
            *   **AI's understanding:** "For these subsequent `arun` calls within the same session, set `js_only=True` in `CrawlerRunConfig` to prevent unnecessary full page navigations, making it faster."
    *   **3.4.4. Taking Screenshots or PDFs:**
        *   **Simple request (Vibe):** "Get me a screenshot of [URL]."
            *   **AI's understanding:** Set `screenshot=True` in `CrawlerRunConfig`.
        *   **Or (Vibe):** "I need a PDF version of [URL]."
            *   **AI's understanding:** Set `pdf=True` in `CrawlerRunConfig`.
    *   **3.4.5. Caching for Speed and Freshness:**
        *   **For faster testing/development (Vibe):** "I'm testing my script for [URL]. Can you make it use the cache so it's faster after the first run?"
            *   **AI's understanding:** Use `cache_mode=CacheMode.ENABLED`.
            *   **Reasoning:** This saves time during development by re-using previously fetched content.
        *   **To get the latest data (Vibe):** "I need the absolute latest version of [URL], don't use any cached data."
            *   **AI's understanding:** Use `cache_mode=CacheMode.BYPASS`.
            *   **Reasoning:** Ensures `crawl4ai` fetches a fresh copy from the web, ignoring any local cache. This is crucial for production or when data changes frequently.

*   **3.5. `BrowserConfig`**: Browser-Level Settings (Simplified for Vibe Coding)
    *   **3.5.1. When it's usually not needed:**
        *   **What to tell your AI (or what it should infer):** "For most simple crawls where you just need to fetch a page and get its content, you probably don't need to worry about `BrowserConfig`. `crawl4ai` uses sensible defaults."
    *   **3.5.2. Headless Mode:**
        *   **Default behavior (Vibe):** "By default, `crawl4ai` runs 'headless', which means you won't see a browser window pop up. This is usually what we want for automated scripts."
        *   **To see the browser (Vibe):** "I'm having trouble with [URL], and I want to see what the browser is doing. Can you make it run in non-headless mode?"
            *   **AI's understanding:** The user wants to visually debug. Set `headless=False` in `BrowserConfig`.
    *   **3.5.3. Using a Proxy:**
        *   **How to ask (Vibe):** "I need to make `crawl4ai` use a proxy server for this crawl."
        *   **Information to provide (Vibe):** "The proxy server address is `http://myproxy.server.com:8080`. If it needs a username and password, they are `myuser` and `mypass`. Make sure to use the `proxy_config` setting in `BrowserConfig`."
            *   **AI's understanding:** The AI should construct a `ProxyConfig` object (or dictionary that `BrowserConfig` can handle) and pass it to `BrowserConfig`.
    *   **3.5.4. Changing User Agent:**
        *   **How to ask (Vibe):** "The website [URL] might be blocking default user agents. Can we make `crawl4ai` look like it's Firefox on a Mac?"
        *   **Information to provide (Vibe):** "You can set a custom `user_agent` string in `BrowserConfig`. For example, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0'."
            *   **AI's understanding:** The AI should pass the provided string to the `user_agent` parameter of `BrowserConfig`.

*   **3.6. `LLMConfig`**: Configuring Language Models (Simplified for Vibe Coding)
    *   **3.6.1. When it's needed:**
        *   **What to tell your AI:** "If we're using `LLMExtractionStrategy` to extract structured data or `LLMContentFilter` to clean up content, we need to tell `crawl4ai` which language model to use. This is done with an `LLMConfig` object."
    *   **3.6.2. Information to provide the AI (Vibe):**
        *   **Model choice:** "For this task, let's use the `provider` called 'openai/gpt-4o-mini'." (Other examples: 'ollama/llama3', 'anthropic/claude-3-opus-20240229').
        *   **API Key:** "My `api_token` for this provider is [YOUR_API_KEY_PLACEHOLDER]. (Best practice is to tell the AI to get it from an environment variable, e.g., 'env:OPENAI_API_KEY')."
            *   **AI's understanding:** The AI will create an `LLMConfig(provider="...", api_token="...")` and pass it to the relevant strategy.
            *   **Code Snippet AI might generate:**
                ```python
                from crawl4ai import LLMConfig
                # For OpenAI
                llm_conf = LLMConfig(provider="openai/gpt-4o-mini", api_token="env:OPENAI_API_KEY")
                # For Ollama (locally running Llama3)
                # llm_conf = LLMConfig(provider="ollama/llama3") # api_token often not needed for local Ollama
                ```

*   **3.7. The `CrawlResult`**: Understanding What You Get Back
    *   **3.7.1. Checking for Success:**
        *   **What to tell your AI (Crucial Vibe):** "When `crawl4ai` finishes an `arun` or `arun_many` call, the most important first step is to check if it was successful. Tell the AI to always generate code that checks `result.success`. This will be `True` or `False`."
        *   **If `False` (Vibe):** "If `result.success` is `False`, the AI should print or log `result.error_message` to tell us what went wrong."
    *   **3.7.2. Accessing Markdown Content:**
        *   **Raw Markdown (Vibe):** "The main text content of the page, converted to Markdown, is usually in `result.markdown.raw_markdown`."
        *   **Filtered Markdown (Vibe):** "If we used a content filter (like `PruningContentFilter`), the cleaner, more focused Markdown will be in `result.markdown.fit_markdown`."
    *   **3.7.3. Accessing Extracted Structured Data (JSON):**
        *   **Where to find it (Vibe):** "If we asked `crawl4ai` to extract specific structured data (using `JsonCssExtractionStrategy` or `LLMExtractionStrategy`), that data will be in `result.extracted_content`."
        *   **How to use it (Vibe):** "The `result.extracted_content` is a JSON string. To use it in Python, tell the AI to parse it using `json.loads()`."
    *   **3.7.4. Accessing Links:**
        *   **What it contains (Vibe):** "`result.links` is a dictionary. It usually has two keys: 'internal' and 'external'. Each of these is a list of links found on the page, with details like the link text and URL."
    *   **3.7.5. Accessing Media Information:**
        *   **What it contains (Vibe):** "`result.media` is another dictionary. It can contain lists of 'images', 'videos', or 'audios' found on the page, along with their URLs and sometimes alt text or descriptions."
    *   **3.7.6. Accessing Screenshots and PDFs:**
        *   **Screenshots (Vibe):** "If we set `screenshot=True` in the config, the screenshot image data (which is a base64 encoded string) will be in `result.screenshot`."
        *   **PDFs (Vibe):** "If we set `pdf=True`, the PDF data (as raw bytes) will be in `result.pdf`."

## 4. Common "Vibe" Recipes & Prompting Patterns for AI Assistants

Here are some common scenarios and how you can prompt your AI assistant to use `crawl4ai` to solve them.

*   **4.1. Recipe 1: Get Clean Markdown from a Page**
    *   **4.1.1. User Vibe Prompt to AI:**
        *   *Example 1 (Basic):* "Hey AI, can you use `crawl4ai` to get me the clean Markdown content of `https://blog.example.com/my-latest-post`?"
        *   *Example 2 (Requesting more cleaning):* "AI, I need *very* clean Markdown from `https://some.news.site/article123`. It's for an LLM, so please try to remove ads, navigation, and footers."
    *   **4.1.2. Key `crawl4ai` elements the AI should use (and why):**
        *   **`AsyncWebCrawler`:** The starting point for any crawl.
        *   **`arun`:** Since it's a single URL.
        *   **`CrawlerRunConfig`:**
            *   For Example 1, the default `DefaultMarkdownGenerator` might be sufficient.
            *   For Example 2 ("very clean"), the AI should be guided to use `DefaultMarkdownGenerator(content_filter=PruningContentFilter())`.
            *   **Reasoning:** `PruningContentFilter` is designed to heuristically remove common boilerplate like headers, footers, and navigation bars before Markdown conversion, leading to cleaner text suitable for LLMs.
    *   **4.1.3. Expected Output from AI-generated code:**
        *   A Python script that initializes `AsyncWebCrawler`, calls `arun` with the appropriate URL and config.
        *   The script should then access and print (or save) `result.markdown.raw_markdown` (for basic) or `result.markdown.fit_markdown` (if `PruningContentFilter` was used).
        *   **Code Example (for "very clean"):**
            ```python
            import asyncio
            from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DefaultMarkdownGenerator
            from crawl4ai.content_filter_strategy import PruningContentFilter

            async def get_clean_markdown(url_to_crawl):
                markdown_generator = DefaultMarkdownGenerator(
                    content_filter=PruningContentFilter()
                )
                run_config = CrawlerRunConfig(
                    markdown_generator=markdown_generator,
                    cache_mode="BYPASS" # Ensure fresh crawl for demo
                )
                async with AsyncWebCrawler() as crawler:
                    result = await crawler.arun(url=url_to_crawl, config=run_config)
                    if result.success:
                        print(f"--- Fit Markdown for {url_to_crawl} ---")
                        print(result.markdown.fit_markdown)
                        # You might also want to see raw_markdown to compare
                        # print(f"--- Raw Markdown for {url_to_crawl} ---")
                        # print(result.markdown.raw_markdown)
                    else:
                        print(f"Failed to crawl {url_to_crawl}: {result.error_message}")

            # asyncio.run(get_clean_markdown("https://en.wikipedia.org/wiki/Python_(programming_language)"))
            ```

*   **4.2. Recipe 2: Extract All Product Names and Prices from an E-commerce Category Page**
    *   **4.2.1. User Vibe Prompt to AI:**
        *   *Example:* "AI, I need to use `crawl4ai` to get all product names and their prices from `https://www.example-store.com/laptops`. On that page, product names look like they are in `<h3>` tags with a class `product-title`, and prices are in `<span>` elements with the class `final-price`."
    *   **4.2.2. Key `crawl4ai` elements AI should use (and why):**
        *   **`AsyncWebCrawler`**, **`arun`**.
        *   **`CrawlerRunConfig`** with **`JsonCssExtractionStrategy`**.
            *   **Reasoning:** The user described a page with repeating structured items. `JsonCssExtractionStrategy` is ideal for this as it uses CSS selectors to pinpoint the data. The AI's task is to translate the user's description of element locations into a valid schema for the strategy.
            *   The AI needs to understand that `baseSelector` in the schema should target the container for each product, and `fields` will target individual pieces of data within that container.
    *   **4.2.3. Expected Output from AI-generated code:**
        *   A Python script that defines the schema dictionary.
        *   Initializes `JsonCssExtractionStrategy` with this schema.
        *   Passes the strategy to `CrawlerRunConfig`.
        *   After `arun`, it parses `result.extracted_content` using `json.loads()` and likely iterates through the list of extracted product dictionaries.
        *   **Code Example:**
            ```python
            import asyncio
            import json
            from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
            from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

            async def extract_products(url_to_crawl):
                # AI helps create this schema based on user's description
                product_schema = {
                    "name": "LaptopList",
                    "baseSelector": "div.product-listing-item", # Hypothetical selector for each product's container
                    "fields": [
                        {"name": "product_name", "selector": "h3.product-title", "type": "text"},
                        {"name": "price", "selector": "span.final-price", "type": "text"}
                    ]
                }
                extraction_strategy = JsonCssExtractionStrategy(schema=product_schema)
                run_config = CrawlerRunConfig(
                    extraction_strategy=extraction_strategy,
                    cache_mode="BYPASS"
                )
                async with AsyncWebCrawler() as crawler:
                    result = await crawler.arun(url=url_to_crawl, config=run_config)
                    if result.success and result.extracted_content:
                        products = json.loads(result.extracted_content)
                        print(f"Found {len(products)} products:")
                        for i, product in enumerate(products[:3]): # Print first 3
                            print(f"  Product {i+1}: Name='{product.get('product_name')}', Price='{product.get('price')}'")
                    else:
                        print(f"Failed to extract products from {url_to_crawl}: {result.error_message}")

            # asyncio.run(extract_products("https://www.example-store.com/laptops")) # Replace with a real URL for testing
            ```

*   **4.3. Recipe 3: Extract Key Information from an Article using an LLM**
    *   **4.3.1. User Vibe Prompt to AI:**
        *   *Example:* "AI, I want `crawl4ai` to read this article: `https://example.com/news/ai-breakthrough`. Use `openai/gpt-4o-mini` to extract the author's name, the publication date, and a short (2-3 sentence) summary. The output should be JSON. My OpenAI API key is in the `OPENAI_API_KEY` environment variable."
    *   **4.3.2. Key `crawl4ai` elements AI should use (and why):**
        *   **`AsyncWebCrawler`**, **`arun`**.
        *   **`CrawlerRunConfig`** with **`LLMExtractionStrategy`**.
        *   **`LLMConfig`**: To specify the `provider` ("openai/gpt-4o-mini") and `api_token` ("env:OPENAI_API_KEY").
            *   **Reasoning:** The task requires understanding and summarization, making `LLMExtractionStrategy` suitable. The AI needs to construct a schema (either a simple dictionary or a Pydantic model `model_json_schema()`) that tells the LLM what fields to populate. The instruction to the LLM will be implicitly derived from the schema field descriptions or can be explicitly provided.
    *   **4.3.3. Expected Output from AI-generated code:**
        *   Python script that defines a Pydantic model (or a dictionary schema).
        *   Initializes `LLMConfig` and `LLMExtractionStrategy`.
        *   Parses `result.extracted_content`.
        *   **Code Example (using Pydantic):**
            ```python
            import asyncio
            import json
            import os
            from pydantic import BaseModel, Field
            from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig
            from crawl4ai.extraction_strategy import LLMExtractionStrategy

            class ArticleDetails(BaseModel):
                author_name: str = Field(..., description="The main author of the article.")
                publication_date: str = Field(..., description="The date the article was published (e.g., YYYY-MM-DD).")
                summary: str = Field(..., description="A concise 2-3 sentence summary of the article.")

            async def extract_article_info_llm(url_to_crawl):
                if not os.getenv("OPENAI_API_KEY"): # Or your specific key variable
                    print("API key environment variable not set. Skipping LLM extraction.")
                    return

                llm_config = LLMConfig(
                    provider="openai/gpt-4o-mini", # Use a cost-effective model for demos
                    api_token="env:OPENAI_API_KEY"
                )
                extraction_strategy = LLMExtractionStrategy(
                    llm_config=llm_config,
                    schema=ArticleDetails.model_json_schema(),
                    extraction_type="schema" # Crucial for Pydantic/JSON schema
                )
                run_config = CrawlerRunConfig(
                    extraction_strategy=extraction_strategy,
                    cache_mode="BYPASS"
                )
                async with AsyncWebCrawler() as crawler:
                    result = await crawler.arun(url=url_to_crawl, config=run_config)
                    if result.success and result.extracted_content:
                        try:
                            article_data = ArticleDetails.model_validate_json(result.extracted_content)
                            print(f"Extracted Article Info for {url_to_crawl}:")
                            print(json.dumps(article_data.model_dump(), indent=2))
                        except Exception as e:
                            print(f"Error parsing LLM output: {e}")
                            print(f"Raw LLM output: {result.extracted_content}")
                    else:
                        print(f"Failed to extract article info from {url_to_crawl}: {result.error_message}")

            # asyncio.run(extract_article_info_llm("https://www.example.com/news/ai-breakthrough")) # Replace with real article
            ```

*   **4.4. Recipe 4: Crawl the first 3 pages of a blog (clicking "Next Page")**
    *   **4.4.1. User Vibe Prompt to AI:**
        *   *Example:* "AI, can you use `crawl4ai` to get the Markdown from the first 3 pages of `https://myblog.example.com/archive`? To get to the next page, I think you need to click a link that says 'Older Posts'."
    *   **4.4.2. Key `crawl4ai` elements AI should use (and why):**
        *   **`AsyncWebCrawler`**.
        *   **Multiple `arun` calls** in a loop (3 iterations).
        *   **`CrawlerRunConfig`** with:
            *   `session_id="blog_session"`: **Crucial** for maintaining the browser state (cookies, current page) across the multiple clicks.
            *   `js_code`: JavaScript to find and click the "Older Posts" link. The AI might need to generate robust JS like:
                `Array.from(document.querySelectorAll('a')).find(a => a.textContent.trim() === 'Older Posts')?.click();`
            *   `wait_for`: After clicking, wait for a condition that indicates the next page has loaded (e.g., a specific element on the new page, or a change in an existing element). This can be tricky and might require some iteration. A simple `wait_for` for a few seconds could also be a starting point, like `wait_for=3000` (milliseconds).
            *   `js_only=True`: For the second and third `arun` calls, after the initial page load. This tells `crawl4ai` to only execute the JS and not perform a full new navigation to the original URL.
    *   **4.4.3. Expected Output from AI-generated code:**
        *   A Python script with a loop that calls `arun` three times.
        *   The script should collect and potentially print or save the Markdown from each page.
        *   **Code Example:**
            ```python
            import asyncio
            from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

            async def crawl_blog_pages(start_url, num_pages=3):
                session_id = "my_blog_crawl_session"
                all_markdowns = []

                # JavaScript to find and click "Older Posts" (example)
                js_click_older_posts = """
                (() => {
                    const links = Array.from(document.querySelectorAll('a'));
                    const olderPostsLink = links.find(a => a.textContent.trim().toLowerCase() === 'older posts');
                    if (olderPostsLink) {
                        olderPostsLink.click();
                        return true; // Indicate click was attempted
                    }
                    return false; // Indicate link not found
                })();
                """

                async with AsyncWebCrawler() as crawler:
                    current_url = start_url
                    for i in range(num_pages):
                        print(f"Crawling page {i+1}...")
                        run_config_dict = {
                            "session_id": session_id,
                            "cache_mode": CacheMode.BYPASS,
                            "wait_for": 2000 # Wait 2s for content to potentially load after click
                        }
                        if i > 0: # For subsequent pages, click and don't re-navigate
                            run_config_dict["js_code"] = js_click_older_posts
                            run_config_dict["js_only"] = True
                        
                        run_config = CrawlerRunConfig(**run_config_dict)
                        
                        result = await crawler.arun(url=current_url, config=run_config) # URL is mainly for context in js_only
                        
                        if result.success:
                            print(f"  Page {i+1} ({result.url}) - Markdown length: {len(result.markdown.raw_markdown)}")
                            all_markdowns.append({"url": result.url, "markdown": result.markdown.raw_markdown})
                            if i < num_pages - 1 and i > 0 and not run_config_dict.get("js_code_executed_successfully", True): # Hypothetical flag
                                print(f"  'Older Posts' link might not have been found or clicked on page {i+1}. Stopping.")
                                break
                        else:
                            print(f"  Failed to crawl page {i+1}: {result.error_message}")
                            break
                    
                    # Important: Clean up the session
                    await crawler.crawler_strategy.kill_session(session_id) 
                
                print(f"\nCollected markdown for {len(all_markdowns)} pages.")
                # For demo, print first 100 chars of each
                # for i, md_data in enumerate(all_markdowns):
                #     print(f"\n--- Page {i+1} URL: {md_data['url']} ---")
                #     print(md_data['markdown'][:100] + "...")

            # asyncio.run(crawl_blog_pages("YOUR_BLOG_START_URL_HERE"))
            ```

*   **4.5. Recipe 5: Get Screenshots of a List of URLs**
    *   **4.5.1. User Vibe Prompt to AI:**
        *   *Example:* "AI, use `crawl4ai` to take a screenshot of each of these pages: `https://example.com`, `https://crawl4ai.com`, `https://github.com`. Save them as `example_com.png`, `crawl4ai_com.png`, and `github_com.png`."
    *   **4.5.2. Key `crawl4ai` elements AI should use (and why):**
        *   **`AsyncWebCrawler`**.
        *   **`arun_many`**: Efficient for processing a list of URLs.
        *   **`CrawlerRunConfig`** with `screenshot=True`.
            *   **Reasoning:** `arun_many` will process each URL with the same config. The AI needs to add logic to iterate through the results and save each `result.screenshot` (which is base64 data) to a uniquely named file.
    *   **4.5.3. Expected Output from AI-generated code:**
        *   Python script.
        *   PNG files saved to the current directory or a specified output directory.
        *   **Code Example:**
            ```python
            import asyncio
            import base64
            import os
            from urllib.parse import urlparse
            from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

            async def take_screenshots(urls_to_screenshot):
                run_config = CrawlerRunConfig(
                    screenshot=True,
                    cache_mode=CacheMode.BYPASS # Get fresh screenshots
                )
                output_dir = "screenshots_output"
                os.makedirs(output_dir, exist_ok=True)

                async with AsyncWebCrawler() as crawler:
                    results = await crawler.arun_many(urls=urls_to_screenshot, config=run_config)
                    
                    for result in results:
                        if result.success and result.screenshot:
                            # Create a filename from the URL
                            parsed_url = urlparse(result.url)
                            filename = "".join(c if c.isalnum() else '_' for c in parsed_url.netloc + parsed_url.path)
                            if not filename or filename == "_": # Handle root path or empty paths
                                filename = "homepage"
                            filepath = os.path.join(output_dir, f"{filename}.png")
                            
                            try:
                                screenshot_data = base64.b64decode(result.screenshot)
                                with open(filepath, "wb") as f:
                                    f.write(screenshot_data)
                                print(f"Screenshot saved to {filepath}")
                            except Exception as e:
                                print(f"Error saving screenshot for {result.url}: {e}")
                        elif not result.success:
                            print(f"Failed to crawl {result.url}: {result.error_message}")
                        elif not result.screenshot:
                            print(f"Crawled {result.url} but no screenshot data was returned.")
            
            # urls = ["https://example.com", "https://crawl4ai.com", "https://github.com"]
            # asyncio.run(take_screenshots(urls))
            ```

## 5. Tips for Effective Prompting Your AI Assistant for Crawl4AI Tasks

To get the best code from your AI assistant when working with `crawl4ai`, consider these prompting tips:

*   **5.1. Be Clear About Your Goal:**
    *   Start with a high-level objective. Instead of just "Crawl a page," say "I need to extract all article titles from the homepage of this news site," or "Get the main content of this blog post as clean Markdown," or "Take full-page screenshots of these product pages." This helps the AI choose the right strategies and configurations.

*   **5.2. Always Provide the URL(s):**
    *   This seems obvious, but be precise. If it's a list, provide the list.
    *   Remember to use the `file:///` prefix for local files (e.g., `file:///Users/me/Documents/mypage.html`) and `raw:` for inline HTML (e.g., `raw:<html><body>...</body></html>`). The AI might not always infer this correctly without a hint.

*   **5.3. Describe Data for Extraction (Especially for `JsonCssExtractionStrategy` or `LLMExtractionStrategy`):**
    *   **What you want:** List the specific pieces of information you need (e.g., "product name," "price," "author," "publication_date," "article summary").
    *   **Where to find it (for CSS/XPath):** If you have an idea of the HTML structure, share it. "Product names seem to be in `<h2>` tags with class `item-title`." "The price is always in a `<span>` element right after a `<strong>` tag that says 'Price:'." This helps the AI generate accurate CSS selectors or XPath expressions for `JsonCssExtractionStrategy`.
    *   **Desired structure (for LLM):** For `LLMExtractionStrategy`, tell the AI the desired JSON structure. "I want a list of objects, where each object has a 'title' and a 'link'." Or even better, "Can you define a Pydantic model for me that has 'title' as a string and 'link' as a string, and then use that for extraction?"

*   **5.4. Specify LLM Details for LLM Extraction or Filtering:**
    *   **Model/Provider:** "Use `openai/gpt-4o-mini` for this extraction." or "I want to use my local Ollama model, `ollama/llama3`."
    *   **API Key:** Clearly state where the API key should come from. "My API key is in the environment variable `OPENAI_API_KEY`." (This is safer than putting the key directly in the prompt). If you must provide it directly, be aware of the security implications.

*   **5.5. Mention Page Dynamics and Interactions:**
    *   "This page loads more items when you scroll down."
    *   "You need to click the 'View All Reviews' button to see all the reviews."
    *   "The data I want only appears after selecting 'Category X' from a dropdown."
    *   This signals to the AI that `js_code`, `wait_for`, and possibly `session_id` will be necessary. You might need to guide it on *how* to identify the elements to interact with (e.g., "The 'Load More' button has the ID `load-more-btn`").

*   **5.6. Iterative Refinement is Key:**
    *   Your first prompt might not yield perfect code. That's okay!
    *   Treat it as a conversation. If the AI-generated code misses something or makes a mistake:
        *   "That was close, but it missed extracting the product ratings. Ratings seem to be in a `div` with class `star-rating` inside each product item."
        *   "The script timed out. Can we increase the `page_timeout` in `CrawlerRunConfig` to 90 seconds?"
        *   "It didn't click the 'Next' button correctly. The button actually has the text '>>' instead of 'Next Page'."
    *   Provide the error messages or incorrect output back to the AI for context.

## 6. What to Expect as Output (From AI-Generated Code)

When you use "Vibe Coding" with an AI assistant for `crawl4ai`, you should generally expect the following:

*   **6.1. Python Code:**
    *   The primary output will be a Python script that uses the `crawl4ai` library.
    *   It should include necessary imports like `asyncio`, `AsyncWebCrawler`, `CrawlerRunConfig`, etc.
    *   It will typically define an `async def main():` function and run it with `asyncio.run(main())`.

*   **6.2. Accessing the `CrawlResult`:**
    *   The core of the script will involve one or more calls to `crawler.arun(...)` or `crawler.arun_many(...)`.
    *   These calls return `CrawlResult` objects (or a list of them for `arun_many`).
    *   The AI-generated code should then show you how to access the specific data you asked for from these `CrawlResult` objects. For example:
        *   `print(result.markdown.raw_markdown)` or `print(result.markdown.fit_markdown)`
        *   `data = json.loads(result.extracted_content)`
        *   `screenshot_data = base64.b64decode(result.screenshot)`
        *   `if not result.success: print(result.error_message)`

*   **6.3. Files Saved to Disk (if requested):**
    *   If your vibe prompt included saving data (e.g., "save the screenshots as PNG files," "write the extracted JSON to `output.json`"), the AI-generated code should include the Python logic to perform these file operations.
    *   **Example for saving a screenshot:**
        ```python
        import base64
        # ... inside your async function, after getting 'result' ...
        if result.success and result.screenshot:
            with open("myscreenshot.png", "wb") as f:
                f.write(base64.b64decode(result.screenshot))
            print("Screenshot saved to myscreenshot.png")
        ```

## 7. Conclusion: Vibe Your Way to Web Data!

*   **7.1. Recap of "Vibe Coding" Benefits with `crawl4ai`:**
    "Vibe Coding" empowers you to leverage the full capabilities of `crawl4ai` without needing to memorize every API detail. By understanding the high-level concepts and key building blocks outlined in this guide, you can effectively communicate your data extraction and web interaction needs to an AI coding assistant. This leads to faster prototyping, easier access to web data for non-programmers, and a more intuitive way to build data-driven applications.

*   **7.2. Encouragement to experiment with different prompts and `crawl4ai` features:**
    The key to successful "Vibe Coding" is experimentation. Try different ways of describing your goals to your AI assistant. If the first attempt doesn't yield the perfect `crawl4ai` code, refine your prompt with more specific details or hints. Don't be afraid to mention `crawl4ai` specific terms like `CrawlerRunConfig`, `js_code`, or `LLMExtractionStrategy` – this guide has equipped you with the essential vocabulary. The more context you provide, the better the AI can assist you.

*   **7.3. Pointers to more detailed `crawl4ai` documentation for users who want to learn direct coding or advanced configurations:**
    While "Vibe Coding" is a great way to get started and be productive quickly, you might eventually want to dive deeper into `crawl4ai`'s capabilities or fine-tune the generated code yourself. For that, refer to:
    *   **The Official Crawl4AI API Reference:** (Assuming this exists or will exist - replace with actual link if available, e.g., `https://docs.crawl4ai.com/api/`) For detailed information on all classes, methods, and parameters.
    *   **Specific "Reasoning & Problem-Solving" Guides:** Check the `crawl4ai` documentation for other guides that delve into specific components like advanced `CrawlerRunConfig` options, deep crawling strategies, or custom extraction techniques.

Happy Vibe Coding, and may your web data adventures be fruitful!
```

## Content (Examples)

# Examples Outline for crawl4ai - vibe Component

**Target Document Type:** Examples Collection
**Target Output Filename Suggestion:** `llm_examples_vibe.md`
**Library Version Context:** 0.6.3
**Outline Generation Date:** 2024-05-24
---

This document provides a collection of runnable code examples for the `vibe` component of the `crawl4ai` library, focusing on its deep crawling capabilities, filtering, and scoring mechanisms.

**Note on URLs:** Most examples use placeholder URLs like `https://docs.crawl4ai.com/vibe-examples/pageN.html`. These are for demonstration and will be mocked to return predefined content. Replace them with actual URLs for real-world use.

**Common Imports (assumed for many examples below, but will be included in each runnable block):**
```python
import asyncio
import time
import re
from pathlib import Path
import os # For local file examples
from crawl4ai import (
    AsyncWebCrawler,
    CrawlerRunConfig,
    CrawlResult,
    BrowserConfig,
    CacheMode,
    # Deep Crawling Strategies
    BFSDeePCrawlStrategy,
    DFSDeePCrawlStrategy,
    BestFirstCrawlingStrategy,
    DeepCrawlStrategy, # For custom strategy
    # Filters
    FilterChain,
    URLPatternFilter,
    DomainFilter,
    ContentTypeFilter,
    URLFilter,
    ContentRelevanceFilter, # Conceptual
    SEOFilter,            # Conceptual
    FilterStats,
    # Scorers
    URLScorer, # For custom scorer
    KeywordRelevanceScorer,
    PathDepthScorer,
    ContentTypeScorer,
    DomainAuthorityScorer, # Conceptual
    FreshnessScorer,       # Conceptual
    CompositeScorer,
    # Other
    LLMExtractionStrategy, # For combination example
    AsyncLogger          # For custom logger example
)
from unittest.mock import patch, AsyncMock # For mocking network calls

# --- Mock Website Data ---
# This data will be used by the MockAsyncWebCrawler to simulate a website
MOCK_SITE_DATA = {
    "https://docs.crawl4ai.com/vibe-examples/index.html": {
        "html_content": """
            <html><head><title>Index</title></head><body>
                <h1>Main Page</h1>
                <a href="page1.html">Page 1</a>
                <a href="page2.html">Page 2 (Feature)</a>
                <a href="https://external-site.com/pageA.html">External Site</a>
                <a href="/vibe-examples/archive/old_page.html">Archive</a>
                <a href="/vibe-examples/blog/post1.html">Blog Post 1</a>
                <a href="/vibe-examples/login.html">Login</a>
                <a href="javascript:void(0);" onclick="document.body.innerHTML += '<a href=js_page.html>JS Link</a>'">Load JS Link</a>
            </body></html>
        """,
        "response_headers": {"Content-Type": "text/html"}
    },
    "https://docs.crawl4ai.com/vibe-examples/page1.html": {
        "html_content": """
            <html><head><title>Page 1</title></head><body>
                <h2>Page One</h2>
                <p>This is page 1. It has some core content about crawl strategies.</p>
                <a href="page1_sub1.html">Sub Page 1.1</a>
                <a href="page1_sub2.pdf">Sub Page 1.2 (PDF)</a>
                <a href="index.html">Back to Index</a>
            </body></html>
        """,
        "response_headers": {"Content-Type": "text/html"}
    },
    "https://docs.crawl4ai.com/vibe-examples/page1_sub1.html": {
        "html_content": "<html><head><title>Sub Page 1.1</title></head><body><p>Sub page 1.1 content. More on core concepts.</p></body></html>",
        "response_headers": {"Content-Type": "text/html"}
    },
    "https://docs.crawl4ai.com/vibe-examples/page1_sub2.pdf": {
        "html_content": "%PDF-1.4 ... (Mock PDF Content: Crawl examples)", # Mock PDF content
        "response_headers": {"Content-Type": "application/pdf"}
    },
    "https://docs.crawl4ai.com/vibe-examples/page2.html": {
        "html_content": """
            <html><head><title>Page 2 - Feature Rich</title></head><body>
                <h2>Page Two with Feature</h2>
                <p>This page discusses a key feature and advanced configuration for async tasks.</p>
                <a href="page2_sub1.html">Sub Page 2.1</a>
            </body></html>
        """,
        "response_headers": {"Content-Type": "text/html"}
    },
    "https://docs.crawl4ai.com/vibe-examples/page2_sub1.html": {
        "html_content": "<html><head><title>Sub Page 2.1</title></head><body><p>More about the feature and JavaScript interaction.</p></body></html>",
        "response_headers": {"Content-Type": "text/html"}
    },
    "https://docs.crawl4ai.com/vibe-examples/archive/old_page.html": {
        "html_content": "<html><head><title>Old Page</title></head><body><p>Archived content, less relevant.</p></body></html>",
        "response_headers": {"Content-Type": "text/html"}
    },
    "https://docs.crawl4ai.com/vibe-examples/blog/post1.html": {
        "html_content": "<html><head><title>Blog Post 1</title></head><body><p>This is a blog post about core ideas and examples.</p></body></html>",
        "response_headers": {"Content-Type": "text/html"}
    },
     "https://docs.crawl4ai.com/vibe-examples/login.html": {
        "html_content": "<html><head><title>Login</title></head><body><form>...</form></body></html>",
        "response_headers": {"Content-Type": "text/html"}
    },
    "https://docs.crawl4ai.com/vibe-examples/js_page.html": {
        "html_content": "<html><head><title>JS Page</title></head><body><p>Content loaded by JavaScript.</p></body></html>",
        "response_headers": {"Content-Type": "text/html"}
    },
    "https://external-site.com/pageA.html": {
        "html_content": "<html><head><title>External Page A</title></head><body><p>Content from external site about other topics.</p></body></html>",
        "response_headers": {"Content-Type": "text/html"}
    },
    # For local file examples
    "file:" + str(Path(os.getcwd()) / "test_local_index.html"): {
         "html_content": """
            <html><head><title>Local Index</title></head><body>
                <h1>Local Main Page</h1>
                <a href="test_local_page1.html">Local Page 1</a>
                <a href="https://docs.crawl4ai.com/vibe-examples/index.html">Web Index</a>
            </body></html>
        """,
        "response_headers": {"Content-Type": "text/html"}
    },
    "file:" + str(Path(os.getcwd()) / "test_local_page1.html"): {
        "html_content": "<html><head><title>Local Page 1</title></head><body><p>Local page 1 content.</p></body></html>",
        "response_headers": {"Content-Type": "text/html"}
    }
}

# Create a dummy local file for testing
Path("test_local_index.html").write_text(MOCK_SITE_DATA["file:" + str(Path(os.getcwd()) / "test_local_index.html")]["html_content"])
Path("test_local_page1.html").write_text(MOCK_SITE_DATA["file:" + str(Path(os.getcwd()) / "test_local_page1.html")]["html_content"])


# --- Mock AsyncWebCrawler ---
# This mock crawler will simulate fetching pages from MOCK_SITE_DATA
class MockAsyncWebCrawler(AsyncWebCrawler):
    async def _fetch_page(self, url: str, config: CrawlerRunConfig):
        # Simulate network delay
        await asyncio.sleep(0.01)
        
        # Normalize URL for lookup (e.g. relative to absolute)
        if not url.startswith("file:") and not url.startswith("http"):
            # This is a simplified relative URL resolver for the mock
            base_parts = self.current_url.split('/')[:-1] if hasattr(self, 'current_url') and self.current_url else []
            normalized_url = "/".join(base_parts + [url])
            if "docs.crawl4ai.com" not in normalized_url and not normalized_url.startswith("file:"): # ensure base domain
                 normalized_url = "https://docs.crawl4ai.com/vibe-examples/" + url.lstrip("/")
        else:
            normalized_url = url

        if normalized_url in MOCK_SITE_DATA:
            page_data = MOCK_SITE_DATA[normalized_url]
            self.current_url = normalized_url # Store for relative path resolution
            
            # Basic link extraction for deep crawling
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(page_data["html_content"], 'html.parser')
            links = []
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                # Simple relative to absolute conversion for mock
                if not href.startswith("http") and not href.startswith("file:") and not href.startswith("javascript:"):
                    abs_href = "/".join(normalized_url.split('/')[:-1]) + "/" + href.lstrip("./")
                     # Further simplify to ensure it hits mock data, very basic
                    if "docs.crawl4ai.com" in abs_href: # if it's a vibe-example page
                        abs_href = "https://docs.crawl4ai.com/vibe-examples/" + Path(href).name
                    elif "external-site.com" in abs_href:
                        abs_href = "https://external-site.com/" + Path(href).name

                elif href.startswith("file:"): # Keep file URLs as is
                    abs_href = href
                elif href.startswith("javascript:"):
                    abs_href = None # Skip JS links for this mock
                else:
                    abs_href = href
                
                if abs_href:
                    links.append({"href": abs_href, "text": a_tag.get_text(strip=True)})

            return CrawlResult(
                url=normalized_url,
                html_content=page_data["html_content"],
                success=True,
                status_code=200,
                response_headers=page_data.get("response_headers", {"Content-Type": "text/html"}),
                links={"internal": [l for l in links if "docs.crawl4ai.com/vibe-examples" in l["href"] or l["href"].startswith("file:")], 
                       "external": [l for l in links if "external-site.com" in l["href"]]}
            )
        else:
            # print(f"Mock Warning: URL not found in MOCK_SITE_DATA: {normalized_url} (Original: {url})")
            return CrawlResult(
                url=url, html_content="", success=False, status_code=404, error_message="Mock URL not found"
            )

    async def arun(self, url: str, config: CrawlerRunConfig = None, **kwargs):
        # This is the method called by DeepCrawlStrategy instances
        # For deep crawls, the strategy itself calls this multiple times.
        # For a single arun call with a deep_crawl_strategy, the decorator handles it.
        
        if config and config.deep_crawl_strategy:
             # The decorator usually handles this part. For direct strategy.arun() tests:
            return await config.deep_crawl_strategy.arun(
                crawler=self, # Pass the mock crawler instance
                start_url=url,
                config=config
            )
        
        # Fallback to single page fetch if no deep crawl strategy
        self.current_url = url # Set for relative path resolution in _fetch_page
        return await self._fetch_page(url, config)

    async def arun_many(self, urls: list[str], config: CrawlerRunConfig = None, **kwargs):
        results = []
        for url_item in urls:
            # In BestFirst, arun_many is called with tuples of (score, depth, url, parent_url)
            # For simplicity in mock, we assume url_item is just the URL string here or a tuple where url is at index 2
            current_url_to_crawl = url_item
            if isinstance(url_item, tuple) and len(url_item) >=3 :
                 current_url_to_crawl = url_item[2]

            self.current_url = current_url_to_crawl # Set for relative path resolution
            result = await self._fetch_page(current_url_to_crawl, config)
            results.append(result)
        if config and config.stream:
            async def result_generator():
                for res in results:
                    yield res
            return result_generator()
        return results

    async def __aenter__(self):
        # print("MockAsyncWebCrawler entered")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # print("MockAsyncWebCrawler exited")
        pass
    
    async def start(self): # Add start method
        # print("MockAsyncWebCrawler started")
        self.ready = True
        return self

    async def close(self): # Add close method
        # print("MockAsyncWebCrawler closed")
        self.ready = False

# --- End Mock ---
```

---
## 1. Introduction to Deep Crawling (`vibe`)

The `vibe` component of Crawl4ai provides powerful deep crawling capabilities, allowing you to traverse websites by following links and processing multiple pages.

### 1.1. Example: Enabling Basic Deep Crawl with `BFSDeePCrawlStrategy` via `CrawlerRunConfig`.
This example demonstrates how to enable a basic Breadth-First Search (BFS) deep crawl by setting the `deep_crawl_strategy` in `CrawlerRunConfig`.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy
from unittest.mock import patch

# Using the MockAsyncWebCrawler defined in the preamble
@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def basic_bfs_deep_crawl():
    # Configure BFS to crawl up to 1 level deep from the start URL
    bfs_strategy = BFSDeePCrawlStrategy(max_depth=1)
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=bfs_strategy,
        # For mock, ensure cache is bypassed to see fresh mock results
        cache_mode=CacheMode.BYPASS 
    )

    # The actual AsyncWebCrawler is replaced by MockAsyncWebCrawler via @patch
    async with AsyncWebCrawler() as crawler: # This will be MockAsyncWebCrawler
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- Basic BFS Deep Crawl (max_depth=1) ---")
        print(f"Crawled {len(results)} pages starting from {start_url}:")
        for i, result in enumerate(results):
            if result.success:
                print(f"  {i+1}. URL: {result.url}, Depth: {result.metadata.get('depth')}, Parent: {result.metadata.get('parent_url')}")
            else:
                print(f"  {i+1}. FAILED: {result.url}, Error: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(basic_bfs_deep_crawl())
```

### 1.2. Example: Understanding `CrawlResult.metadata` (depth, parent_url, score) in Deep Crawl Results.
Each `CrawlResult` from a deep crawl contains useful metadata like the crawl `depth`, the `parent_url` from which it was discovered, and a `score` (if applicable, e.g., with `BestFirstCrawlingStrategy`).

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, KeywordRelevanceScorer, BestFirstCrawlingStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def understand_metadata():
    # Using BestFirstCrawlingStrategy to demonstrate scores
    scorer = KeywordRelevanceScorer(keywords=["feature", "core"])
    strategy = BestFirstCrawlingStrategy(max_depth=1, url_scorer=scorer)
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- Understanding CrawlResult.metadata ---")
        for result in results:
            if result.success:
                depth = result.metadata.get('depth', 'N/A')
                parent = result.metadata.get('parent_url', 'N/A')
                score = result.metadata.get('score', 'N/A') # Score comes from BestFirst strategy
                print(f"URL: {result.url}")
                print(f"  Depth: {depth}")
                print(f"  Parent URL: {parent}")
                print(f"  Score: {score if score != 'N/A' else 'N/A (not scored or BFS/DFS)'}")
                print("-" * 20)

if __name__ == "__main__":
    asyncio.run(understand_metadata())
```

### 1.3. Example: Minimal setup for deep crawling a single level deep.
This demonstrates the most straightforward way to perform a shallow deep crawl (depth 1).

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def minimal_single_level_deep_crawl():
    # BFS strategy, max_depth=1 means start_url + its direct links
    strategy = BFSDeePCrawlStrategy(max_depth=1) 
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- Minimal Single Level Deep Crawl (max_depth=1) ---")
        print(f"Total pages crawled: {len(results)}")
        for result in results:
            if result.success:
                print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")

if __name__ == "__main__":
    asyncio.run(minimal_single_level_deep_crawl())
```

---
## 2. Breadth-First Search (`BFSDeePCrawlStrategy`) Examples

`BFSDeePCrawlStrategy` explores the website level by level.

### 2.1. Example: Basic `BFSDeePCrawlStrategy` with default depth.
The default `max_depth` for `BFSDeePCrawlStrategy` is often 1 if not specified, meaning it crawls the start URL and its direct links.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def bfs_default_depth():
    # Default max_depth is typically 1 (start_url + its direct children)
    # but let's be explicit for clarity or test with a higher default if library changes
    strategy = BFSDeePCrawlStrategy() # Default max_depth is 1
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- BFS with Default Depth (max_depth=1) ---")
        print(f"Crawled {len(results)} pages.")
        for result in results:
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")

if __name__ == "__main__":
    asyncio.run(bfs_default_depth())
```

### 2.2. Example: `BFSDeePCrawlStrategy` - Setting `max_depth` to control crawl depth (e.g., 3 levels).
Control how many levels deep the BFS crawler will go from the start URL. `max_depth=0` means only the start URL. `max_depth=1` means start URL + its direct links.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def bfs_set_max_depth():
    strategy = BFSDeePCrawlStrategy(max_depth=2) # Start URL (0), its links (1), and their links (2)
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- BFS with max_depth=2 ---")
        print(f"Crawled {len(results)} pages.")
        for result in sorted(results, key=lambda r: (r.metadata.get('depth', 0), r.url)):
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")
        
        # Verify that no pages with depth > 2 are present
        assert all(r.metadata.get('depth', 0) <= 2 for r in results if r.success)

if __name__ == "__main__":
    asyncio.run(bfs_set_max_depth())
```

### 2.3. Example: `BFSDeePCrawlStrategy` - Setting `max_pages` to limit the total number of pages crawled (e.g., 10 pages).
Limit the crawl to a maximum number of pages, regardless of depth.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy
from unittest.mock import patch
import math # for math.inf

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def bfs_set_max_pages():
    strategy = BFSDeePCrawlStrategy(
        max_depth=math.inf, # Effectively no depth limit for this test
        max_pages=3         # Limit to 3 pages
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- BFS with max_pages=3 ---")
        print(f"Crawled {len(results)} pages (should be at most 3).")
        for result in results:
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")
        
        assert len(results) <= 3

if __name__ == "__main__":
    asyncio.run(bfs_set_max_pages())
```

### 2.4. Example: `BFSDeePCrawlStrategy` - Using `include_external=True` to follow links to external domains.
Allow the BFS crawler to follow links that lead to different domains than the start URL.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def bfs_include_external():
    strategy = BFSDeePCrawlStrategy(
        max_depth=1, 
        include_external=True
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- BFS with include_external=True (max_depth=1) ---")
        print(f"Crawled {len(results)} pages.")
        found_external = False
        for result in results:
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")
            if "external-site.com" in result.url:
                found_external = True
        
        assert found_external, "Expected to crawl an external link."

if __name__ == "__main__":
    asyncio.run(bfs_include_external())
```

### 2.5. Example: `BFSDeePCrawlStrategy` - Using `include_external=False` (default) to stay within the starting domain.
The default behavior is to only crawl links within the same domain as the start URL.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def bfs_exclude_external():
    strategy = BFSDeePCrawlStrategy(
        max_depth=1, 
        include_external=False # Default, but explicit for clarity
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- BFS with include_external=False (max_depth=1) ---")
        print(f"Crawled {len(results)} pages.")
        found_external = False
        for result in results:
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")
            if "external-site.com" in result.url:
                found_external = True
        
        assert not found_external, "Should not have crawled external links."

if __name__ == "__main__":
    asyncio.run(bfs_exclude_external())
```

### 2.6. Example: `BFSDeePCrawlStrategy` - Streaming results using `CrawlerRunConfig(stream=True)`.
Process results as they become available, useful for long crawls.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def bfs_streaming_results():
    strategy = BFSDeePCrawlStrategy(max_depth=1)
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        stream=True, # Enable streaming
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        print(f"--- BFS with Streaming Results (max_depth=1) ---")
        count = 0
        async for result in await crawler.arun(url=start_url, config=run_config):
            count += 1
            if result.success:
                print(f"  Streamed Result {count}: {result.url}, Depth: {result.metadata.get('depth')}")
            else:
                print(f"  Streamed FAILED Result {count}: {result.url}, Error: {result.error_message}")
        print(f"Total results streamed: {count}")

if __name__ == "__main__":
    asyncio.run(bfs_streaming_results())
```

### 2.7. Example: `BFSDeePCrawlStrategy` - Batch results using `CrawlerRunConfig(stream=False)` (default).
The default behavior is to return all results as a list after the crawl completes.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def bfs_batch_results():
    strategy = BFSDeePCrawlStrategy(max_depth=1)
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        stream=False, # Default, but explicit for clarity
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config) # Returns a list
        
        print(f"--- BFS with Batch Results (max_depth=1) ---")
        print(f"Received {len(results)} pages in a batch.")
        for result in results:
            if result.success:
                print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")

if __name__ == "__main__":
    asyncio.run(bfs_batch_results())
```

### 2.8. Example: `BFSDeePCrawlStrategy` - Integrating a `FilterChain` with `URLPatternFilter` to crawl specific paths.
Use filters to guide the crawler, for instance, to only explore URLs matching `/blog/*`.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, URLPatternFilter
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def bfs_with_url_pattern_filter():
    # Only crawl URLs containing '/blog/'
    url_filter = URLPatternFilter(patterns=["*/blog/*"])
    filter_chain = FilterChain(filters=[url_filter])
    
    strategy = BFSDeePCrawlStrategy(
        max_depth=1, 
        filter_chain=filter_chain
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- BFS with URLPatternFilter ('*/blog/*') ---")
        print(f"Crawled {len(results)} pages.")
        all_match_pattern = True
        for result in results:
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")
            # The start URL itself might not match, but discovered links should
            if result.metadata.get('depth', 0) > 0 and "/blog/" not in result.url:
                all_match_pattern = False
        
        # The start_url itself is always processed, then its links are filtered.
        # So, we check if all *discovered* pages match the pattern.
        discovered_pages = [r for r in results if r.metadata.get('depth',0) > 0]
        if discovered_pages: # only assert if any pages beyond start_url were processed
            assert all("/blog/" in r.url for r in discovered_pages), "Not all crawled pages matched the /blog/ pattern"
        print("Filter applied successfully (start URL is always processed, subsequent links are filtered).")


if __name__ == "__main__":
    asyncio.run(bfs_with_url_pattern_filter())
```

### 2.9. Example: `BFSDeePCrawlStrategy` - Demonstrating `shutdown()` to gracefully stop an ongoing crawl.
Showcase how to stop a crawl prematurely using the strategy's `shutdown()` method.

```python
import asyncio
import time
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def bfs_demonstrate_shutdown():
    strategy = BFSDeePCrawlStrategy(
        max_depth=5, # A potentially long crawl
        max_pages=100 
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        stream=True, # Streaming is good to see partial results before shutdown
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html" # A site with enough links
        
        print(f"--- BFS with shutdown() demonstration ---")
        
        crawl_task = asyncio.create_task(crawler.arun(url=start_url, config=run_config))
        
        # Let the crawl run for a very short time
        await asyncio.sleep(0.1) 
        
        print("Attempting to shut down the crawl...")
        await strategy.shutdown() 
        
        results_list = []
        try:
            # Await the results from the crawl task
            # If streaming, this will iterate through what was processed before shutdown
            async for res in await crawl_task:
                results_list.append(res)
                print(f"  Collected result (post-shutdown signal): {res.url}")
        except asyncio.CancelledError:
            print("Crawl task was cancelled.")
        
        print(f"Crawl shut down. Processed {len(results_list)} pages before/during shutdown.")
        # The number of pages will be less than if it ran to completion
        assert len(results_list) < 10, "Crawl likely didn't shut down early enough or mock site too small."

if __name__ == "__main__":
    asyncio.run(bfs_demonstrate_shutdown())
```

### 2.10. Example: `BFSDeePCrawlStrategy` - Crawling with no `max_depth` limit but a `max_pages` limit.
Demonstrate a scenario where depth is unlimited (or very high) but the crawl stops after a certain number of pages.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy
from unittest.mock import patch
import math

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def bfs_no_depth_limit_max_pages():
    strategy = BFSDeePCrawlStrategy(
        max_depth=math.inf, # Unlimited depth
        max_pages=4        # But only 4 pages
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- BFS with no depth limit, max_pages=4 ---")
        print(f"Crawled {len(results)} pages.")
        for result in results:
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")
        
        assert len(results) <= 4, "More pages crawled than max_pages limit."

if __name__ == "__main__":
    asyncio.run(bfs_no_depth_limit_max_pages())
```

---
## 3. Depth-First Search (`DFSDeePCrawlStrategy`) Examples

`DFSDeePCrawlStrategy` explores as far down one branch as possible before backtracking.

### 3.1. Example: Basic `DFSDeePCrawlStrategy` with default depth.
The default `max_depth` for `DFSDeePCrawlStrategy` is typically 10 if not specified.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DFSDeePCrawlStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def dfs_default_depth():
    # Default max_depth for DFS is typically higher (e.g., 10)
    strategy = DFSDeePCrawlStrategy() 
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        max_pages=5, # Limit pages to keep example short with default depth
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- DFS with Default Depth (max_pages=5 to limit output) ---")
        print(f"Crawled {len(results)} pages.")
        for result in results: # Order might be less predictable than BFS for small mock
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")

if __name__ == "__main__":
    asyncio.run(dfs_default_depth())
```

### 3.2. Example: `DFSDeePCrawlStrategy` - Setting `max_depth` to control how deep each branch goes.
Set `max_depth` to 2 for a DFS crawl.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DFSDeePCrawlStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def dfs_set_max_depth():
    strategy = DFSDeePCrawlStrategy(max_depth=2)
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- DFS with max_depth=2 ---")
        print(f"Crawled {len(results)} pages.")
        for result in results:
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")
        assert all(r.metadata.get('depth', 0) <= 2 for r in results if r.success)


if __name__ == "__main__":
    asyncio.run(dfs_set_max_depth())
```

### 3.3. Example: `DFSDeePCrawlStrategy` - Setting `max_pages` to limit the total number of pages.
Limit the total number of pages crawled by DFS to 3.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DFSDeePCrawlStrategy
from unittest.mock import patch
import math

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def dfs_set_max_pages():
    strategy = DFSDeePCrawlStrategy(
        max_depth=math.inf, # No depth limit for this test
        max_pages=3
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- DFS with max_pages=3 ---")
        print(f"Crawled {len(results)} pages (should be at most 3).")
        for result in results:
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")
        assert len(results) <= 3

if __name__ == "__main__":
    asyncio.run(dfs_set_max_pages())
```

### 3.4. Example: `DFSDeePCrawlStrategy` - Following external links with `include_external=True`.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DFSDeePCrawlStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def dfs_include_external():
    strategy = DFSDeePCrawlStrategy(
        max_depth=1, 
        include_external=True,
        max_pages=5 # Limit pages as external can be vast
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- DFS with include_external=True (max_depth=1, max_pages=5) ---")
        print(f"Crawled {len(results)} pages.")
        found_external = False
        for result in results:
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")
            if "external-site.com" in result.url:
                found_external = True
        
        assert found_external, "Expected to crawl an external link."

if __name__ == "__main__":
    asyncio.run(dfs_include_external())
```

### 3.5. Example: `DFSDeePCrawlStrategy` - Staying within the domain with `include_external=False`.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DFSDeePCrawlStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def dfs_exclude_external():
    strategy = DFSDeePCrawlStrategy(
        max_depth=1, 
        include_external=False # Default
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- DFS with include_external=False (max_depth=1) ---")
        print(f"Crawled {len(results)} pages.")
        found_external = False
        for result in results:
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")
            if "external-site.com" in result.url:
                found_external = True
        
        assert not found_external, "Should not have crawled external links."

if __name__ == "__main__":
    asyncio.run(dfs_exclude_external())
```

### 3.6. Example: `DFSDeePCrawlStrategy` - Streaming results.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DFSDeePCrawlStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def dfs_streaming_results():
    strategy = DFSDeePCrawlStrategy(max_depth=1)
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        stream=True,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        print(f"--- DFS with Streaming Results (max_depth=1) ---")
        count = 0
        async for result in await crawler.arun(url=start_url, config=run_config):
            count +=1
            if result.success:
                print(f"  Streamed Result {count}: {result.url}, Depth: {result.metadata.get('depth')}")
        print(f"Total results streamed: {count}")


if __name__ == "__main__":
    asyncio.run(dfs_streaming_results())
```

### 3.7. Example: `DFSDeePCrawlStrategy` - Batch results.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DFSDeePCrawlStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def dfs_batch_results():
    strategy = DFSDeePCrawlStrategy(max_depth=1)
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        stream=False, # Default
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- DFS with Batch Results (max_depth=1) ---")
        print(f"Received {len(results)} pages in a batch.")
        for result in results:
            if result.success:
                print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")

if __name__ == "__main__":
    asyncio.run(dfs_batch_results())
```

### 3.8. Example: `DFSDeePCrawlStrategy` - Integrating a `FilterChain` with `DomainFilter` to restrict to subdomains.
This example is conceptual for subdomains as MOCK_SITE_DATA doesn't have distinct subdomains. The filter setup is key.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DFSDeePCrawlStrategy, FilterChain, DomainFilter
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def dfs_with_domain_filter_subdomains():
    # Allow only the start domain and its subdomains
    # For this mock, 'docs.crawl4ai.com' will be the main domain.
    # If we had e.g., 'blog.docs.crawl4ai.com', this filter would allow it.
    domain_filter = DomainFilter(
        allowed_domains=["docs.crawl4ai.com"], 
        allow_subdomains=True
    )
    filter_chain = FilterChain(filters=[domain_filter])
    
    strategy = DFSDeePCrawlStrategy(
        max_depth=1, 
        filter_chain=filter_chain,
        include_external=True # Necessary to even consider other (sub)domains
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- DFS with DomainFilter (allow subdomains of docs.crawl4ai.com) ---")
        print(f"Crawled {len(results)} pages.")
        for result in results:
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")
            # In a real scenario, you'd assert that only allowed domains/subdomains are present.
            # Our mock data doesn't have true subdomains to test this effectively.
            assert "docs.crawl4ai.com" in result.url or "external-site.com" not in result.url

if __name__ == "__main__":
    asyncio.run(dfs_with_domain_filter_subdomains())
```

---
## 4. Best-First Crawling (`BestFirstCrawlingStrategy`) Examples

`BestFirstCrawlingStrategy` uses a priority queue, guided by scorers, to decide which URLs to crawl next.

### 4.1. Example: Basic `BestFirstCrawlingStrategy` with default parameters.
If no `url_scorer` is provided, it behaves somewhat like BFS but might have different internal queue management.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def best_first_default_params():
    strategy = BestFirstCrawlingStrategy(max_depth=1) # Default scorer (often scores 0)
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- BestFirstCrawlingStrategy with default parameters (max_depth=1) ---")
        print(f"Crawled {len(results)} pages.")
        for result in results:
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}, Score: {result.metadata.get('score', 0.0):.2f}")

if __name__ == "__main__":
    asyncio.run(best_first_default_params())
```

### 4.2. Example: `BestFirstCrawlingStrategy` - Setting `max_depth` to limit crawl depth.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def best_first_max_depth():
    strategy = BestFirstCrawlingStrategy(max_depth=2)
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- BestFirstCrawlingStrategy with max_depth=2 ---")
        print(f"Crawled {len(results)} pages.")
        for result in sorted(results, key=lambda r: (r.metadata.get('depth', 0), r.url)):
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}, Score: {result.metadata.get('score', 0.0):.2f}")
        assert all(r.metadata.get('depth', 0) <= 2 for r in results if r.success)

if __name__ == "__main__":
    asyncio.run(best_first_max_depth())
```

### 4.3. Example: `BestFirstCrawlingStrategy` - Setting `max_pages` to limit total pages crawled.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy
from unittest.mock import patch
import math

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def best_first_max_pages():
    strategy = BestFirstCrawlingStrategy(
        max_depth=math.inf, 
        max_pages=3
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- BestFirstCrawlingStrategy with max_pages=3 ---")
        print(f"Crawled {len(results)} pages.")
        for result in results:
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}, Score: {result.metadata.get('score', 0.0):.2f}")
        assert len(results) <= 3

if __name__ == "__main__":
    asyncio.run(best_first_max_pages())
```

### 4.4. Example: `BestFirstCrawlingStrategy` - Using `include_external=True`.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def best_first_include_external():
    strategy = BestFirstCrawlingStrategy(
        max_depth=1, 
        include_external=True,
        max_pages=5 # To keep it manageable
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- BestFirstCrawlingStrategy with include_external=True (max_depth=1) ---")
        print(f"Crawled {len(results)} pages.")
        found_external = False
        for result in results:
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}, Score: {result.metadata.get('score', 0.0):.2f}")
            if "external-site.com" in result.url:
                found_external = True
        
        assert found_external, "Expected to crawl an external link."

if __name__ == "__main__":
    asyncio.run(best_first_include_external())
```

### 4.5. Example: `BestFirstCrawlingStrategy` - Using `KeywordRelevanceScorer` to prioritize URLs containing specific keywords.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, KeywordRelevanceScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def best_first_keyword_scorer():
    scorer = KeywordRelevanceScorer(keywords=["feature", "advanced", "core"])
    strategy = BestFirstCrawlingStrategy(
        max_depth=1, 
        url_scorer=scorer,
        max_pages=4 # Limit for example clarity
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS,
        stream=True # Stream to see order
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        print(f"--- BestFirstCrawlingStrategy with KeywordRelevanceScorer ---")
        results_list = []
        async for result in await crawler.arun(url=start_url, config=run_config):
            results_list.append(result)
            if result.success:
                print(f"  URL: {result.url}, Score: {result.metadata.get('score', 0.0):.2f} (Depth: {result.metadata.get('depth')})")
        
        # Check if pages with keywords like "feature" or "core" were prioritized (appeared earlier/higher score)
        # This is a soft check as actual order depends on many factors in a real crawl
        # and the mock site's link structure.
        print("\nNote: Higher scores should ideally correspond to URLs with keywords 'feature', 'advanced', 'core'.")
        feature_page_crawled = any("page2.html" in r.url for r in results_list) # page2 has "feature"
        assert feature_page_crawled, "Page with 'feature' keyword was expected."


if __name__ == "__main__":
    asyncio.run(best_first_keyword_scorer())
```

### 4.6. Example: `BestFirstCrawlingStrategy` - Using `PathDepthScorer` to influence priority based on URL path depth.
This scorer penalizes deeper paths by default.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, PathDepthScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def best_first_path_depth_scorer():
    # Penalizes deeper paths (lower score for deeper paths)
    scorer = PathDepthScorer(higher_score_is_better=False) 
    strategy = BestFirstCrawlingStrategy(
        max_depth=2, # Allow some depth to see scorer effect
        url_scorer=scorer
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS,
        stream=True
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        print(f"--- BestFirstCrawlingStrategy with PathDepthScorer (favoring shallower paths) ---")
        
        results_list = []
        async for result in await crawler.arun(url=start_url, config=run_config):
            results_list.append(result)
            if result.success:
                 print(f"  URL: {result.url}, Score: {result.metadata.get('score', 0.0):.2f}, Depth: {result.metadata.get('depth')}")
        
        # A simple check: depth 1 pages should generally have higher (less negative) scores than depth 2
        # (if scores are negative due to penalty) or simply appear earlier if scores are positive.
        # With default scoring, higher score_is_better = True, so higher depth = lower score.
        # With higher_score_is_better=False, higher depth = higher (less negative) score.
        # The mock PathDepthScorer will need to be implemented or this test adjusted based on actual scorer logic.
        # For now, let's assume the scorer penalizes, so deeper paths have lower (more negative) scores.
        print("\nNote: Shallower pages should ideally have higher scores.")


if __name__ == "__main__":
    asyncio.run(best_first_path_depth_scorer())
```

### 4.7. Example: `BestFirstCrawlingStrategy` - Using `ContentTypeScorer` to prioritize HTML pages over PDFs.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, ContentTypeScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def best_first_content_type_scorer():
    # Prioritize HTML, penalize PDF
    scorer = ContentTypeScorer(content_type_weights={"text/html": 1.0, "application/pdf": -0.5})
    strategy = BestFirstCrawlingStrategy(
        max_depth=1, 
        url_scorer=scorer
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS,
        stream=True
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/page1.html" # This page links to HTML and PDF
        print(f"--- BestFirstCrawlingStrategy with ContentTypeScorer (HTML > PDF) ---")
        
        results_list = []
        async for result in await crawler.arun(url=start_url, config=run_config):
            results_list.append(result)
            if result.success:
                 print(f"  URL: {result.url}, Score: {result.metadata.get('score', 0.0):.2f}, Content-Type: {result.response_headers.get('Content-Type')}")

        html_page_score = next((r.metadata.get('score') for r in results_list if "page1_sub1.html" in r.url), None)
        pdf_page_score = next((r.metadata.get('score') for r in results_list if "page1_sub2.pdf" in r.url), None)

        print(f"HTML page score: {html_page_score}, PDF page score: {pdf_page_score}")
        if html_page_score is not None and pdf_page_score is not None:
            assert html_page_score > pdf_page_score, "HTML page should have a higher score than PDF."
        elif html_page_score is None or pdf_page_score is None:
            print("Warning: Could not find both HTML and PDF pages in results to compare scores.")


if __name__ == "__main__":
    asyncio.run(best_first_content_type_scorer())
```

### 4.8. Example: `BestFirstCrawlingStrategy` - Using `CompositeScorer` to combine `KeywordRelevanceScorer` and `PathDepthScorer`.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, KeywordRelevanceScorer, PathDepthScorer, CompositeScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def best_first_composite_scorer():
    keyword_scorer = KeywordRelevanceScorer(keywords=["feature", "core"], weight=0.7)
    path_scorer = PathDepthScorer(weight=0.3, higher_score_is_better=False) # Penalize depth slightly
    
    composite_scorer = CompositeScorer(scorers=[keyword_scorer, path_scorer])
    
    strategy = BestFirstCrawlingStrategy(
        max_depth=2, 
        url_scorer=composite_scorer,
        max_pages=6
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS,
        stream=True
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        print(f"--- BestFirstCrawlingStrategy with CompositeScorer ---")
        
        async for result in await crawler.arun(url=start_url, config=run_config):
            if result.success:
                print(f"  URL: {result.url}, Score: {result.metadata.get('score', 0.0):.2f}, Depth: {result.metadata.get('depth')}")
        print("\nNote: Scores are a combination of keyword relevance and path depth penalty.")

if __name__ == "__main__":
    asyncio.run(best_first_composite_scorer())
```

### 4.9. Example: `BestFirstCrawlingStrategy` - Integrating a `FilterChain` with `ContentTypeFilter` to only process HTML.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, FilterChain, ContentTypeFilter
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def best_first_with_content_type_filter():
    content_filter = ContentTypeFilter(allowed_types=["text/html"])
    filter_chain = FilterChain(filters=[content_filter])
    
    # Scorer is optional here, just demonstrating filter integration
    strategy = BestFirstCrawlingStrategy(
        max_depth=1, 
        filter_chain=filter_chain
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/page1.html" # This page links to HTML and PDF
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- BestFirstCrawlingStrategy with ContentTypeFilter (HTML only) ---")
        print(f"Crawled {len(results)} pages.")
        all_html = True
        for result in results:
            content_type = result.response_headers.get('Content-Type', '')
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}, Content-Type: {content_type}")
            if result.metadata.get('depth',0) > 0 and "text/html" not in content_type : # Start URL is not filtered
                 all_html = False
        
        discovered_pages = [r for r in results if r.metadata.get('depth',0) > 0]
        if discovered_pages:
            assert all("text/html" in r.response_headers.get('Content-Type','') for r in discovered_pages), "Non-HTML page found among discovered pages."
        print("Filter for HTML content type applied successfully to discovered pages.")

if __name__ == "__main__":
    asyncio.run(best_first_with_content_type_filter())
```

### 4.10. Example: `BestFirstCrawlingStrategy` - Streaming results and observing the order based on scores.
This example will use a scorer and stream results to demonstrate that higher-scored URLs are (generally) processed earlier.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, KeywordRelevanceScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def best_first_streaming_order():
    scorer = KeywordRelevanceScorer(keywords=["feature", "advanced"])
    strategy = BestFirstCrawlingStrategy(
        max_depth=1, 
        url_scorer=scorer,
        max_pages=5
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        stream=True,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        print(f"--- BestFirstCrawlingStrategy - Streaming and Observing Order ---")
        
        previous_score = float('inf') # Assuming scores are positive and higher is better
        processed_urls = []
        async for result in await crawler.arun(url=start_url, config=run_config):
            if result.success:
                current_score = result.metadata.get('score', 0.0)
                print(f"  Streamed: {result.url}, Score: {current_score:.2f}, Depth: {result.metadata.get('depth')}")
                # Note: Due to batching (BATCH_SIZE) and async nature, strict descending order isn't guaranteed
                # but generally higher scored items should appear earlier.
                # assert current_score <= previous_score + 1e-9, f"Scores not in generally descending order: {previous_score} then {current_score}"
                # previous_score = current_score
                processed_urls.append((result.url, current_score))

        print("\nProcessed URLs and their scores (order of processing):")
        for url, score in processed_urls:
            print(f"  {url} (Score: {score:.2f})")
        print("Note: Higher scored URLs are prioritized but strict order depends on batching and concurrency.")

if __name__ == "__main__":
    asyncio.run(best_first_streaming_order())
```

### 4.11. Example: `BestFirstCrawlingStrategy` - Batch results and analyzing scores post-crawl.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, KeywordRelevanceScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def best_first_batch_analysis():
    scorer = KeywordRelevanceScorer(keywords=["feature", "core"])
    strategy = BestFirstCrawlingStrategy(
        max_depth=1, 
        url_scorer=scorer,
        max_pages=5
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        stream=False, # Batch mode
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- BestFirstCrawlingStrategy - Batch Results Analysis ---")
        print(f"Received {len(results)} pages.")
        
        # Sort by score for analysis (higher score first)
        sorted_results = sorted(results, key=lambda r: r.metadata.get('score', 0.0), reverse=True)
        
        for result in sorted_results:
            if result.success:
                print(f"  URL: {result.url}, Score: {result.metadata.get('score', 0.0):.2f}, Depth: {result.metadata.get('depth')}")

if __name__ == "__main__":
    asyncio.run(best_first_batch_analysis())
```

### 4.12. Example: `BestFirstCrawlingStrategy` - Accessing and interpreting `score`, `depth`, and `parent_url` from `CrawlResult.metadata`.
This explicitly shows how to get these specific metadata fields.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, KeywordRelevanceScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def best_first_access_metadata():
    scorer = KeywordRelevanceScorer(keywords=["feature"])
    strategy = BestFirstCrawlingStrategy(max_depth=1, url_scorer=scorer)
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- BestFirstCrawlingStrategy - Accessing Metadata ---")
        for result in results:
            if result.success:
                url = result.url
                metadata = result.metadata
                depth = metadata.get('depth', 'N/A')
                parent_url = metadata.get('parent_url', 'N/A')
                score = metadata.get('score', 'N/A')
                
                print(f"URL: {url}")
                print(f"  Depth: {depth}")
                print(f"  Parent URL: {parent_url}")
                print(f"  Score: {score:.2f}" if isinstance(score, float) else f"  Score: {score}")
                print("-" * 10)

if __name__ == "__main__":
    asyncio.run(best_first_access_metadata())
```

### 4.13. Example: `BestFirstCrawlingStrategy` - Demonstrating `shutdown()` to stop an ongoing prioritized crawl.

```python
import asyncio
import time
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, KeywordRelevanceScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def best_first_demonstrate_shutdown():
    scorer = KeywordRelevanceScorer(keywords=["feature", "core", "example"])
    strategy = BestFirstCrawlingStrategy(
        max_depth=5, # A potentially long crawl
        max_pages=100,
        url_scorer=scorer
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        stream=True, 
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        
        print(f"--- BestFirstCrawlingStrategy with shutdown() demonstration ---")
        
        crawl_task = asyncio.create_task(crawler.arun(url=start_url, config=run_config))
        
        await asyncio.sleep(0.1) 
        
        print("Attempting to shut down the BestFirst crawl...")
        await strategy.shutdown() 
        
        results_list = []
        try:
            async for res in await crawl_task:
                results_list.append(res)
                print(f"  Collected result (post-shutdown signal): {res.url} (Score: {res.metadata.get('score', 0.0):.2f})")
        except asyncio.CancelledError:
            print("Crawl task was cancelled.")
        
        print(f"Crawl shut down. Processed {len(results_list)} pages before/during shutdown.")
        assert len(results_list) < 10, "Crawl likely didn't shut down early enough or mock site too small."

if __name__ == "__main__":
    asyncio.run(best_first_demonstrate_shutdown())
```

### 4.14. Example: `BestFirstCrawlingStrategy` - Explaining the effect of `BATCH_SIZE` on `arun_many`.
`BATCH_SIZE` is an internal constant in `bbf_strategy.py` (typically 10). This example explains its role rather than making it directly configurable by the user through the strategy's constructor, as it's an internal implementation detail of how the strategy uses `crawler.arun_many`.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, KeywordRelevanceScorer
from unittest.mock import patch

# Note: BATCH_SIZE is internal to BestFirstCrawlingStrategy, usually 10.
# We can't directly set it, but we can explain its effect.

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def best_first_batch_size_effect():
    print("--- Explaining BATCH_SIZE in BestFirstCrawlingStrategy ---")
    print("BestFirstCrawlingStrategy processes URLs in batches for efficiency.")
    print("Internally, it retrieves a batch of highest-priority URLs (typically up to BATCH_SIZE, e.g., 10) from its queue.")
    print("It then calls `crawler.arun_many()` with this batch.")
    print("This means that while URLs are prioritized, the order within a small batch might not be strictly descending by score,")
    print("especially if `stream=True`, as results from `arun_many` can arrive slightly out of strict submission order.")
    print("The overall crawl still heavily favors higher-scored URLs first over many batches.")

    # To simulate observing this, let's run a crawl and see if groups of results are processed.
    scorer = KeywordRelevanceScorer(keywords=["feature", "core", "page1", "page2"])
    strategy = BestFirstCrawlingStrategy(
        max_depth=2, 
        url_scorer=scorer,
        max_pages=6 # Small enough to potentially see batching effects if BATCH_SIZE was smaller
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        stream=True,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        
        print("\n--- Crawl Example (max_pages=6) ---")
        results_in_order = []
        async for result in await crawler.arun(url=start_url, config=run_config):
            if result.success:
                results_in_order.append(result.metadata.get('score',0.0))
                print(f"  Streamed: {result.url}, Score: {result.metadata.get('score', 0.0):.2f}")
        
        # This assertion is hard to make definitively without knowing the exact internal BATCH_SIZE
        # and perfect mock site behavior. The print statements are more illustrative.
        print("\nScores in order of processing:", [f"{s:.2f}" for s in results_in_order])
        print("Observe if there are small groups where order might not be strictly descending due to batch processing.")


if __name__ == "__main__":
    asyncio.run(best_first_batch_size_effect())
```

---
## 5. Configuring Filters (`FilterChain`) for Deep Crawling

Filters allow you to control which URLs are processed during a deep crawl. They are applied *before* a URL is added to the crawl queue (except for the start URL).

### 5.1. `URLPatternFilter`

#### 5.1.1. Example: Using `URLPatternFilter` to allow URLs matching specific patterns (e.g., `/blog/*`).

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, URLPatternFilter
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def filter_allow_pattern():
    # Allow only URLs containing '/blog/'
    url_filter = URLPatternFilter(patterns=["*/blog/*"])
    filter_chain = FilterChain(filters=[url_filter])
    
    strategy = BFSDeePCrawlStrategy(max_depth=1, filter_chain=filter_chain)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- URLPatternFilter: Allowing '*/blog/*' ---")
        print(f"Crawled {len(results)} pages.")
        for r in results:
            print(f"  URL: {r.url} (Depth: {r.metadata.get('depth')})")
            if r.metadata.get('depth', 0) > 0: # Check discovered URLs
                assert "/blog/" in r.url, f"Page {r.url} does not match pattern."
        print("All discovered pages match the allowed pattern.")

if __name__ == "__main__":
    asyncio.run(filter_allow_pattern())
```

#### 5.1.2. Example: Using `URLPatternFilter` to block URLs matching specific patterns (e.g., `*/login/*`, `*/archive/*`).

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, URLPatternFilter
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def filter_block_pattern():
    # Block URLs containing '/login/' or '/archive/'
    url_filter = URLPatternFilter(patterns=["*/login/*", "*/archive/*"], block_list=True)
    filter_chain = FilterChain(filters=[url_filter])
    
    strategy = BFSDeePCrawlStrategy(max_depth=1, filter_chain=filter_chain)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- URLPatternFilter: Blocking '*/login/*' and '*/archive/*' ---")
        print(f"Crawled {len(results)} pages.")
        for r in results:
            print(f"  URL: {r.url} (Depth: {r.metadata.get('depth')})")
            assert "/login/" not in r.url, f"Page {r.url} should have been blocked (login)."
            assert "/archive/" not in r.url, f"Page {r.url} should have been blocked (archive)."
        print("No pages matching blocked patterns were crawled.")

if __name__ == "__main__":
    asyncio.run(filter_block_pattern())
```

#### 5.1.3. Example: `URLPatternFilter` with `case_sensitive=True` vs. `case_sensitive=False`.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, URLPatternFilter
from unittest.mock import patch

# Add a case-specific URL to MOCK_SITE_DATA
MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/Page1.html"] = {
    "html_content": "<html><head><title>Page 1 Case Test</title></head><body><p>Content for case test.</p></body></html>",
    "response_headers": {"Content-Type": "text/html"}
}
MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/index.html"]["html_content"] += '<a href="Page1.html">Page 1 Case Test</a>'


@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def filter_pattern_case_sensitivity():
    start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"

    # Case-sensitive: should only match 'page1.html'
    print("\n--- URLPatternFilter: Case Sensitive (Allow '*/page1.html*') ---")
    url_filter_sensitive = URLPatternFilter(patterns=["*/page1.html*"], case_sensitive=True)
    filter_chain_sensitive = FilterChain(filters=[url_filter_sensitive])
    strategy_sensitive = BFSDeePCrawlStrategy(max_depth=1, filter_chain=filter_chain_sensitive)
    run_config_sensitive = CrawlerRunConfig(deep_crawl_strategy=strategy_sensitive, cache_mode=CacheMode.BYPASS)
    
    async with AsyncWebCrawler() as crawler:
        results_sensitive = await crawler.arun(url=start_url, config=run_config_sensitive)
        print(f"Crawled {len(results_sensitive)} pages.")
        for r in results_sensitive:
            print(f"  URL: {r.url}")
            if r.metadata.get('depth',0) > 0:
                assert "page1.html" in r.url and "Page1.html" not in r.url, "Case-sensitive filter failed."
    
    # Case-insensitive: should match both 'page1.html' and 'Page1.html'
    print("\n--- URLPatternFilter: Case Insensitive (Allow '*/page1.html*') ---")
    url_filter_insensitive = URLPatternFilter(patterns=["*/page1.html*"], case_sensitive=False)
    filter_chain_insensitive = FilterChain(filters=[url_filter_insensitive])
    strategy_insensitive = BFSDeePCrawlStrategy(max_depth=1, filter_chain=filter_chain_insensitive)
    run_config_insensitive = CrawlerRunConfig(deep_crawl_strategy=strategy_insensitive, cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler() as crawler:
        results_insensitive = await crawler.arun(url=start_url, config=run_config_insensitive)
        print(f"Crawled {len(results_insensitive)} pages.")
        found_page1_lower = False
        found_page1_upper = False
        for r in results_insensitive:
            print(f"  URL: {r.url}")
            if "page1.html" in r.url.lower(): # Check lower to catch both
                 if "page1.html" == Path(r.url).name: found_page1_lower = True
                 if "Page1.html" == Path(r.url).name: found_page1_upper = True
        
        assert found_page1_lower and found_page1_upper, "Case-insensitive filter should have matched both cases."

if __name__ == "__main__":
    asyncio.run(filter_pattern_case_sensitivity())
```

### 5.2. `DomainFilter`

#### 5.2.1. Example: Using `DomainFilter` with `allowed_domains` to restrict crawling to a list of specific domains.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, DomainFilter
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def filter_allowed_domains():
    # Only crawl within 'docs.crawl4ai.com'
    domain_filter = DomainFilter(allowed_domains=["docs.crawl4ai.com"])
    filter_chain = FilterChain(filters=[domain_filter])
    
    # include_external needs to be True for DomainFilter to even consider other domains for blocking/allowing
    strategy = BFSDeePCrawlStrategy(max_depth=1, filter_chain=filter_chain, include_external=True)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html" # This links to external-site.com
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- DomainFilter: Allowing only 'docs.crawl4ai.com' ---")
        print(f"Crawled {len(results)} pages.")
        for r in results:
            print(f"  URL: {r.url}")
            assert "docs.crawl4ai.com" in r.url, f"Page {r.url} is not from an allowed domain."
        print("All crawled pages are from 'docs.crawl4ai.com'.")

if __name__ == "__main__":
    asyncio.run(filter_allowed_domains())
```

#### 5.2.2. Example: Using `DomainFilter` with `blocked_domains` to avoid crawling certain domains.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, DomainFilter
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def filter_blocked_domains():
    # Block 'external-site.com'
    domain_filter = DomainFilter(blocked_domains=["external-site.com"])
    filter_chain = FilterChain(filters=[domain_filter])
    
    strategy = BFSDeePCrawlStrategy(max_depth=1, filter_chain=filter_chain, include_external=True)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- DomainFilter: Blocking 'external-site.com' ---")
        print(f"Crawled {len(results)} pages.")
        for r in results:
            print(f"  URL: {r.url}")
            assert "external-site.com" not in r.url, f"Page {r.url} from blocked domain was crawled."
        print("No pages from 'external-site.com' were crawled.")

if __name__ == "__main__":
    asyncio.run(filter_blocked_domains())
```

#### 5.2.3. Example: `DomainFilter` configured to allow subdomains (`allow_subdomains=True`).
(Conceptual as MOCK_SITE_DATA doesn't have subdomains for `docs.crawl4ai.com`.)

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, DomainFilter
from unittest.mock import patch

# Imagine MOCK_SITE_DATA also has:
# "https://blog.docs.crawl4ai.com/vibe-examples/post.html": { ... }
# And index.html links to it.

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def filter_allow_subdomains():
    domain_filter = DomainFilter(allowed_domains=["docs.crawl4ai.com"], allow_subdomains=True)
    filter_chain = FilterChain(filters=[domain_filter])
    
    strategy = BFSDeePCrawlStrategy(max_depth=1, filter_chain=filter_chain, include_external=True)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- DomainFilter: Allowing subdomains of 'docs.crawl4ai.com' (Conceptual) ---")
        print(f"Crawled {len(results)} pages.")
        for r in results:
            print(f"  URL: {r.url}")
            # In a real test, you'd check if blog.docs.crawl4ai.com was included
        print("This example is conceptual; for a real test, ensure mock data includes subdomains.")

if __name__ == "__main__":
    asyncio.run(filter_allow_subdomains())
```

#### 5.2.4. Example: `DomainFilter` configured to disallow subdomains (`allow_subdomains=False`).
(Conceptual as MOCK_SITE_DATA doesn't have subdomains for `docs.crawl4ai.com`.)

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, DomainFilter
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def filter_disallow_subdomains():
    domain_filter = DomainFilter(allowed_domains=["docs.crawl4ai.com"], allow_subdomains=False) # Default
    filter_chain = FilterChain(filters=[domain_filter])
    
    strategy = BFSDeePCrawlStrategy(max_depth=1, filter_chain=filter_chain, include_external=True)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- DomainFilter: Disallowing subdomains of 'docs.crawl4ai.com' (Conceptual) ---")
        print(f"Crawled {len(results)} pages.")
        for r in results:
            print(f"  URL: {r.url}")
            # In a real test, you'd check if blog.docs.crawl4ai.com was NOT included
        print("This example is conceptual; for a real test, ensure mock data includes subdomains to be excluded.")

if __name__ == "__main__":
    asyncio.run(filter_disallow_subdomains())
```

### 5.3. `ContentTypeFilter`

#### 5.3.1. Example: Using `ContentTypeFilter` to allow only `text/html` pages.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, ContentTypeFilter
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def filter_allow_html_only():
    content_filter = ContentTypeFilter(allowed_types=["text/html"])
    filter_chain = FilterChain(filters=[content_filter])
    
    strategy = BFSDeePCrawlStrategy(max_depth=1, filter_chain=filter_chain)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/page1.html" # Links to HTML and PDF
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- ContentTypeFilter: Allowing only 'text/html' ---")
        print(f"Crawled {len(results)} pages.")
        for r in results:
            content_type = r.response_headers.get('Content-Type', '')
            print(f"  URL: {r.url}, Content-Type: {content_type}")
            if r.metadata.get('depth', 0) > 0: # Check discovered URLs
                assert "text/html" in content_type, f"Page {r.url} has wrong content type: {content_type}"
        print("All discovered pages are 'text/html'.")

if __name__ == "__main__":
    asyncio.run(filter_allow_html_only())
```

#### 5.3.2. Example: Using `ContentTypeFilter` with multiple `allowed_types` (e.g., `text/html`, `application/json`).
(Conceptual, as MOCK_SITE_DATA only has html/pdf)

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, ContentTypeFilter
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def filter_allow_multiple_types():
    content_filter = ContentTypeFilter(allowed_types=["text/html", "application/json"])
    filter_chain = FilterChain(filters=[content_filter])
    
    strategy = BFSDeePCrawlStrategy(max_depth=1, filter_chain=filter_chain)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/page1.html" 
        # Imagine page1.html also links to a page1_sub3.json
        MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/page1_sub3.json"] = {
            "html_content": '{"key": "value"}',
            "response_headers": {"Content-Type": "application/json"}
        }
        MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/page1.html"]["html_content"] += '<a href="page1_sub3.json">JSON Data</a>'


        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- ContentTypeFilter: Allowing 'text/html', 'application/json' ---")
        print(f"Crawled {len(results)} pages.")
        found_json = False
        for r in results:
            content_type = r.response_headers.get('Content-Type', '')
            print(f"  URL: {r.url}, Content-Type: {content_type}")
            if r.metadata.get('depth',0) > 0:
                assert "text/html" in content_type or "application/json" in content_type
            if "application/json" in content_type:
                found_json = True
        assert found_json, "Expected to find a JSON page."
        print("All discovered pages are either 'text/html' or 'application/json'.")
        
        # Clean up mock data
        del MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/page1_sub3.json"]
        MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/page1.html"]["html_content"] = MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/page1.html"]["html_content"].replace('<a href="page1_sub3.json">JSON Data</a>', '')


if __name__ == "__main__":
    asyncio.run(filter_allow_multiple_types())
```

#### 5.3.3. Example: Using `ContentTypeFilter` with `blocked_types` (e.g., blocking `application/pdf`).

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, ContentTypeFilter
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def filter_block_pdf():
    content_filter = ContentTypeFilter(blocked_types=["application/pdf"])
    filter_chain = FilterChain(filters=[content_filter])
    
    strategy = BFSDeePCrawlStrategy(max_depth=1, filter_chain=filter_chain)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/page1.html" # Links to HTML and PDF
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- ContentTypeFilter: Blocking 'application/pdf' ---")
        print(f"Crawled {len(results)} pages.")
        for r in results:
            content_type = r.response_headers.get('Content-Type', '')
            print(f"  URL: {r.url}, Content-Type: {content_type}")
            assert "application/pdf" not in content_type, f"PDF page {r.url} was not blocked."
        print("No 'application/pdf' pages were crawled (beyond start URL if it was PDF).")

if __name__ == "__main__":
    asyncio.run(filter_block_pdf())
```

### 5.4. `URLFilter` (Simple exact match)

#### 5.4.1. Example: `URLFilter` to allow a specific list of exact URLs.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, URLFilter
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def filter_allow_exact_urls():
    allowed_urls = [
        "https://docs.crawl4ai.com/vibe-examples/page1.html",
        "https://docs.crawl4ai.com/vibe-examples/page1_sub1.html"
    ]
    url_filter = URLFilter(urls=allowed_urls, block_list=False) # Allow list
    filter_chain = FilterChain(filters=[url_filter])
    
    strategy = BFSDeePCrawlStrategy(max_depth=2, filter_chain=filter_chain)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- URLFilter: Allowing specific URLs ---")
        print(f"Crawled {len(results)} pages.")
        crawled_urls = {r.url for r in results}
        # The start URL is always crawled initially, then its links are filtered.
        # So we check that all *other* crawled URLs are in the allowed list.
        for r_url in crawled_urls:
            if r_url != start_url: # Exclude start_url from this assertion
                 assert r_url in allowed_urls, f"URL {r_url} was not in the allowed list."
        print("Only URLs from the allowed list (plus start_url) were crawled.")

if __name__ == "__main__":
    asyncio.run(filter_allow_exact_urls())
```

#### 5.4.2. Example: `URLFilter` to block a specific list of exact URLs.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, URLFilter
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def filter_block_exact_urls():
    blocked_urls = [
        "https://docs.crawl4ai.com/vibe-examples/page2.html",
        "https://docs.crawl4ai.com/vibe-examples/archive/old_page.html"
    ]
    url_filter = URLFilter(urls=blocked_urls, block_list=True) # Block list
    filter_chain = FilterChain(filters=[url_filter])
    
    strategy = BFSDeePCrawlStrategy(max_depth=1, filter_chain=filter_chain)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- URLFilter: Blocking specific URLs ---")
        print(f"Crawled {len(results)} pages.")
        crawled_urls = {r.url for r in results}
        for blocked_url in blocked_urls:
            assert blocked_url not in crawled_urls, f"URL {blocked_url} should have been blocked."
        print("Blocked URLs were not crawled.")

if __name__ == "__main__":
    asyncio.run(filter_block_exact_urls())
```

### 5.5. `ContentRelevanceFilter`
This filter uses an LLM to determine relevance. The example focuses on setup, as a full run requires an LLM.

#### 5.5.1. Example: Setting up `ContentRelevanceFilter` with target keywords (conceptual, focusing on setup).

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, ContentRelevanceFilter, LLMConfig

# This is a conceptual example showing setup.
# A real run would require an LLM provider to be configured.
async def setup_content_relevance_filter():
    print("--- Setting up ContentRelevanceFilter (Conceptual) ---")
    
    # Define keywords and context for relevance
    keywords = ["artificial intelligence", "web crawling", "data extraction"]
    context_query = "Articles related to AI-powered web scraping tools and techniques."

    # Configure LLM (replace with your actual provider and API key)
    llm_config = LLMConfig(provider="openai/gpt-3.5-turbo", api_token="YOUR_OPENAI_API_KEY")
    
    relevance_filter = ContentRelevanceFilter(
        llm_config=llm_config,
        keywords=keywords,
        context_query=context_query,
        threshold=0.6 # Adjust threshold as needed
    )
    filter_chain = FilterChain(filters=[relevance_filter])
    
    strategy = BFSDeePCrawlStrategy(max_depth=1, filter_chain=filter_chain)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    print("ContentRelevanceFilter configured. To run this example:")
    print("1. Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key.")
    print("2. (Optional) Install OpenAI client: pip install openai")
    print("3. Uncomment the crawler execution part below.")

    # # Example of how it would be used (requires actual LLM call)
    # async with AsyncWebCrawler() as crawler:
    #     # Mock or use a real URL that would trigger the LLM
    #     start_url = "https://docs.crawl4ai.com/vibe-examples/page1.html" 
    #     print(f"Attempting to crawl {start_url} with ContentRelevanceFilter...")
    #     # results = await crawler.arun(url=start_url, config=run_config)
    #     # print(f"Crawled {len(results)} pages after relevance filtering.")
    #     # for r in results:
    #     #     print(f"  URL: {r.url}, Relevance Score: {r.metadata.get('relevance_score')}")
    print("Conceptual setup complete.")

if __name__ == "__main__":
    asyncio.run(setup_content_relevance_filter())
```

#### 5.5.2. Example: `ContentRelevanceFilter` with a custom `threshold`.

```python
import asyncio
from crawl4ai import ContentRelevanceFilter, LLMConfig

async def content_relevance_custom_threshold():
    print("--- ContentRelevanceFilter with custom threshold (Conceptual Setup) ---")
    llm_config = LLMConfig(provider="openai/gpt-3.5-turbo", api_token="YOUR_OPENAI_API_KEY") # Replace
    
    # A higher threshold means stricter relevance checking
    strict_filter = ContentRelevanceFilter(
        llm_config=llm_config,
        keywords=["specific technical term"],
        threshold=0.8 
    )
    print(f"Strict filter created with threshold: {strict_filter.threshold}")

    # A lower threshold is more lenient
    lenient_filter = ContentRelevanceFilter(
        llm_config=llm_config,
        keywords=["general topic"],
        threshold=0.4
    )
    print(f"Lenient filter created with threshold: {lenient_filter.threshold}")
    print("Note: Actual filtering behavior depends on LLM responses to content.")

if __name__ == "__main__":
    asyncio.run(content_relevance_custom_threshold())
```

### 5.6. `SEOFilter`
This filter checks for common SEO issues. The example is conceptual, focusing on setup.

#### 5.6.1. Example: Basic `SEOFilter` with default SEO checks (conceptual, focusing on setup).

```python
import asyncio
from crawl4ai import SEOFilter

async def setup_basic_seo_filter():
    print("--- Basic SEOFilter with default checks (Conceptual Setup) ---")
    
    # Default checks might include missing title, short meta description, etc.
    seo_filter = SEOFilter() 
    
    print(f"SEOFilter created with default settings:")
    print(f"  Min Title Length: {seo_filter.min_title_length}")
    print(f"  Max Title Length: {seo_filter.max_title_length}")
    print(f"  Min Meta Description Length: {seo_filter.min_meta_description_length}")
    # ... and other default parameters
    print("This filter would be added to a FilterChain and used in a DeepCrawlStrategy.")
    print("It would then check each page against these SEO criteria.")

if __name__ == "__main__":
    asyncio.run(setup_basic_seo_filter())
```

#### 5.6.2. Example: `SEOFilter` configuring specific checks like `min_title_length`, `max_meta_description_length`, or `keyword_in_title_check` (conceptual).

```python
import asyncio
from crawl4ai import SEOFilter

async def setup_custom_seo_filter():
    print("--- SEOFilter with custom checks (Conceptual Setup) ---")
    
    custom_seo_filter = SEOFilter(
        min_title_length=20,
        max_meta_description_length=150,
        keyword_in_title_check=True,
        target_keywords_for_seo=["crawl4ai", "web scraping"] # if keyword_in_title_check is True
    )
    
    print(f"Custom SEOFilter created with:")
    print(f"  Min Title Length: {custom_seo_filter.min_title_length}")
    print(f"  Max Meta Description Length: {custom_seo_filter.max_meta_description_length}")
    print(f"  Keyword in Title Check: {custom_seo_filter.keyword_in_title_check}")
    print(f"  Target SEO Keywords: {custom_seo_filter.target_keywords_for_seo}")
    print("This filter would apply these specific criteria during a crawl.")

if __name__ == "__main__":
    asyncio.run(setup_custom_seo_filter())
```

### 5.7. `FilterChain`

#### 5.7.1. Example: Combining `URLPatternFilter` (allow `/products/*`) and `DomainFilter` (only `example.com`) in a `FilterChain`.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, URLPatternFilter, DomainFilter
from unittest.mock import patch

# Add mock data for this scenario
MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/products/productA.html"] = {
    "html_content": "<html><title>Product A</title><body>Product A details</body></html>",
    "response_headers": {"Content-Type": "text/html"}
}
MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/index.html"]["html_content"] += '<a href="products/productA.html">Product A</a>'


@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def filter_chain_combination():
    product_filter = URLPatternFilter(patterns=["*/products/*"])
    domain_filter = DomainFilter(allowed_domains=["docs.crawl4ai.com"])
    
    combined_filter_chain = FilterChain(filters=[product_filter, domain_filter])
    
    strategy = BFSDeePCrawlStrategy(max_depth=2, filter_chain=combined_filter_chain, include_external=True)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- FilterChain: URLPatternFilter + DomainFilter ---")
        print(f"Crawled {len(results)} pages.")
        for r in results:
            print(f"  URL: {r.url}")
            if r.metadata.get('depth', 0) > 0: # Discovered URLs
                assert "docs.crawl4ai.com" in r.url, "Domain filter failed."
                assert "/products/" in r.url, "URL pattern filter failed."
        print("All discovered pages are from 'docs.crawl4ai.com' and match '*/products/*'.")
        
        # Clean up mock data
        del MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/products/productA.html"]
        MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/index.html"]["html_content"] = MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/index.html"]["html_content"].replace('<a href="products/productA.html">Product A</a>', '')


if __name__ == "__main__":
    asyncio.run(filter_chain_combination())
```

#### 5.7.2. Example: Using `FilterChain` with `FilterStats` to retrieve and display statistics about filtered URLs.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, URLPatternFilter, FilterStats
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def filter_chain_with_stats():
    url_filter = URLPatternFilter(patterns=["*/blog/*"], block_list=False) # Allow only blog
    filter_stats = FilterStats() # Create a stats object
    filter_chain = FilterChain(filters=[url_filter], stats=filter_stats) # Pass stats to chain
    
    strategy = BFSDeePCrawlStrategy(max_depth=1, filter_chain=filter_chain)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- FilterChain with FilterStats ---")
        print(f"Crawled {len(results)} pages.")
        
        print("\nFilter Statistics:")
        print(f"  Total URLs considered by filters: {filter_stats.total_considered}")
        print(f"  Total URLs allowed: {filter_stats.total_allowed}")
        print(f"  Total URLs blocked: {filter_stats.total_blocked}")
        
        # Based on MOCK_SITE_DATA, index links to one /blog/ page and several non-blog pages.
        # Start URL itself is not subject to filter_chain in this strategy logic.
        # Links from start URL: page1, page2, external, archive, blog, login
        # Only /blog/post1.html should pass. 5 should be blocked.
        assert filter_stats.total_considered >= 5 # Links from index.html
        assert filter_stats.total_allowed >= 1    # /blog/post1.html
        assert filter_stats.total_blocked >= 4    # page1, page2, external (if not implicitly blocked), archive, login

if __name__ == "__main__":
    asyncio.run(filter_chain_with_stats())
```

#### 5.7.3. Example: `FilterChain` with `allow_empty=True` vs `allow_empty=False`.
This shows how `allow_empty` on the `FilterChain` itself works. If `allow_empty=True` (default), an empty chain allows all URLs. If `False`, an empty chain blocks all.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def filter_chain_allow_empty():
    start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
    
    # Case 1: allow_empty=True (default) - empty chain allows all
    print("\n--- FilterChain with allow_empty=True (empty chain) ---")
    empty_chain_allow = FilterChain(filters=[], allow_empty=True)
    strategy_allow = BFSDeePCrawlStrategy(max_depth=1, filter_chain=empty_chain_allow)
    run_config_allow = CrawlerRunConfig(deep_crawl_strategy=strategy_allow, cache_mode=CacheMode.BYPASS)
    async with AsyncWebCrawler() as crawler:
        results_allow = await crawler.arun(url=start_url, config=run_config_allow)
        print(f"Crawled {len(results_allow)} pages. (Expected > 1 as all links from index should be allowed)")
        assert len(results_allow) > 1 # Start URL + its links

    # Case 2: allow_empty=False - empty chain blocks all (except start URL)
    print("\n--- FilterChain with allow_empty=False (empty chain) ---")
    empty_chain_block = FilterChain(filters=[], allow_empty=False)
    strategy_block = BFSDeePCrawlStrategy(max_depth=1, filter_chain=empty_chain_block)
    run_config_block = CrawlerRunConfig(deep_crawl_strategy=strategy_block, cache_mode=CacheMode.BYPASS)
    async with AsyncWebCrawler() as crawler:
        results_block = await crawler.arun(url=start_url, config=run_config_block)
        print(f"Crawled {len(results_block)} pages. (Expected 1, only start URL)")
        assert len(results_block) == 1 # Only start_url, as all its links are blocked by empty chain


if __name__ == "__main__":
    asyncio.run(filter_chain_allow_empty())
```

---
## 6. Configuring Scorers (`URLScorer`) for `BestFirstCrawlingStrategy`

Scorers are used by `BestFirstCrawlingStrategy` to prioritize URLs in its crawl queue.

### 6.1. `KeywordRelevanceScorer`

#### 6.1.1. Example: `KeywordRelevanceScorer` with a list of keywords and default weight.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, KeywordRelevanceScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def scorer_keyword_default_weight():
    scorer = KeywordRelevanceScorer(keywords=["feature", "core concepts"]) # Default weight is 1.0
    strategy = BestFirstCrawlingStrategy(max_depth=1, url_scorer=scorer, max_pages=4)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS, stream=True)

    print("--- KeywordRelevanceScorer with default weight ---")
    async with AsyncWebCrawler() as crawler:
        async for result in await crawler.arun("https://docs.crawl4ai.com/vibe-examples/index.html", config=run_config):
            if result.success:
                print(f"  URL: {result.url}, Score: {result.metadata.get('score', 0.0):.2f}")
    print("Pages containing 'feature' or 'core concepts' in their URL should have higher scores.")

if __name__ == "__main__":
    asyncio.run(scorer_keyword_default_weight())
```

#### 6.1.2. Example: `KeywordRelevanceScorer` adjusting the `weight` parameter to influence its importance.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, KeywordRelevanceScorer, PathDepthScorer, CompositeScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def scorer_keyword_custom_weight():
    # High weight for keywords, low for path depth
    keyword_scorer = KeywordRelevanceScorer(keywords=["feature"], weight=2.0) 
    path_scorer = PathDepthScorer(weight=0.1, higher_score_is_better=False) # Less penalty
    
    composite_scorer = CompositeScorer(scorers=[keyword_scorer, path_scorer])
    strategy = BestFirstCrawlingStrategy(max_depth=1, url_scorer=composite_scorer, max_pages=4)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS, stream=True)

    print("--- KeywordRelevanceScorer with adjusted weight (weight=2.0) in CompositeScorer ---")
    async with AsyncWebCrawler() as crawler:
        async for result in await crawler.arun("https://docs.crawl4ai.com/vibe-examples/index.html", config=run_config):
            if result.success:
                print(f"  URL: {result.url}, Score: {result.metadata.get('score', 0.0):.2f}")
    print("Keyword relevance should have a stronger impact on the final score.")

if __name__ == "__main__":
    asyncio.run(scorer_keyword_custom_weight())
```

#### 6.1.3. Example: `KeywordRelevanceScorer` with `case_sensitive=True`.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, KeywordRelevanceScorer
from unittest.mock import patch

# Modify mock data to have case-specific keywords in URLs
MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/FEATUREpage.html"] = {
    "html_content": "<html><title>FEATURE Page</title><body>Uppercase FEATURE</body></html>",
    "response_headers": {"Content-Type": "text/html"}
}
MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/index.html"]["html_content"] += '<a href="FEATUREpage.html">FEATURE Page</a>'


@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def scorer_keyword_case_sensitive():
    # Case-sensitive: will only score URLs with 'feature' (lowercase)
    scorer_sensitive = KeywordRelevanceScorer(keywords=["feature"], case_sensitive=True)
    strategy_sensitive = BestFirstCrawlingStrategy(max_depth=1, url_scorer=scorer_sensitive, max_pages=5)
    run_config_sensitive = CrawlerRunConfig(deep_crawl_strategy=strategy_sensitive, cache_mode=CacheMode.BYPASS, stream=True)

    print("--- KeywordRelevanceScorer with case_sensitive=True (keyword: 'feature') ---")
    async with AsyncWebCrawler() as crawler:
        async for result in await crawler.arun("https://docs.crawl4ai.com/vibe-examples/index.html", config=run_config_sensitive):
            if result.success:
                print(f"  URL: {result.url}, Score: {result.metadata.get('score', 0.0):.2f}")
                if "FEATUREpage.html" in result.url: # Uppercase 'FEATURE'
                    assert result.metadata.get('score', 0.0) == 0.0, "Uppercase keyword should not be scored."
                elif "page2.html" in result.url: # Contains lowercase 'feature' in title/mock
                     assert result.metadata.get('score', 0.0) > 0.0, "Lowercase keyword should be scored."

    # Clean up mock data
    del MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/FEATUREpage.html"]
    MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/index.html"]["html_content"] = MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/index.html"]["html_content"].replace('<a href="FEATUREpage.html">FEATURE Page</a>', '')


if __name__ == "__main__":
    asyncio.run(scorer_keyword_case_sensitive())
```

### 6.2. `PathDepthScorer`

#### 6.2.1. Example: `PathDepthScorer` with default behavior (penalizing deeper paths).
By default, `PathDepthScorer` gives higher scores to shallower paths (depth 0 > depth 1 > depth 2).

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, PathDepthScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def scorer_path_depth_default():
    scorer = PathDepthScorer() # Default: higher_score_is_better=True, depth_penalty_factor=0.1
    strategy = BestFirstCrawlingStrategy(max_depth=2, url_scorer=scorer, max_pages=6)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS, stream=True)

    print("--- PathDepthScorer with default behavior (shallower is better) ---")
    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        
        depth_scores = {}
        async for result in await crawler.arun(url=start_url, config=run_config):
            if result.success:
                depth = result.metadata.get('depth')
                score = result.metadata.get('score', 0.0)
                print(f"  URL: {result.url}, Depth: {depth}, Score: {score:.2f}")
                if depth not in depth_scores:
                    depth_scores[depth] = []
                depth_scores[depth].append(score)
        
        if 1 in depth_scores and 2 in depth_scores and depth_scores[1] and depth_scores[2]:
           avg_score_depth1 = sum(depth_scores[1]) / len(depth_scores[1])
           avg_score_depth2 = sum(depth_scores[2]) / len(depth_scores[2])
           print(f"Avg score depth 1: {avg_score_depth1:.2f}, Avg score depth 2: {avg_score_depth2:.2f}")
           assert avg_score_depth1 > avg_score_depth2, "Shallower paths should have higher scores."

if __name__ == "__main__":
    asyncio.run(scorer_path_depth_default())
```

#### 6.2.2. Example: `PathDepthScorer` with custom `depth_penalty_factor`.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, PathDepthScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def scorer_path_depth_custom_penalty():
    # Higher penalty factor means deeper paths are penalized more severely
    scorer = PathDepthScorer(depth_penalty_factor=0.5, higher_score_is_better=True) 
    strategy = BestFirstCrawlingStrategy(max_depth=2, url_scorer=scorer, max_pages=6)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS, stream=True)

    print("--- PathDepthScorer with custom depth_penalty_factor=0.5 ---")
    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        
        depth_scores = {}
        async for result in await crawler.arun(url=start_url, config=run_config):
            if result.success:
                depth = result.metadata.get('depth')
                score = result.metadata.get('score', 0.0)
                print(f"  URL: {result.url}, Depth: {depth}, Score: {score:.2f}")
                if depth not in depth_scores:
                    depth_scores[depth] = []
                depth_scores[depth].append(score)

        if 1 in depth_scores and 2 in depth_scores and depth_scores[1] and depth_scores[2]:
           avg_score_depth1 = sum(depth_scores[1]) / len(depth_scores[1])
           avg_score_depth2 = sum(depth_scores[2]) / len(depth_scores[2])
           print(f"Avg score depth 1: {avg_score_depth1:.2f}, Avg score depth 2: {avg_score_depth2:.2f}")
           # Expect a larger difference due to higher penalty
           assert (avg_score_depth1 - avg_score_depth2) > 0.05, "Higher penalty factor should result in a larger score drop for deeper paths."


if __name__ == "__main__":
    asyncio.run(scorer_path_depth_custom_penalty())
```

#### 6.2.3. Example: `PathDepthScorer` with `higher_score_is_better=False` (to favor deeper paths).

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, PathDepthScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def scorer_path_depth_favor_deep():
    # Now, deeper paths will get higher (less negative or more positive) scores
    scorer = PathDepthScorer(higher_score_is_better=False) 
    strategy = BestFirstCrawlingStrategy(max_depth=2, url_scorer=scorer, max_pages=6)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS, stream=True)

    print("--- PathDepthScorer with higher_score_is_better=False (favoring deeper paths) ---")
    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        
        depth_scores = {}
        async for result in await crawler.arun(url=start_url, config=run_config):
            if result.success:
                depth = result.metadata.get('depth')
                score = result.metadata.get('score', 0.0)
                print(f"  URL: {result.url}, Depth: {depth}, Score: {score:.2f}")
                if depth not in depth_scores:
                    depth_scores[depth] = []
                depth_scores[depth].append(score)
        
        if 1 in depth_scores and 2 in depth_scores and depth_scores[1] and depth_scores[2]:
           avg_score_depth1 = sum(depth_scores[1]) / len(depth_scores[1])
           avg_score_depth2 = sum(depth_scores[2]) / len(depth_scores[2])
           print(f"Avg score depth 1: {avg_score_depth1:.2f}, Avg score depth 2: {avg_score_depth2:.2f}")
           assert avg_score_depth2 > avg_score_depth1, "Deeper paths should have higher scores with higher_score_is_better=False."

if __name__ == "__main__":
    asyncio.run(scorer_path_depth_favor_deep())
```

### 6.3. `ContentTypeScorer`

#### 6.3.1. Example: `ContentTypeScorer` prioritizing `text/html` and penalizing `application/pdf`.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, ContentTypeScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def scorer_content_type_html_vs_pdf():
    scorer = ContentTypeScorer(
        content_type_weights={"text/html": 1.0, "application/pdf": -1.0, "image/jpeg": 0.2}
    )
    strategy = BestFirstCrawlingStrategy(max_depth=1, url_scorer=scorer, max_pages=5)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS, stream=True)

    print("--- ContentTypeScorer (HTML: 1.0, PDF: -1.0) ---")
    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/page1.html" # Links to HTML and PDF
        async for result in await crawler.arun(url=start_url, config=run_config):
            if result.success:
                content_type = result.response_headers.get('Content-Type', 'unknown')
                print(f"  URL: {result.url}, Score: {result.metadata.get('score', 0.0):.2f}, Type: {content_type}")

if __name__ == "__main__":
    asyncio.run(scorer_content_type_html_vs_pdf())
```

#### 6.3.2. Example: `ContentTypeScorer` with custom `content_type_weights`.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, ContentTypeScorer
from unittest.mock import patch

# Add a JSON page to mock data
MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/data.json"] = {
    "html_content": '{"data": "sample"}', "response_headers": {"Content-Type": "application/json"}
}
MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/index.html"]["html_content"] += '<a href="data.json">JSON Data</a>'


@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def scorer_content_type_custom_weights():
    scorer = ContentTypeScorer(
        content_type_weights={
            "application/json": 2.0, # Highly prioritize JSON
            "text/html": 0.5,
            "application/pdf": -2.0 # Strongly penalize PDF
        }
    )
    strategy = BestFirstCrawlingStrategy(max_depth=1, url_scorer=scorer, max_pages=5)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS, stream=True)

    print("--- ContentTypeScorer with custom weights (JSON: 2.0, HTML: 0.5, PDF: -2.0) ---")
    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/page1.html" # Links to HTML, PDF. Index links to JSON.
        
        # We'll crawl index to ensure JSON is discoverable
        async for result in await crawler.arun("https://docs.crawl4ai.com/vibe-examples/index.html", config=run_config):
            if result.success:
                content_type = result.response_headers.get('Content-Type', 'unknown')
                print(f"  URL: {result.url}, Score: {result.metadata.get('score', 0.0):.2f}, Type: {content_type}")
    
    del MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/data.json"]
    MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/index.html"]["html_content"] = MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/index.html"]["html_content"].replace('<a href="data.json">JSON Data</a>', '')

if __name__ == "__main__":
    asyncio.run(scorer_content_type_custom_weights())
```

### 6.4. `DomainAuthorityScorer`

#### 6.4.1. Example: Setting up `DomainAuthorityScorer` (conceptual, as DA often requires an external API or dataset).
This example shows how to instantiate and potentially use it, but actual scoring depends on external data.

```python
import asyncio
from crawl4ai import DomainAuthorityScorer

async def setup_domain_authority_scorer():
    print("--- DomainAuthorityScorer (Conceptual Setup) ---")
    
    # Conceptual: imagine you have a way to get DA scores
    # da_scores = {"example.com": 90, "anotherexample.net": 70}
    # scorer = DomainAuthorityScorer(domain_authority_map=da_scores, weight=1.5)
    
    # For this example, we'll just instantiate it
    scorer = DomainAuthorityScorer(weight=1.5)
    print(f"DomainAuthorityScorer created with weight: {scorer.weight}")
    print("To use this scorer effectively, you'd need a 'domain_authority_map' or a way to fetch DA scores.")
    print("Example URL score (conceptual): ", scorer.score("https://highly-authoritative-site.com/page"))

if __name__ == "__main__":
    asyncio.run(setup_domain_authority_scorer())
```

### 6.5. `FreshnessScorer`

#### 6.5.1. Example: Setting up `FreshnessScorer` (conceptual, as freshness often requires parsing dates from content or headers).
This example focuses on instantiation. Actual scoring would need date extraction.

```python
import asyncio
from crawl4ai import FreshnessScorer
from datetime import datetime, timedelta

async def setup_freshness_scorer():
    print("--- FreshnessScorer (Conceptual Setup) ---")
    
    # Conceptual: the scorer would need a way to get the publication date of a URL
    # For this example, we'll just instantiate it
    scorer = FreshnessScorer(
        max_age_days=30,      # Pages older than 30 days get lower scores
        date_penalty_factor=0.1 # How much to penalize per day older
    )
    print(f"FreshnessScorer created with max_age_days: {scorer.max_age_days}")
    print("To use this, the crawling process or a pre-processor would need to extract and provide publication dates for URLs.")
    
    # Conceptual scoring:
    # recent_date = datetime.now() - timedelta(days=5)
    # old_date = datetime.now() - timedelta(days=60)
    # print(f"Score for recent page (mock date): {scorer.score('https://example.com/recent', publication_date=recent_date)}")
    # print(f"Score for old page (mock date): {scorer.score('https://example.com/old', publication_date=old_date)}")


if __name__ == "__main__":
    asyncio.run(setup_freshness_scorer())
```

### 6.6. `CompositeScorer`

#### 6.6.1. Example: Combining `KeywordRelevanceScorer` and `PathDepthScorer` using `CompositeScorer` with equal weights.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy
from crawl4ai import KeywordRelevanceScorer, PathDepthScorer, CompositeScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def composite_scorer_equal_weights():
    keyword_scorer = KeywordRelevanceScorer(keywords=["feature"]) # Default weight 1.0
    path_scorer = PathDepthScorer(higher_score_is_better=False)  # Default weight 1.0, penalizes depth
    
    # Equal weighting by default if weights list not provided or all weights are same
    composite_scorer = CompositeScorer(scorers=[keyword_scorer, path_scorer])
    
    strategy = BestFirstCrawlingStrategy(max_depth=1, url_scorer=composite_scorer, max_pages=5)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS, stream=True)

    print("--- CompositeScorer with equal weights for Keyword and PathDepth ---")
    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        async for result in await crawler.arun(url=start_url, config=run_config):
            if result.success:
                print(f"  URL: {result.url}, Score: {result.metadata.get('score', 0.0):.2f}, Depth: {result.metadata.get('depth')}")
    print("Scores are an equal combination of keyword relevance and path depth penalty.")

if __name__ == "__main__":
    asyncio.run(composite_scorer_equal_weights())
```

#### 6.6.2. Example: `CompositeScorer` assigning different `weights` to prioritize one scorer over another.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy
from crawl4ai import KeywordRelevanceScorer, PathDepthScorer, CompositeScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def composite_scorer_different_weights():
    # Keyword relevance is more important
    keyword_scorer = KeywordRelevanceScorer(keywords=["feature"]) 
    path_scorer = PathDepthScorer(higher_score_is_better=False)
    
    composite_scorer = CompositeScorer(
        scorers=[keyword_scorer, path_scorer],
        weights=[0.8, 0.2] # Keyword scorer has 80% influence, PathDepth 20%
    )
    
    strategy = BestFirstCrawlingStrategy(max_depth=1, url_scorer=composite_scorer, max_pages=5)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS, stream=True)

    print("--- CompositeScorer with different weights (Keyword: 0.8, PathDepth: 0.2) ---")
    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        async for result in await crawler.arun(url=start_url, config=run_config):
            if result.success:
                print(f"  URL: {result.url}, Score: {result.metadata.get('score', 0.0):.2f}, Depth: {result.metadata.get('depth')}")
    print("Keyword relevance should more heavily influence scores.")

if __name__ == "__main__":
    asyncio.run(composite_scorer_different_weights())
```

#### 6.6.3. Example: Nesting `CompositeScorer` for more complex scoring logic.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy
from crawl4ai import KeywordRelevanceScorer, PathDepthScorer, ContentTypeScorer, CompositeScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def composite_scorer_nesting():
    keyword_scorer = KeywordRelevanceScorer(keywords=["feature"])
    path_scorer = PathDepthScorer(higher_score_is_better=False)
    content_type_scorer = ContentTypeScorer(content_type_weights={"text/html": 1.0, "application/pdf": -1.0})

    # First level composite: keyword and path
    relevance_and_structure_scorer = CompositeScorer(
        scorers=[keyword_scorer, path_scorer],
        weights=[0.7, 0.3]
    )

    # Second level composite: combine above with content type
    final_scorer = CompositeScorer(
        scorers=[relevance_and_structure_scorer, content_type_scorer],
        weights=[0.8, 0.2] # Relevance/structure is 80%, content type 20%
    )
    
    strategy = BestFirstCrawlingStrategy(max_depth=1, url_scorer=final_scorer, max_pages=5)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS, stream=True)

    print("--- Nested CompositeScorer ---")
    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        async for result in await crawler.arun(url=start_url, config=run_config):
            if result.success:
                 print(f"  URL: {result.url}, Score: {result.metadata.get('score', 0.0):.2f}, Depth: {result.metadata.get('depth')}, Type: {result.response_headers.get('Content-Type')}")
    print("Scores reflect a nested combination of keyword, path, and content type.")

if __name__ == "__main__":
    asyncio.run(composite_scorer_nesting())
```

---
## 7. General Deep Crawl Configuration and Usage

### 7.1. Example: Deep crawling a site that relies heavily on JavaScript for link generation.
This example demonstrates the setup. A real JS-heavy site would be needed for full verification.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, BrowserConfig
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def deep_crawl_js_heavy_site():
    # BrowserConfig enables JS by default.
    # For very JS-heavy sites, ensure headless=False if debugging, and consider timeouts.
    browser_cfg = BrowserConfig(headless=True) # Keep headless for automated tests

    # CrawlerRunConfig might need adjustments for JS execution time
    run_cfg = CrawlerRunConfig(
        page_timeout=30000, # 30 seconds, might need more for complex JS
        # js_code can be used to trigger actions if needed before link discovery
        # js_code="window.scrollTo(0, document.body.scrollHeight);", # Example to scroll
        deep_crawl_strategy=BFSDeePCrawlStrategy(max_depth=1, max_pages=3),
        cache_mode=CacheMode.BYPASS
    )

    print("--- Deep Crawling a JS-Heavy Site (Conceptual: JS execution is enabled by default) ---")
    # Using index.html which has a JS-triggered link via onclick
    start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
    
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        results = await crawler.arun(url=start_url, config=run_cfg)
        
        print(f"Crawled {len(results)} pages.")
        js_link_found = False
        for result in results:
            print(f"  URL: {result.url}")
            if "js_page.html" in result.url:
                js_link_found = True
        
        # This assertion relies on the MockAsyncWebCrawler's _fetch_page
        # correctly parsing links from html_content, even if added by mock JS.
        # A more robust test would involve Playwright's own JS execution.
        # For now, we assume the mock crawler finds links from the final HTML state.
        # To truly test JS-driven links, one would need to modify MockAsyncWebCrawler
        # to simulate JS execution or use a real browser test.
        # This example mainly shows the configuration for enabling JS.
        print("Note: True JS-link discovery depends on Playwright's execution within the crawler.")
        print("The mock crawler simulates link finding from final HTML state.")
        # assert js_link_found, "JS-generated link was not found. Mock might need adjustment or real browser test."


if __name__ == "__main__":
    asyncio.run(deep_crawl_js_heavy_site())
```

### 7.2. Example: How `CrawlerRunConfig` parameters (e.g., `page_timeout`) and `BrowserConfig` (e.g., `user_agent`, `proxy_config`) affect underlying page fetches.
This shows how `BrowserConfig` (passed to `AsyncWebCrawler`) and `CrawlerRunConfig` (passed to `arun`) influence individual page fetches.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, BrowserConfig, ProxyConfig
from unittest.mock import patch

# Mocking a proxy server check - in reality, you'd use a real proxy
async def mock_check_ip_via_proxy(url, config):
    # This function would normally make a request through the proxy
    # and return the perceived IP. For mock, we'll just simulate.
    if config and config.proxy_config and config.proxy_config.server == "http://mockproxy.com:8080":
        return "1.2.3.4" # Mocked IP if proxy is used
    return "9.8.7.6" # Mocked direct IP

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def deep_crawl_with_configs():
    browser_cfg = BrowserConfig(
        user_agent="MyCustomDeepCrawler/1.0",
        proxy_config=ProxyConfig(server="http://mockproxy.com:8080") # This should be used by crawler
    )
    
    # For deep crawl, the page_timeout in CrawlerRunConfig applies to each page fetch
    run_cfg = CrawlerRunConfig(
        page_timeout=15000, # 15s timeout for each page in the deep crawl
        deep_crawl_strategy=BFSDeePCrawlStrategy(max_depth=0), # Just the start URL
        cache_mode=CacheMode.BYPASS
    )

    print("--- Deep Crawl with Custom Browser & Run Configs ---")
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        # The crawler instance now has the browser_cfg settings.
        # We expect its internal page fetches to use these.
        
        # We'd need to inspect logs or mock `crawler.strategy._fetch_page` to truly verify user_agent/proxy.
        # For this example, we'll conceptually check based on setup.
        print(f"Browser User-Agent set to: {crawler.browser_config.user_agent}")
        if crawler.browser_config.proxy_config:
            print(f"Browser Proxy set to: {crawler.browser_config.proxy_config.server}")
        
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_cfg)
        
        if results and results[0].success:
            print(f"Crawled {results[0].url} successfully with page_timeout={run_cfg.page_timeout}ms")
            # In a real scenario with a proxy, you'd verify the source IP.
            # For mock:
            # perceived_ip = await mock_check_ip_via_proxy(start_url, browser_cfg) 
            # print(f"Perceived IP (mocked): {perceived_ip}")
            # assert perceived_ip == "1.2.3.4" # Assuming proxy was used
        else:
            print(f"Crawl failed for {start_url}")

if __name__ == "__main__":
    asyncio.run(deep_crawl_with_configs())
```

### 7.3. Example: Iterating through deep crawl results and handling cases where some pages failed to crawl or were filtered out.
A robust deep crawl should handle partial failures gracefully.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain, URLPatternFilter
from unittest.mock import patch

# Add a URL that will "fail" in our mock
MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/failing_page.html"] = {
    "html_content": None, # Simulate failure by not providing content
    "success": False,
    "status_code": 500,
    "error_message": "Mock Server Error"
}
MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/index.html"]["html_content"] += '<a href="failing_page.html">Failing Page</a>'


@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def deep_crawl_handling_failures():
    # Filter out '/archive/' pages, and one page will fail
    url_filter = URLPatternFilter(patterns=["*/archive/*"], block_list=True)
    filter_chain = FilterChain(filters=[url_filter])
    
    strategy = BFSDeePCrawlStrategy(max_depth=1, filter_chain=filter_chain)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"--- Deep Crawl - Handling Failures and Filtered Pages ---")
        successful_pages = 0
        failed_pages = 0
        
        for result in results:
            if result.success:
                successful_pages += 1
                print(f"  SUCCESS: {result.url} (Depth: {result.metadata.get('depth')})")
                assert "/archive/" not in result.url
            else:
                failed_pages += 1
                print(f"  FAILURE: {result.url} (Error: {result.error_message}, Status: {result.status_code})")
        
        print(f"\nTotal Successful: {successful_pages}, Total Failed/Filtered Out by crawler: {failed_pages}")
        # Start URL + index links (page1, page2, external, blog, login, failing) = 7 initial candidates
        # - external might be skipped by default include_external=False (depends on strategy)
        # - /archive/ is filtered by URLPatternFilter
        # - failing_page.html will fail
        # So, we expect start_url + page1, page2, blog, login. Failing page is in results but success=False.
        # The number of results includes the start_url and pages that were attempted.
        # Filters apply to links *discovered* from a page.
        
        # One page (/archive/old_page.html) should be filtered by the filter chain.
        # One page (failing_page.html) should be in results but with success=False.
        assert any("failing_page.html" in r.url and not r.success for r in results)
        assert not any("/archive/" in r.url for r in results)

    # Clean up mock data
    del MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/failing_page.html"]
    MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/index.html"]["html_content"] = MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/index.html"]["html_content"].replace('<a href="failing_page.html">Failing Page</a>', '')

if __name__ == "__main__":
    asyncio.run(deep_crawl_handling_failures())
```

### 7.4. Example: Using a custom `logger` instance passed to a `DeepCrawlStrategy`.

```python
import asyncio
import logging
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, AsyncLogger
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def deep_crawl_custom_logger():
    # Setup a custom logger
    custom_logger = AsyncLogger(log_file="custom_deep_crawl.log", name="MyDeepCrawler", level="DEBUG")
    
    strategy = BFSDeePCrawlStrategy(max_depth=0, logger=custom_logger) # Pass logger to strategy
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    print("--- Deep Crawl with Custom Logger ---")
    async with AsyncWebCrawler() as crawler: # Main crawler logger can be default
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        await crawler.arun(url=start_url, config=run_config)
        
    print("Crawl complete. Check 'custom_deep_crawl.log' for logs from the strategy.")
    # You can verify the log file content here if needed
    # e.g., with open("custom_deep_crawl.log", "r") as f: assert "MyDeepCrawler" in f.read()
    # For this example, just visual confirmation is sufficient.

if __name__ == "__main__":
    asyncio.run(deep_crawl_custom_logger())
```

### 7.5. Example: Deep crawling starting from a local HTML file that contains links to other local files or web URLs.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy
from unittest.mock import patch
from pathlib import Path
import os

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def deep_crawl_from_local_file():
    # Ensure the mock local files exist for the test
    local_index_path = Path(os.getcwd()) / "test_local_index.html"
    local_page1_path = Path(os.getcwd()) / "test_local_page1.html"
    
    # If not created by preamble, create them
    if not local_index_path.exists():
        local_index_path.write_text(MOCK_SITE_DATA[f"file://{local_index_path}"]["html_content"])
    if not local_page1_path.exists():
        local_page1_path.write_text(MOCK_SITE_DATA[f"file://{local_page1_path}"]["html_content"])

    start_file_url = f"file://{local_index_path.resolve()}"
    
    strategy = BFSDeePCrawlStrategy(max_depth=1, include_external=True) # Allow following to web URLs
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    print(f"--- Deep Crawling from Local File: {start_file_url} ---")
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun(url=start_file_url, config=run_config)
        
        print(f"Crawled {len(results)} pages.")
        found_local_link = False
        found_web_link = False
        for result in results:
            print(f"  URL: {result.url}, Depth: {result.metadata.get('depth')}")
            if result.url == f"file://{local_page1_path.resolve()}":
                found_local_link = True
            if result.url == "https://docs.crawl4ai.com/vibe-examples/index.html":
                found_web_link = True
        
        assert found_local_link, "Did not follow local file link."
        assert found_web_link, "Did not follow web link from local file."
    
    # Clean up dummy files
    if local_index_path.exists(): os.remove(local_index_path)
    if local_page1_path.exists(): os.remove(local_page1_path)


if __name__ == "__main__":
    asyncio.run(deep_crawl_from_local_file())
```

### 7.6. Example: Comparing outputs from `BFSDeePCrawlStrategy`, `DFSDeePCrawlStrategy`, and `BestFirstCrawlingStrategy`.
This example runs all three main strategies with similar settings to highlight differences in traversal and results.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai import BFSDeePCrawlStrategy, DFSDeePCrawlStrategy, BestFirstCrawlingStrategy, KeywordRelevanceScorer
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def compare_deep_crawl_strategies():
    start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
    max_depth = 2
    max_pages = 7 # Keep it manageable for comparison
    
    common_config_params = {
        "max_depth": max_depth,
        "max_pages": max_pages,
        "include_external": False, # Keep it simple for comparison
    }
    
    scorer = KeywordRelevanceScorer(keywords=["feature", "core"])

    strategies_to_compare = {
        "BFS": BFSDeePCrawlStrategy(**common_config_params),
        "DFS": DFSDeePCrawlStrategy(**common_config_params),
        "Best-First": BestFirstCrawlingStrategy(**common_config_params, url_scorer=scorer)
    }

    print(f"--- Comparing Deep Crawl Strategies (max_depth={max_depth}, max_pages={max_pages}) ---")

    async with AsyncWebCrawler() as crawler:
        for name, strategy_instance in strategies_to_compare.items():
            print(f"\n-- Running {name} Strategy --")
            run_config = CrawlerRunConfig(
                deep_crawl_strategy=strategy_instance,
                cache_mode=CacheMode.BYPASS,
                stream=False # Batch for easier comparison of final set
            )
            
            start_time = time.perf_counter()
            results = await crawler.arun(url=start_url, config=run_config)
            duration = time.perf_counter() - start_time
            
            print(f"  {name} crawled {len(results)} pages in {duration:.2f}s.")
            # Sort by depth then URL for consistent output for BFS/DFS
            # For Best-First, sort by score (desc) then depth then URL
            if name == "Best-First":
                 sorted_results = sorted(results, key=lambda r: (r.metadata.get('score', 0.0), -r.metadata.get('depth', 0), r.url), reverse=True)
            else:
                 sorted_results = sorted(results, key=lambda r: (r.metadata.get('depth', 0), r.url))


            for i, r in enumerate(sorted_results):
                if i < 5 or i > len(sorted_results) - 3 : # Show first 5 and last 2
                    score_str = f", Score: {r.metadata.get('score', 0.0):.2f}" if name == "Best-First" else ""
                    print(f"    URL: {r.url} (Depth: {r.metadata.get('depth')}{score_str})")
                elif i == 5:
                    print(f"    ... ({len(sorted_results) - 5 -2 } more results) ...")
            print("-" * 30)

if __name__ == "__main__":
    asyncio.run(compare_deep_crawl_strategies())
```

---
## 8. Advanced Scenarios & Customization

### 8.1. Example: Implementing a custom `DeepCrawlStrategy` by subclassing `DeepCrawlStrategy`.
This provides a skeleton for creating your own crawl logic.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DeepCrawlStrategy, CrawlResult
from typing import List, Set, Dict, AsyncGenerator, Tuple
from unittest.mock import patch

class MyCustomDeepCrawlStrategy(DeepCrawlStrategy):
    def __init__(self, max_depth=1, **kwargs):
        self.max_depth = max_depth
        # Potentially other custom init params
        super().__init__(**kwargs) # Pass along other kwargs if base class uses them
        print("MyCustomDeepCrawlStrategy Initialized")

    async def _arun_batch(self, start_url: str, crawler: AsyncWebCrawler, config: CrawlerRunConfig) -> List[CrawlResult]:
        print(f"[Custom Strategy] _arun_batch called for: {start_url}")
        # Implement batch crawling logic (e.g., BFS-like)
        # This is a simplified version. A real one needs queue, visited set, depth tracking etc.
        results = []
        initial_result_container = await crawler.arun(url=start_url, config=config.clone(deep_crawl_strategy=None))
        initial_result = initial_result_container[0] # arun returns a list
        
        if not initial_result.success: return [initial_result]
        results.append(initial_result)
        
        if self.max_depth > 0 and initial_result.links.get("internal"):
            for link_info in initial_result.links["internal"][:2]: # Crawl first 2 internal links
                link_url = link_info["href"]
                # Pass metadata for depth and parent
                link_config = config.clone(deep_crawl_strategy=None)
                
                # In a real strategy, you'd manage metadata directly or pass it for crawler.arun
                # For this mock, we simplify as crawler.arun normally doesn't take depth/parent for single page
                print(f"  [Custom Strategy] Crawling linked URL: {link_url} at depth 1")
                linked_result_container = await crawler.arun(url=link_url, config=link_config)
                linked_result = linked_result_container[0]
                # Manually add metadata for this example
                if linked_result.metadata is None: linked_result.metadata = {}
                linked_result.metadata['depth'] = 1
                linked_result.metadata['parent_url'] = start_url
                results.append(linked_result)
        return results

    async def _arun_stream(self, start_url: str, crawler: AsyncWebCrawler, config: CrawlerRunConfig) -> AsyncGenerator[CrawlResult, None]:
        print(f"[Custom Strategy] _arun_stream called for: {start_url}")
        # Implement streaming crawling logic
        # Simplified: yields results from a batch-like process for this example
        batch_results = await self._arun_batch(start_url, crawler, config)
        for result in batch_results:
            yield result
            
    async def can_process_url(self, url: str, depth: int) -> bool:
        # Example: only process URLs not containing "archive" and within max_depth
        print(f"[Custom Strategy] can_process_url called for: {url}, depth: {depth}")
        if "archive" in url:
            return False
        return depth <= self.max_depth

    async def link_discovery(
        self, result: CrawlResult, source_url: str, current_depth: int, 
        visited: Set[str], next_level: List[Tuple[str, str]], depths: Dict[str, int]
    ) -> None:
        # This method is crucial for discovering and queuing new links.
        # The base class might have a default implementation, or you might need to call
        # crawler.arun to get links if result.links is not populated.
        # For this example, we'll assume result.links is populated by the crawler.
        print(f"[Custom Strategy] link_discovery for: {source_url} at depth {current_depth}")
        new_depth = current_depth + 1
        if new_depth > self.max_depth:
            return

        for link_info in result.links.get("internal", [])[:3]: # Limit for example
            link_url = link_info["href"]
            if link_url not in visited and await self.can_process_url(link_url, new_depth):
                next_level.append((link_url, source_url)) # (url, parent_url)
                depths[link_url] = new_depth
                print(f"  [Custom Strategy] Discovered and added to queue: {link_url}")
    
    async def shutdown(self):
        print("[Custom Strategy] Shutdown called.")
        # Implement any cleanup or signal to stop crawling loops


@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def custom_deep_crawl_strategy_example():
    custom_strategy = MyCustomDeepCrawlStrategy(max_depth=1)
    run_config = CrawlerRunConfig(deep_crawl_strategy=custom_strategy, cache_mode=CacheMode.BYPASS)

    print("--- Using Custom DeepCrawlStrategy ---")
    async with AsyncWebCrawler() as crawler: # This will be MockAsyncWebCrawler
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"\nCustom strategy crawled {len(results)} pages:")
        for r in results:
            print(f"  URL: {r.url}, Success: {r.success}, Depth: {r.metadata.get('depth') if r.metadata else 'N/A'}")

if __name__ == "__main__":
    asyncio.run(custom_deep_crawl_strategy_example())
```

### 8.2. Example: Implementing a custom `URLFilter`.
`URLFilter` itself is a concrete class, but you can create custom logic by making a callable class or function that adheres to the expected filter signature `(url: str) -> bool`. For more complex stateful filters, subclassing a base might be an option if one is provided or creating your own structure.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, FilterChain
from unittest.mock import patch

class MyCustomURLFilter:
    def __init__(self, forbidden_keyword: str):
        self.forbidden_keyword = forbidden_keyword.lower()
        print(f"MyCustomURLFilter initialized to block URLs with '{self.forbidden_keyword}'")

    async def __call__(self, url: str) -> bool: # Filters must be async
        """Return True if URL should be allowed, False if blocked."""
        if self.forbidden_keyword in url.lower():
            print(f"[CustomFilter] Blocking URL: {url} (contains '{self.forbidden_keyword}')")
            return False # Block if keyword found
        print(f"[CustomFilter] Allowing URL: {url}")
        return True # Allow otherwise

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def custom_url_filter_example():
    custom_filter = MyCustomURLFilter(forbidden_keyword="archive")
    filter_chain = FilterChain(filters=[custom_filter])
    
    strategy = BFSDeePCrawlStrategy(max_depth=1, filter_chain=filter_chain)
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS)

    print("--- Using Custom URLFilter (blocking 'archive') ---")
    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"\nCustom filter crawl resulted in {len(results)} pages:")
        for r in results:
            print(f"  URL: {r.url}")
            assert "archive" not in r.url.lower(), f"Custom filter failed to block {r.url}"
        print("Successfully blocked URLs containing 'archive'.")

if __name__ == "__main__":
    asyncio.run(custom_url_filter_example())
```

### 8.3. Example: Implementing a custom `URLScorer` for `BestFirstCrawlingStrategy`.
Subclass `URLScorer` and implement the `score` method.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BestFirstCrawlingStrategy, URLScorer
from urllib.parse import urlparse
from unittest.mock import patch

class MyCustomURLScorer(URLScorer):
    def __init__(self, preferred_domain: str, weight: float = 1.0):
        super().__init__(weight)
        self.preferred_domain = preferred_domain
        print(f"MyCustomURLScorer initialized, preferring domain: {self.preferred_domain}")

    def score(self, url: str, **kwargs) -> float:
        """Scores URL based on whether it matches the preferred domain."""
        parsed_url = urlparse(url)
        score = 0.0
        if parsed_url.netloc == self.preferred_domain:
            score = 1.0 * self.weight
            print(f"[CustomScorer] URL {url} matches preferred domain. Score: {score}")
        else:
            score = 0.1 * self.weight # Lower score for other domains
            print(f"[CustomScorer] URL {url} does NOT match preferred domain. Score: {score}")
        return score

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def custom_url_scorer_example():
    custom_scorer = MyCustomURLScorer(preferred_domain="docs.crawl4ai.com", weight=2.0)
    
    strategy = BestFirstCrawlingStrategy(
        max_depth=1, 
        url_scorer=custom_scorer,
        include_external=True, # To allow scoring external domains differently
        max_pages=5
    )
    run_config = CrawlerRunConfig(deep_crawl_strategy=strategy, cache_mode=CacheMode.BYPASS, stream=True)

    print("--- Using Custom URLScorer (preferring 'docs.crawl4ai.com') ---")
    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        async for result in await crawler.arun(url=start_url, config=run_config):
            if result.success:
                print(f"  URL: {result.url}, Score: {result.metadata.get('score', 0.0):.2f}")
    print("Pages from 'docs.crawl4ai.com' should generally have higher scores.")

if __name__ == "__main__":
    asyncio.run(custom_url_scorer_example())
```

### 8.4. Example: Deep crawling a site with very large number of pages efficiently using `max_pages` and streaming.
This combines `max_pages` to limit the scope and `stream=True` to process results incrementally, which is crucial for very large crawls to manage memory and get feedback sooner.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy
from unittest.mock import patch

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def deep_crawl_large_site_efficiently():
    # Simulate a large site by setting a high conceptual depth,
    # but limit actual work with max_pages.
    strategy = BFSDeePCrawlStrategy(
        max_depth=10,      # Imagine this could lead to thousands of pages
        max_pages=10,      # But we only want the first 10 found by BFS
        include_external=False 
    )
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        stream=True,       # Process results as they come
        cache_mode=CacheMode.BYPASS # Or CacheMode.ENABLED for subsequent partial crawls
    )

    print("--- Efficiently Crawling a 'Large' Site (max_pages=10, stream=True) ---")
    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html" # Use our mock site
        
        crawled_count = 0
        async for result in await crawler.arun(url=start_url, config=run_config):
            crawled_count += 1
            if result.success:
                print(f"  Processed ({crawled_count}/{strategy.max_pages}): {result.url} at depth {result.metadata.get('depth')}")
            else:
                print(f"  Failed ({crawled_count}/{strategy.max_pages}): {result.url} - {result.error_message}")
            
            if crawled_count >= strategy.max_pages:
                print(f"Reached max_pages limit of {strategy.max_pages}. Stopping.")
                # In a real scenario, you might need to call strategy.shutdown() if the crawler
                # doesn't automatically stop precisely at max_pages when streaming.
                # However, strategies are designed to respect max_pages.
                break 
                
        print(f"\nTotal pages processed: {crawled_count}")
        assert crawled_count <= strategy.max_pages

if __name__ == "__main__":
    asyncio.run(deep_crawl_large_site_efficiently())
```

### 8.5. Example: Combining deep crawling with `LLMExtractionStrategy` to extract structured data from each crawled page.
This example shows setting up a deep crawl where each successfully crawled page's content is then passed to an `LLMExtractionStrategy`.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, LLMExtractionStrategy, LLMConfig
from pydantic import BaseModel, Field
from unittest.mock import patch

class PageSummary(BaseModel):
    title: str = Field(description="The main title of the page.")
    brief_summary: str = Field(description="A one-sentence summary of the page content.")

# Mock the LLM call within the extraction strategy for this example
async def mock_llm_extract(self, url: str, sections: list[str]):
    print(f"[Mock LLM] Extracting from {url}, first section: {sections[0][:50]}...")
    # Based on the URL from MOCK_SITE_DATA, return a plausible mock summary
    if "index.html" in url:
        return [{"title": "Index", "brief_summary": "This is the main page."}]
    elif "page1.html" in url:
        return [{"title": "Page 1", "brief_summary": "Content about crawl strategies."}]
    elif "page2.html" in url:
        return [{"title": "Page 2 - Feature Rich", "brief_summary": "Discusses a key feature."}]
    return [{"title": "Unknown Title", "brief_summary": "Could not summarize."}]

@patch('crawl4ai.extraction_strategy.LLMExtractionStrategy.run', side_effect=mock_llm_extract)
@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def deep_crawl_with_llm_extraction(mock_llm_run): # mock_llm_run is from the patch
    llm_config = LLMConfig(provider="mock/mock-model") # Mock provider
    
    extraction_strategy = LLMExtractionStrategy(
        llm_config=llm_config,
        schema=PageSummary.model_json_schema(), # Use Pydantic model for schema
        extraction_type="schema",
        instruction="Extract the title and a brief summary for the provided HTML content."
    )
    
    deep_crawl_config = BFSDeePCrawlStrategy(max_depth=1, max_pages=3)
    
    run_config = CrawlerRunConfig(
        deep_crawl_strategy=deep_crawl_config,
        extraction_strategy=extraction_strategy, # Apply this to each crawled page
        cache_mode=CacheMode.BYPASS
    )

    print("--- Deep Crawl with LLM Extraction on Each Page ---")
    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        for result in results:
            if result.success:
                print(f"\nCrawled URL: {result.url}")
                if result.extracted_content:
                    print(f"  Extracted Data: {result.extracted_content}")
                else:
                    print("  No data extracted (or LLM mock returned empty).")
            else:
                print(f"\nFailed to crawl URL: {result.url} - {result.error_message}")
        
        assert mock_llm_run.called, "LLM Extraction strategy's run method was not called."

if __name__ == "__main__":
    asyncio.run(deep_crawl_with_llm_extraction())
```

### 8.6. Example: Scenario for using `can_process_url` within a strategy to dynamically decide if a URL should be added to the queue.
Override `can_process_url` in a custom strategy to implement dynamic filtering logic based on URL and current depth.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeePCrawlStrategy, CrawlResult
from typing import List, Set, Dict, Tuple
from unittest.mock import patch

class DepthAndPatternAwareBFSStrategy(BFSDeePCrawlStrategy):
    async def can_process_url(self, url: str, depth: int) -> bool:
        # Standard checks from parent (like filter_chain)
        if not await super().can_process_url(url, depth):
            print(f"[Custom can_process_url] Blocked by parent: {url}")
            return False
        
        # Custom logic: Do not process '/archive/' pages if depth is > 1
        if depth > 1 and "/archive/" in url:
            print(f"[Custom can_process_url] Blocking deep archive page: {url} at depth {depth}")
            return False
        
        print(f"[Custom can_process_url] Allowing: {url} at depth {depth}")
        return True

@patch('crawl4ai.AsyncWebCrawler', MockAsyncWebCrawler)
async def custom_can_process_url_example():
    # Add a deeper archive link for testing
    MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/page1.html"]["html_content"] += '<a href="archive/deep_archive.html">Deep Archive</a>'
    MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/archive/deep_archive.html"] = {
        "html_content": "<html><title>Deep Archive</title><body>Very old stuff.</body></html>",
        "response_headers": {"Content-Type": "text/html"}
    }

    custom_strategy = DepthAndPatternAwareBFSStrategy(max_depth=2) # Crawl up to depth 2
    run_config = CrawlerRunConfig(deep_crawl_strategy=custom_strategy, cache_mode=CacheMode.BYPASS)

    print("--- Custom Strategy with Dynamic can_process_url ---")
    async with AsyncWebCrawler() as crawler:
        start_url = "https://docs.crawl4ai.com/vibe-examples/index.html"
        results = await crawler.arun(url=start_url, config=run_config)
        
        print(f"\nCrawled {len(results)} pages:")
        archive_at_depth_1_crawled = False
        deep_archive_blocked = True

        for r in results:
            print(f"  URL: {r.url}, Depth: {r.metadata.get('depth')}")
            if "/archive/old_page.html" in r.url and r.metadata.get('depth') == 1:
                archive_at_depth_1_crawled = True
            if "/archive/deep_archive.html" in r.url and r.metadata.get('depth') == 2:
                 # This should not happen due to our custom can_process_url
                deep_archive_blocked = False 
        
        assert archive_at_depth_1_crawled, "Archive page at depth 1 should have been crawled."
        assert deep_archive_blocked, "Deep archive page at depth 2 should have been blocked by custom can_process_url."
        print("Dynamic URL processing logic worked as expected.")

    # Clean up mock data
    MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/page1.html"]["html_content"] = MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/page1.html"]["html_content"].replace('<a href="archive/deep_archive.html">Deep Archive</a>', '')
    del MOCK_SITE_DATA["https://docs.crawl4ai.com/vibe-examples/archive/deep_archive.html"]


if __name__ == "__main__":
    asyncio.run(custom_can_process_url_example())
    # Clean up dummy files after all examples run
    if (Path(os.getcwd()) / "test_local_index.html").exists():
        os.remove(Path(os.getcwd()) / "test_local_index.html")
    if (Path(os.getcwd()) / "test_local_page1.html").exists():
        os.remove(Path(os.getcwd()) / "test_local_page1.html")
    if Path("custom_deep_crawl.log").exists():
        os.remove("custom_deep_crawl.log")

```

---

