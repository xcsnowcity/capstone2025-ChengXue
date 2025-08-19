#!/usr/bin/env python3
import asyncio
import xml.etree.ElementTree as ET
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set
import re
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator


class SitemapContentCrawler:
    def __init__(self):
        self.output_dir = Path("Knowledge Base/crawl4ai_content")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Sitemap configurations
        self.sitemap_configs = [
            {
                "name": "HSE",
                "sitemap_url": "https://www.hse.ie/sitemap.xml",
                "keywords": [
                    "domestic-violence", "socialinclusion", "primarycare", 
                    "acute-hospitals-division/woman-infants", "mental-health",
                    "child-protection", "abuse", "violence", "trauma"
                ]
            },
            {
                "name": "Tusla", 
                "sitemap_url": "https://www.tusla.ie/sitemap.xml",
                "keywords": [
                    "domestic", "violence", "abuse", "gender-based", "sexual",
                    "child-protection", "family-support", "trauma", "welfare"
                ]
            }
        ]

    def fetch_sitemap(self, sitemap_url: str) -> List[str]:
        try:
            print(f"Fetching sitemap: {sitemap_url}")
            response = requests.get(sitemap_url, timeout=30)
            response.raise_for_status()
            
            # Handle single-line XML
            xml_content = response.text
            if not xml_content.startswith('<?xml'):
                # Fix malformed XML if needed
                xml_content = '<?xml version="1.0" encoding="utf-8"?>\n' + xml_content
                
            root = ET.fromstring(xml_content)
            
            # Extract URLs from sitemap
            urls = []
            for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                loc_elem = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                if loc_elem is not None:
                    urls.append(loc_elem.text)
                    
            print(f"  Found {len(urls)} total URLs in sitemap")
            return urls
            
        except Exception as e:
            print(f"  Error fetching sitemap: {e}")
            return []

    def filter_relevant_urls(self, urls: List[str], keywords: List[str]) -> List[Dict]:
        relevant_urls = []
        
        for url in urls:
            url_lower = url.lower()
            
            # Skip PDFs (can't crawl as web pages)
            if url_lower.endswith('.pdf'):
                continue
                
            score = 0
            matched_keywords = []
            
            # Score based on keyword matches
            for keyword in keywords:
                if keyword.lower() in url_lower:
                    score += 1
                    matched_keywords.append(keyword)
                    
            # Additional scoring for high-value patterns
            if 'domestic-violence' in url_lower or 'domestic-sexual-and-gender-based-violence' in url_lower:
                score += 5
            elif any(term in url_lower for term in ['abuse', 'violence', 'trauma']):
                score += 2
            elif any(term in url_lower for term in ['support', 'services', 'help']):
                score += 1
                
            # Only include URLs with relevance score >= 4 (high-quality DV content)
            if score >= 4:
                relevant_urls.append({
                    'url': url,
                    'score': score,
                    'keywords': matched_keywords
                })
                
        # Sort by relevance score (highest first)
        relevant_urls.sort(key=lambda x: x['score'], reverse=True)
        
        print(f"  Filtered to {len(relevant_urls)} relevant URLs (PDFs excluded)")
        for i, url_info in enumerate(relevant_urls[:5]):
            print(f"    {i+1}. [{url_info['score']}] {url_info['url']}")
            
        return relevant_urls

    async def crawl_urls(self, url_list: List[Dict], source_name: str):
        
        browser_config = BrowserConfig(
            browser_type="firefox",
            headless=True,
            verbose=True
        )
        
        crawler_config = CrawlerRunConfig(
            # Content processing
            markdown_generator=DefaultMarkdownGenerator(),
            
            # Optimization settings
            word_count_threshold=100,
            only_text=True,
            cache_mode=CacheMode.BYPASS,
            process_iframes=False,
            scan_full_page=True,
            
            # Remove navigation/footer clutter
            excluded_tags=['script', 'style', 'nav', 'header', 'footer', 'aside', 'advertisement'],
            remove_overlay_elements=True,
            # No CSS selector restriction - capture all content
        )
        
        successful_extractions = 0
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            for i, url_info in enumerate(url_list, 1):
                url = url_info['url']
                score = url_info['score']
                
                print(f"\n[{i}/{len(url_list)}] Crawling: {url}")
                print(f"  Relevance Score: {score}")
                
                try:
                    result = await crawler.arun(url=url, config=crawler_config)
                    
                    if result.success and result.markdown:
                        content = result.markdown.strip()
                        
                        if len(content) > 100:  # Minimum content threshold (lowered)
                            # Generate unique filename with URL hash to prevent overwrites
                            import hashlib
                            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
                            url_slug = re.sub(r'[^\w\-]', '_', url.split('/')[-1] if url.endswith('/') else url.split('/')[-1])
                            timestamp = datetime.now().strftime("%H%M%S")
                            filename = f"{source_name.lower()}_{score:02d}_{url_hash}_{url_slug[:30]}_{timestamp}.md"
                            filepath = self.output_dir / filename
                            
                            # Metadata
                            metadata = {
                                "url": url,
                                "title": (result.metadata.get('title') if result.metadata else None) or "Untitled",
                                "source": source_name,
                                "relevance_score": score,
                                "keywords": url_info['keywords'],
                                "extraction_time": datetime.now().isoformat(),
                                "word_count": len(content.split()),
                                "character_count": len(content)
                            }
                            
                            # Write content with metadata
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(f"# {metadata['title']}\n\n")
                                f.write(f"**Source:** {source_name} ({url})\n")
                                f.write(f"**Relevance Score:** {score}/10\n")
                                f.write(f"**Keywords:** {', '.join(url_info['keywords'])}\n")
                                f.write(f"**Extracted:** {metadata['extraction_time']}\n")
                                f.write(f"**Words:** {metadata['word_count']}\n\n")
                                f.write("---\n\n")
                                f.write(content)
                                
                            print(f"  Saved: {metadata['word_count']} words → {filename}")
                            successful_extractions += 1
                        else:
                            print(f"  Content too short: {len(content)} chars")
                    else:
                        print(f"  Failed to extract content")
                        
                except Exception as e:
                    print(f"  Error crawling {url}: {str(e)}")
                    
        return successful_extractions

    async def run_comprehensive_crawl(self):
        
        print("Sitemap-Based Content Crawler for Irish DV Support")
        print("=" * 70)
        
        total_successful = 0
        
        for config in self.sitemap_configs:
            print(f"\nProcessing {config['name']} sitemap...")
            print("=" * 50)
            
            # Fetch sitemap
            all_urls = self.fetch_sitemap(config['sitemap_url'])
            
            if not all_urls:
                print(f"  No URLs found for {config['name']}")
                continue
                
            # Filter relevant URLs
            relevant_urls = self.filter_relevant_urls(all_urls, config['keywords'])
            
            if not relevant_urls:
                print(f"  No relevant URLs found for {config['name']}")
                continue
                
            # Crawl all discovered URLs (no limit)
            print(f"  Crawling all {len(relevant_urls)} relevant URLs")
            print(f"  Estimated time: {(len(relevant_urls) * 3) // 60} minutes")
            
            # Crawl the URLs
            successful = await self.crawl_urls(relevant_urls, config['name'])
            total_successful += successful
            
            print(f"\n{config['name']} Summary: {successful}/{len(relevant_urls)} URLs successfully crawled")
        
        print(f"\nCrawling Complete!")
        print(f"Total successful extractions: {total_successful}")
        print(f"Content saved to: {self.output_dir}")
        
        return total_successful > 0


async def main():
    print("Testing Firefox Browser Setup...")
    
    # Test browser
    browser_config = BrowserConfig(browser_type="firefox", headless=True, verbose=True)
    async with AsyncWebCrawler(config=browser_config) as crawler:
        test_result = await crawler.arun(url="https://httpbin.org/html")
        if test_result.success:
            print("Firefox browser working correctly!\n")
        else:
            print("Browser test failed!")
            return False
    
    # Run sitemap crawler
    crawler = SitemapContentCrawler()
    success = await crawler.run_comprehensive_crawl()
    
    if success:
        print("\nAll done")
    else:
        print("\nSitemap crawling failed")
    
    return success


if __name__ == "__main__":
    asyncio.run(main())