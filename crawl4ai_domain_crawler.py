#!/usr/bin/env python3
import os
import asyncio
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from urllib.parse import urljoin, urlparse
import re

# Crawl4AI imports with advanced filtering
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai import LLMExtractionStrategy
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

# Our knowledge base processor
from main import KnowledgeBaseProcessor

class ComprehensiveDomainCrawler:
    def __init__(self):
        self.kb_processor = KnowledgeBaseProcessor()
        self.output_dir = Path("Knowledge Base/crawl4ai_domain_content")
        self.output_dir.mkdir(exist_ok=True)
        
        # Browser configuration with Firefox
        self.browser_config = BrowserConfig(
            browser_type="firefox",
            headless=True,
            viewport_width=1280,
            viewport_height=720,
            verbose=True
        )
        
        # Target domains with intelligent stopping criteria
        self.target_domains = [
            {
                "domain": "hse.ie",
                "organization": "HSE",
                "priority_score": 9,  # Critical health resource
                "max_crawl_hours": 3,  # Time-based limit
                "focus_keywords": ["domestic", "violence", "abuse", "safety", "protection", "victim", "survivor"],
                "exclude_paths": ["/images/", "/downloads/", "/admin/", "/api/", "/jobs/"],
                "min_relevance_score": 6.0,
                "stop_after_consecutive_low_scores": 20,
                "max_depth": 4
            },
            {
                "domain": "tusla.ie", 
                "organization": "Tusla",
                "priority_score": 8,  # Child protection focus
                "max_crawl_hours": 2,
                "focus_keywords": ["domestic", "violence", "abuse", "child", "protection", "family", "safety"],
                "exclude_paths": ["/images/", "/downloads/", "/careers/", "/tenders/"],
                "min_relevance_score": 6.0,
                "stop_after_consecutive_low_scores": 15,
                "max_depth": 3
            },
            {
                "domain": "citizensinformation.ie",
                "organization": "Citizens Information", 
                "priority_score": 9,  # Critical legal resource
                "max_crawl_hours": 2.5,
                "focus_keywords": ["domestic", "violence", "abuse", "safety", "order", "legal", "rights", "court"],
                "exclude_paths": ["/images/", "/downloads/", "/admin/", "/api/", "/news/archive/"],
                "min_relevance_score": 7.0,  # Higher threshold for legal content
                "stop_after_consecutive_low_scores": 15,
                "max_depth": 3
            }
        ]
        
        # DV relevance LLM strategy
        self.setup_dv_filter_strategy()
        
        # Smart content filtering
        self.content_filter = PruningContentFilter(threshold=0.5)
        self.markdown_generator = DefaultMarkdownGenerator(
            content_filter=self.content_filter,
            options={"citations": True, "ignore_links": False}
        )
        
    def setup_dv_filter_strategy(self):
        try:
            from crawl4ai.extraction_strategy import LLMConfig
            llm_config = LLMConfig(
                provider="openai",
                api_key=os.getenv("OPENROUTER_API_KEY"),
                model="google/gemini-2.0-flash-exp", 
                base_url="https://openrouter.ai/api/v1"
            )
            
            self.dv_filter_strategy = LLMExtractionStrategy(
                llm_config=llm_config,
                schema={
                    "type": "object",
                    "properties": {
                        "is_dv_relevant": {
                            "type": "boolean",
                            "description": "Is this content relevant to domestic violence support, legal rights, or victim assistance?"
                        },
                        "relevance_score": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 10,
                            "description": "Relevance score from 0-10, where 10 is highly relevant DV content"
                        },
                        "content_type": {
                            "type": "string", 
                            "enum": ["legal", "support", "medical", "emergency", "resources", "education", "irrelevant"],
                            "description": "Type of domestic violence content"
                        },
                        "key_topics": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Key domestic violence topics mentioned (e.g., safety orders, counseling, emergency contacts)"
                        },
                        "clean_summary": {
                            "type": "string",
                            "description": "Clean, factual summary of the domestic violence information without website navigation"
                        }
                    },
                    "required": ["is_dv_relevant", "relevance_score", "content_type"]
                },
                instruction="""
                Analyze this web page content to determine if it's relevant to domestic violence support in Ireland.

                Look for:
                - Legal information (safety orders, barring orders, legal rights)
                - Support services (counseling, helplines, shelters) 
                - Medical/healthcare support for DV victims
                - Emergency procedures and contacts
                - Educational content about recognizing abuse
                - Resources for survivors (housing, financial support)

                IGNORE:
                - General medical conditions unrelated to DV
                - Job listings and careers pages
                - Administrative/technical content
                - Marketing and promotional material
                - Website navigation and headers/footers

                Focus on Irish-specific domestic violence content that would help survivors.
                """
            )
            self.use_llm_filter = True
            print("DV relevance LLM filter configured")
        except Exception as e:
            print(f"LLM filter not available: {e}")
            self.use_llm_filter = False
    
    def create_crawl_config(self, domain_info: Dict) -> CrawlerRunConfig:
        
        # Build keyword-based CSS selectors for faster filtering
        keyword_selectors = []
        for keyword in domain_info["focus_keywords"]:
            keyword_selectors.extend([
                f"[*|*='{keyword}' i]",  # Attribute contains keyword
                f"*:contains('{keyword}')",  # Text contains keyword  
            ])
        
        return CrawlerRunConfig(
            # Performance optimizations
            cache_mode=CacheMode.BYPASS,
            page_timeout=15000,
            
            # Content filtering
            word_count_threshold=100,  # Skip very short pages
            excluded_tags=['script', 'style', 'nav', 'header', 'footer', 'form', 'iframe'],
            excluded_selector="#cookie-banner, .advertisement, .social-media, .navigation",
            
            # Focus on main content areas
            css_selector="main, article, .content, .main-content, #content, #main",
            target_elements=[
                ".article-content", ".post-content", ".page-content", 
                ".main-text", ".content-body", ".article-body"
            ],
            
            # Link management
            exclude_external_links=True,
            exclude_social_media_links=True,
            exclude_domains=["google-analytics.com", "facebook.com", "twitter.com"],
            
            # Advanced processing
            markdown_generator=self.markdown_generator,
            extraction_strategy=self.dv_filter_strategy if self.use_llm_filter else None,
            
            # Dynamic content handling
            remove_overlay_elements=True,
            process_iframes=False,  # Skip for speed
            scan_full_page=True,
            
            # No specific wait condition - pages load dynamically
            # wait_for="css:main",
            # wait_for_timeout=5000
        )
    
    def should_crawl_url(self, url: str, domain_info: Dict) -> bool:
        parsed = urlparse(url)
        
        # Check if URL belongs to target domain
        if not parsed.netloc.endswith(domain_info["domain"]):
            return False
        
        # Check excluded paths
        for exclude_path in domain_info["exclude_paths"]:
            if exclude_path in parsed.path:
                return False
        
        # Check for DV-related keywords in URL
        url_lower = url.lower()
        keyword_score = sum(1 for keyword in domain_info["focus_keywords"] if keyword in url_lower)
        
        # Prioritize URLs with DV keywords
        if keyword_score >= 2:  # At least 2 keywords
            return True
        elif keyword_score == 1:
            return True  # Still crawl, but lower priority
        
        # Skip URLs that clearly aren't relevant
        irrelevant_patterns = [
            "careers", "jobs", "recruitment", "tenders", "procurement",
            "news/archive", "events/past", "gallery", "images",
            "contact", "about-us", "privacy", "terms", "cookies"
        ]
        
        for pattern in irrelevant_patterns:
            if pattern in url_lower:
                return False
        
        return True  # Default to crawl if uncertain
    
    async def discover_domain_urls(self, domain_info: Dict) -> List[str]:
        
        print(f"Discovering URLs for {domain_info['domain']} (no artificial limits)...")
        discovered_urls = set()
        urls_to_explore = []  # Queue for breadth-first exploration
        explored_urls = set()  # Track what we've already explored
        
        # Start with prioritized entry points
        entry_points = self._get_prioritized_entry_points(domain_info)
        urls_to_explore.extend(entry_points)
        
        config = self.create_crawl_config(domain_info)
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            
            current_depth = 0
            
            while urls_to_explore and current_depth < domain_info["max_depth"]:
                current_level_urls = urls_to_explore.copy()
                urls_to_explore.clear()
                
                print(f"Exploring depth {current_depth + 1}: {len(current_level_urls)} URLs")
                
                for entry_url in current_level_urls:
                    if entry_url in explored_urls:
                        continue
                    
                    explored_urls.add(entry_url)
                    
                    try:
                        result = await crawler.arun(entry_url, config=config)
                        
                        if result.success and result.links:
                            # Extract internal links
                            internal_links = result.links.get('internal', [])
                            new_urls_found = 0
                            
                            for link_info in internal_links:
                                url = link_info.get('url', '')
                                if (self.should_crawl_url(url, domain_info) and 
                                    url not in discovered_urls and 
                                    url not in explored_urls):
                                    
                                    discovered_urls.add(url)
                                    urls_to_explore.append(url)  # For next depth level
                                    new_urls_found += 1
                            
                            if new_urls_found > 0:
                                print(f"    {entry_url}: Found {new_urls_found} new relevant URLs")
                            
                    except Exception as e:
                        print(f" Error exploring {entry_url}: {e}")
                        continue
                
                current_depth += 1
                print(f"Total discovered so far: {len(discovered_urls)} URLs")
        
        discovered_list = list(discovered_urls)
        print(f"Discovered {len(discovered_list)} URLs for {domain_info['domain']} across {current_depth} depth levels")
        return discovered_list

    def _get_prioritized_entry_points(self, domain_info: Dict) -> List[str]:
        
        base_points = [
            f"https://www.{domain_info['domain']}/",
            f"https://{domain_info['domain']}/",
        ]
        
        # Add keyword-specific high-priority URLs
        if "hse.ie" in domain_info["domain"]:
            base_points.extend([
                "https://www.hse.ie/eng/about/who/primarycare/socialinclusion/other-areas/domestic-violence/",
                "https://www.hse.ie/eng/services/publications/children/",
                "https://www.hse.ie/eng/about/who/acute-hospitals-division/woman-infants/domestic-violence/",
                "https://www2.hse.ie/conditions/",
                "https://www.hse.ie/eng/services/list/1/lho/dublin/dublinsc/our-services/primary-care/social-inclusion/"
            ])
        
        elif "tusla.ie" in domain_info["domain"]:
            base_points.extend([
                "https://www.tusla.ie/services/family-community-support/domestic-sexual-and-gender-based-violence/",
                "https://www.tusla.ie/services/child-protection-welfare/",
                "https://www.tusla.ie/services/family-community-support/",
                "https://www.tusla.ie/uploads/content/Policies_and_Procedures_DV.pdf",
                "https://www.tusla.ie/services/family-community-support/family-support/"
            ])
        
        elif "citizensinformation.ie" in domain_info["domain"]:
            base_points.extend([
                "https://www.citizensinformation.ie/en/justice/victims-of-crime/",
                "https://www.citizensinformation.ie/en/justice/courts-system/",
                "https://www.citizensinformation.ie/en/health/health-services/",
                "https://www.citizensinformation.ie/en/social-welfare/",
                "https://www.citizensinformation.ie/en/housing/"
            ])
        
        return base_points
    
    async def crawl_single_page(self, url: str, domain_info: Dict, config: CrawlerRunConfig) -> Optional[Dict]:
        
        print(f"Crawling: {url}")
        
        try:
            async with AsyncWebCrawler(config=self.browser_config) as crawler:
                result = await crawler.arun(url, config=config)
                
                if not result.success:
                    print(f" Failed: {result.error_message}")
                    return None
                
                # Check content length
                if not result.markdown or len(result.markdown.raw_markdown) < 200:
                    print(f" Skipped: Too little content ({len(result.markdown.raw_markdown) if result.markdown else 0} chars)")
                    return None
                
                # LLM relevance filtering if available
                is_relevant = True
                relevance_data = {}
                
                if self.use_llm_filter and result.extracted_content:
                    try:
                        relevance_data = json.loads(result.extracted_content)
                        is_relevant = (
                            relevance_data.get("is_dv_relevant", False) and 
                            relevance_data.get("relevance_score", 0) >= 6.0  # Threshold for relevance
                        )
                        
                        if not is_relevant:
                            print(f"Skipped: Not DV relevant (score: {relevance_data.get('relevance_score', 0)})")
                            return None
                            
                    except json.JSONDecodeError:
                        print(f"Could not parse LLM relevance data")
                        # Fall back to keyword checking
                        content_lower = result.markdown.raw_markdown.lower()
                        keyword_matches = sum(1 for keyword in domain_info["focus_keywords"] if keyword in content_lower)
                        if keyword_matches < 2:
                            print(f"Skipped: Insufficient keyword matches ({keyword_matches})")
                            return None
                
                # Create content data
                content_data = {
                    "url": url,
                    "organization": domain_info["organization"],
                    "content_type": relevance_data.get("content_type", "support"),
                    "title": result.metadata.get("title", ""),
                    "raw_markdown": result.markdown.raw_markdown,
                    "clean_markdown": result.markdown.fit_markdown or result.markdown.raw_markdown,
                    "relevance_score": relevance_data.get("relevance_score", 5.0),
                    "key_topics": relevance_data.get("key_topics", []),
                    "clean_summary": relevance_data.get("clean_summary", ""),
                    "links_found": len(result.links.get('internal', [])) if result.links else 0,
                    "crawl_timestamp": datetime.now().isoformat(),
                    "success": True
                }
                
                print(f"Success - {len(result.markdown.raw_markdown)} chars, relevance: {content_data['relevance_score']}")
                return content_data
                
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def create_rag_chunks_from_content(self, content_data: Dict) -> List[Dict]:
        
        if not content_data or not content_data.get("success"):
            return []
        
        chunks = []
        
        # Use clean summary if available, otherwise fall back to markdown
        main_content = content_data.get("clean_summary") or content_data["clean_markdown"]
        
        if len(main_content) > 200:  # Only process substantial content
            
            # Create main content chunk
            main_chunk = {
                "content": main_content,
                "title": content_data["title"],
                "organization": content_data["organization"],
                "content_type": content_data["content_type"],
                "source_url": content_data["url"],
                "relevance_score": content_data["relevance_score"],
                "key_topics": content_data.get("key_topics", []),
                "chunk_type": "main_content",
                "crawl_timestamp": content_data["crawl_timestamp"],
                "county": self._extract_county(main_content)
            }
            chunks.append(main_chunk)
            
            # Create focused chunks for key topics if available
            for i, topic in enumerate(content_data.get("key_topics", [])[:3]):  # Max 3 topic chunks
                if len(topic.strip()) > 20:
                    topic_chunk = {
                        "content": f"Irish domestic violence information about {topic}: {main_content[:500]}...",
                        "title": f"{content_data['title']} - {topic}",
                        "organization": content_data["organization"],
                        "content_type": content_data["content_type"],
                        "source_url": content_data["url"],
                        "relevance_score": content_data["relevance_score"],
                        "key_topics": [topic],
                        "chunk_type": "topic_focused",
                        "crawl_timestamp": content_data["crawl_timestamp"],
                        "county": main_chunk["county"]
                    }
                    chunks.append(topic_chunk)
        
        return chunks
    
    def _extract_county(self, text: str) -> str:
        irish_counties = [
            "carlow", "cavan", "clare", "cork", "donegal", "dublin",
            "galway", "kerry", "kildare", "kilkenny", "laois", "leitrim", 
            "limerick", "longford", "louth", "mayo", "meath", "monaghan",
            "offaly", "roscommon", "sligo", "tipperary", "waterford",
            "westmeath", "wexford", "wicklow"
        ]
        
        text_lower = text.lower()
        for county in irish_counties:
            if county in text_lower:
                return county.title()
        
        return "National"
    
    def add_chunks_to_knowledge_base(self, chunks: List[Dict]) -> int:
        
        if not chunks:
            return 0
        
        print(f"Adding {len(chunks)} chunks to knowledge base...")
        
        try:
            collection = self.kb_processor.chroma_client.get_collection("domestic_violence_kb")
        except:
            print("Could not access ChromaDB collection")
            return 0
        
        added_count = 0
        
        for chunk in chunks:
            try:
                # Create unique ID
                chunk_id = f"domain_crawl_{chunk['organization'].lower().replace(' ', '_')}_{hash(chunk['content']) % 100000}"
                
                # Create embedding
                embedding = self.kb_processor.embedding_model.encode(chunk["content"]).tolist()
                
                # Prepare metadata
                metadata = {
                    "organization": chunk["organization"],
                    "content_type": chunk["content_type"],
                    "county": chunk["county"],
                    "source_url": chunk["source_url"],
                    "crawl_timestamp": chunk["crawl_timestamp"],
                    "chunk_type": chunk["chunk_type"],
                    "filename": f"domain_crawl_{chunk['organization'].lower()}",
                    "relevance_score": chunk.get("relevance_score", 5.0),
                    "key_topics": json.dumps(chunk.get("key_topics", []))
                }
                
                # Add to collection
                collection.add(
                    documents=[chunk["content"]],
                    embeddings=[embedding],
                    metadatas=[metadata],
                    ids=[chunk_id]
                )
                
                added_count += 1
                
            except Exception as e:
                print(f"Error adding chunk: {e}")
                continue
        
        print(f"Added {added_count} chunks to knowledge base")
        return added_count
    
    async def crawl_domain(self, domain_info: Dict) -> List[Dict]:
        
        print(f"Starting comprehensive crawl of {domain_info['domain']}")
        print(f"Stopping criteria: {domain_info['max_crawl_hours']}h limit, min relevance {domain_info['min_relevance_score']}, stop after {domain_info['stop_after_consecutive_low_scores']} consecutive low scores")
        print("=" * 80)
        
        start_time = datetime.now()
        max_crawl_seconds = domain_info['max_crawl_hours'] * 3600
        
        # Step 1: Discover URLs (with prioritization)
        discovered_urls = await self.discover_domain_urls(domain_info)
        
        if not discovered_urls:
            print(f"No URLs discovered for {domain_info['domain']}")
            return []
        
        # Step 2: Sort URLs by priority (keyword density, URL structure)
        prioritized_urls = self._prioritize_urls(discovered_urls, domain_info)
        
        # Step 3: Crawl with intelligent stopping
        crawl_config = self.create_crawl_config(domain_info)
        all_content = []
        consecutive_low_scores = 0
        total_crawled = 0
        
        print(f"Starting intelligent crawl of {len(prioritized_urls)} prioritized URLs...")
        
        for url in prioritized_urls:
            # Check time limit
            elapsed_time = (datetime.now() - start_time).total_seconds()
            if elapsed_time > max_crawl_seconds:
                print(f"Time limit reached ({domain_info['max_crawl_hours']}h)")
                break
            
            total_crawled += 1
            remaining_time = (max_crawl_seconds - elapsed_time) / 60  # minutes
            print(f"[{total_crawled}/{len(prioritized_urls)}] ⏱️{remaining_time:.0f}min left ", end="")
            
            # Add polite delay
            if total_crawled > 1:
                await asyncio.sleep(2)
            
            content_data = await self.crawl_single_page(url, domain_info, crawl_config)
            
            if content_data:
                relevance_score = content_data.get('relevance_score', 0)
                
                if relevance_score >= domain_info['min_relevance_score']:
                    all_content.append(content_data)
                    consecutive_low_scores = 0  # Reset counter
                    
                    # Save individual high-quality content
                    safe_filename = re.sub(r'[^\w\-_\.]', '_', content_data.get('title', f'content_{total_crawled}'))
                    filename = self.output_dir / f"{domain_info['organization'].lower()}_{safe_filename[:50]}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(content_data, f, indent=2, ensure_ascii=False)
                    
                    print(f"Added (score: {relevance_score:.1f})")
                else:
                    consecutive_low_scores += 1
                    print(f"Low relevance (score: {relevance_score:.1f}, consecutive: {consecutive_low_scores})")
                    
                    # Check consecutive low scores stopping criterion
                    if consecutive_low_scores >= domain_info['stop_after_consecutive_low_scores']:
                        print(f"Stopping: {consecutive_low_scores} consecutive pages below relevance threshold")
                        break
            else:
                consecutive_low_scores += 1
                print(f"Failed to crawl (consecutive failures: {consecutive_low_scores})")
                
                # Stop if too many consecutive failures
                if consecutive_low_scores >= domain_info['stop_after_consecutive_low_scores']:
                    print(f"Stopping: Too many consecutive failures")
                    break
        
        elapsed_minutes = (datetime.now() - start_time).total_seconds() / 60
        success_rate = (len(all_content) / total_crawled * 100) if total_crawled > 0 else 0
        
        print(f"Intelligent crawl completed for {domain_info['domain']}")
        print(f"Results: {len(all_content)} relevant pages from {total_crawled} crawled ({success_rate:.1f}% success rate)")
        print(f"Time taken: {elapsed_minutes:.1f} minutes")
        
        return all_content

    def _prioritize_urls(self, urls: List[str], domain_info: Dict) -> List[str]:
        
        def calculate_url_priority(url: str) -> float:
            score = 0.0
            url_lower = url.lower()
            
            # Keyword scoring
            for keyword in domain_info['focus_keywords']:
                if keyword in url_lower:
                    score += 2.0  # High value for keywords in URL
            
            # Path depth scoring (shorter paths often more important)
            path_parts = url.split('/')
            if len(path_parts) <= 5:
                score += 1.0  # Bonus for shorter paths
            
            # Specific high-value URL patterns
            high_value_patterns = [
                'domestic-violence', 'safety-order', 'protection', 'support-services',
                'victim-services', 'crisis', 'helpline', 'emergency', 'legal-rights',
                'policies', 'procedures', 'guidelines'
            ]
            
            for pattern in high_value_patterns:
                if pattern in url_lower:
                    score += 3.0  # Very high value for specific DV patterns
            
            # Penalize obviously low-value URLs  
            low_value_patterns = [
                'archive', 'old', 'deprecated', 'temp', 'test', 'admin',
                'login', 'register', 'search', 'sitemap'
            ]
            
            for pattern in low_value_patterns:
                if pattern in url_lower:
                    score -= 5.0
            
            return max(0.0, score)  # Ensure non-negative
        
        # Calculate priorities and sort
        url_priorities = [(url, calculate_url_priority(url)) for url in urls]
        url_priorities.sort(key=lambda x: x[1], reverse=True)  # Sort by priority (highest first)
        
        prioritized_urls = [url for url, priority in url_priorities]
        
        print(f"Prioritized {len(prioritized_urls)} URLs (top 10 priorities: {[p for _, p in url_priorities[:10]]})")
        return prioritized_urls
    
    async def run_comprehensive_crawl(self) -> bool:
        
        print("Comprehensive Domain Crawling for Irish DV Support")
        print("=" * 70)
        
        all_domain_content = []
        all_chunks = []
        
        for domain_info in self.target_domains:
            # Crawl domain
            domain_content = await self.crawl_domain(domain_info)
            all_domain_content.extend(domain_content)
            
            # Convert to RAG chunks
            for content_data in domain_content:
                chunks = self.create_rag_chunks_from_content(content_data)
                all_chunks.extend(chunks)
        
        # Add all chunks to knowledge base
        if all_chunks:
            added_count = self.add_chunks_to_knowledge_base(all_chunks)
            
            # Create summary
            organizations = list(set(c['organization'] for c in all_domain_content))
            avg_relevance = sum(c.get('relevance_score', 5.0) for c in all_domain_content) / len(all_domain_content) if all_domain_content else 0
            
            summary = {
                "crawl_timestamp": datetime.now().isoformat(),
                "browser_used": "firefox",
                "domains_crawled": len(self.target_domains),
                "total_pages_discovered": sum(len(await self.discover_domain_urls(d)) for d in self.target_domains),
                "pages_successfully_crawled": len(all_domain_content),
                "chunks_generated": len(all_chunks),
                "chunks_added_to_kb": added_count,
                "organizations": organizations,
                "average_relevance_score": avg_relevance,
                "llm_filtering_used": self.use_llm_filter,
                "content_summary": {
                    org: len([c for c in all_domain_content if c['organization'] == org])
                    for org in organizations
                }
            }
            
            with open(self.output_dir / "comprehensive_crawl_summary.json", 'w') as f:
                json.dump(summary, f, indent=2)
            
            print(f"Comprehensive Crawl Results:")
            print(f"  Domains crawled: {len(self.target_domains)}")
            print(f"  Pages successfully crawled: {len(all_domain_content)}")
            print(f"  Total chunks generated: {len(all_chunks)}")  
            print(f"  Chunks added to KB: {added_count}")
            print(f"  Average relevance score: {avg_relevance:.1f}/10")
            print(f"  Organizations: {organizations}")
            
            return True
        else:
            print("No relevant content was found across all domains")
            return False

async def main():
    
    print("Testing Firefox Browser Setup...")
    browser_config = BrowserConfig(browser_type="firefox", headless=True, verbose=True)
    
    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun("https://httpbin.org/html")
            if result.success:
                print("Firefox browser working correctly!")
            else:
                print("Browser test failed")
                return
    except Exception as e:
        print(f"Browser setup error: {e}")
        return
    
    print("\n" + "="*70)
    
    # Run comprehensive crawl
    crawler = ComprehensiveDomainCrawler()
    success = await crawler.run_comprehensive_crawl()
    
    if success:
        print("Comprehensive domain crawling completed successfully!")
    else:
        print("Comprehensive domain crawling failed")

if __name__ == "__main__":
    asyncio.run(main())