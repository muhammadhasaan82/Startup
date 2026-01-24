"""
Website scraper for comprehensive data ingestion.
Crawls the entire NexGenTeck website and extracts ALL content for the knowledge base.
This is the ONLY source of information for the chatbot.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Set
from urllib.parse import urljoin, urlparse
import logging
import time

from config import config
from utils import clean_text, chunk_text

logger = logging.getLogger(__name__)


class WebsiteScraper:
    """
    Comprehensive website scraper for building the chatbot's knowledge base.
    Extracts ALL content from the website - this is the source of truth.
    """
    
    def __init__(self, base_url: str = None):
        """
        Initialize the scraper.
        
        Args:
            base_url: Base URL to scrape (defaults to config.WEBSITE_URL)
        """
        self.base_url = base_url or config.WEBSITE_URL
        self.visited_urls: Set[str] = set()
        self.documents: List[Dict[str, str]] = []
        
    def scrape(self, max_pages: int = 100) -> List[Dict[str, str]]:
        """
        Scrape the ENTIRE website and extract ALL content.
        This builds the complete knowledge base for the chatbot.
        
        Args:
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of documents with 'content' and 'metadata' keys
        """
        logger.info(f"Starting comprehensive scrape of {self.base_url}")
        logger.info(f"Will scrape up to {max_pages} pages")
        
        try:
            self._crawl_page(self.base_url, max_pages)
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            # Return fallback content if scraping fails
            if not self.documents:
                return self._get_fallback_content()
        
        logger.info(f"Scraped {len(self.visited_urls)} pages, created {len(self.documents)} documents")
        return self.documents
    
    def _crawl_page(self, url: str, max_pages: int):
        """
        Recursively crawl a page and all its links.
        
        Args:
            url: URL to crawl
            max_pages: Maximum pages remaining
        """
        if len(self.visited_urls) >= max_pages:
            return
        
        # Normalize URL
        url = url.split('#')[0]  # Remove anchors
        url = url.rstrip('/')
        
        if url in self.visited_urls:
            return
        
        # Only crawl pages from the same domain
        if urlparse(url).netloc != urlparse(self.base_url).netloc:
            return
        
        # Skip non-HTML resources
        skip_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.css', '.js', '.ico', '.woff', '.woff2']
        if any(url.lower().endswith(ext) for ext in skip_extensions):
            return
        
        self.visited_urls.add(url)
        logger.info(f"Scraping page {len(self.visited_urls)}/{max_pages}: {url}")
        
        try:
            response = requests.get(url, timeout=15, headers={
                'User-Agent': 'NexGenTeck-Chatbot/1.0 (Knowledge Base Builder)'
            })
            response.raise_for_status()
            
            # Only process HTML content
            content_type = response.headers.get('content-type', '')
            if 'text/html' not in content_type:
                return
                
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Extract ALL content from this page
        self._extract_all_content(soup, url)
        
        # Small delay to be respectful
        time.sleep(0.2)
        
        # Find and crawl ALL internal links
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            self._crawl_page(full_url, max_pages)
    
    def _extract_all_content(self, soup: BeautifulSoup, url: str):
        """
        Extract ALL relevant content from a page.
        This is comprehensive - we want all the website information.
        
        Args:
            soup: BeautifulSoup object
            url: URL of the page
        """
        # Remove elements that don't contain useful content
        for element in soup(['script', 'style', 'noscript', 'iframe']):
            element.decompose()
        
        # Extract page title
        title = soup.find('title')
        title_text = clean_text(title.get_text()) if title else ""
        
        # Extract meta description
        meta_desc = soup.find('meta', {'name': 'description'})
        meta_desc_text = meta_desc.get('content', '') if meta_desc else ''
        
        # Extract all headings
        headings = []
        for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = clean_text(h.get_text())
            if text and len(text) > 2:
                level = h.name  # h1, h2, etc.
                headings.append(f"[{level.upper()}] {text}")
        
        # Extract all paragraphs
        paragraphs = []
        for p in soup.find_all('p'):
            text = clean_text(p.get_text())
            if text and len(text) > 15:  # Skip very short paragraphs
                paragraphs.append(text)
        
        # Extract list items (services, features, benefits, etc.)
        list_items = []
        for li in soup.find_all('li'):
            text = clean_text(li.get_text())
            if text and len(text) > 10:
                list_items.append(f"• {text}")
        
        # Extract spans and divs with substantial text (for modern websites)
        other_content = []
        for elem in soup.find_all(['span', 'div', 'section', 'article']):
            # Only direct text, not nested
            direct_text = elem.find(string=True, recursive=False)
            if direct_text:
                text = clean_text(str(direct_text))
                if text and len(text) > 30:
                    other_content.append(text)
        
        # Extract table content
        tables = []
        for table in soup.find_all('table'):
            rows = []
            for tr in table.find_all('tr'):
                cells = [clean_text(td.get_text()) for td in tr.find_all(['td', 'th'])]
                if cells:
                    rows.append(' | '.join(cells))
            if rows:
                tables.append('\n'.join(rows))
        
        # Build comprehensive document for this page
        content_parts = []
        
        # Page identification
        content_parts.append(f"PAGE: {title_text}")
        content_parts.append(f"URL: {url}")
        
        if meta_desc_text:
            content_parts.append(f"DESCRIPTION: {meta_desc_text}")
        
        # All headings provide structure
        if headings:
            content_parts.append("SECTIONS:")
            content_parts.extend(headings)
        
        # Main content
        if paragraphs:
            content_parts.append("CONTENT:")
            content_parts.extend(paragraphs)
        
        # Lists contain important features/services
        if list_items:
            content_parts.append("FEATURES/ITEMS:")
            content_parts.extend(list_items[:30])  # Limit to prevent too much
        
        # Other content
        if other_content:
            unique_other = list(set(other_content))[:20]
            content_parts.extend(unique_other)
        
        # Tables
        if tables:
            content_parts.append("TABLE DATA:")
            content_parts.extend(tables[:5])
        
        # Combine all content
        full_content = "\n\n".join(content_parts)
        
        if full_content and len(full_content) > 50:
            # Chunk the content for better retrieval
            chunks = chunk_text(full_content, chunk_size=800, overlap=100)
            
            for i, chunk in enumerate(chunks):
                self.documents.append({
                    'content': chunk,
                    'metadata': {
                        'source': url,
                        'title': title_text,
                        'chunk_index': i,
                        'total_chunks': len(chunks)
                    }
                })
    
    def _get_fallback_content(self) -> List[Dict[str, str]]:
        """
        Return fallback content if scraping fails completely.
        This ensures the chatbot has basic knowledge.
        """
        fallback = [
            {
                'content': """PAGE: NexGenTeck - Digital Solutions Company
URL: https://nexgenteck.com

NexGenTeck is a leading technology company specializing in comprehensive digital solutions. 
We help businesses transform and grow through innovative technology.

Our core services include:
• Web Development - Custom websites, web applications, responsive design
• Mobile App Development - iOS and Android apps, cross-platform solutions
• E-commerce Solutions - Online stores, payment integration, inventory management
• SEO Services - Search engine optimization, content strategy, analytics
• Social Media Marketing - Brand management, content creation, advertising
• Blockchain Development - Smart contracts, DeFi solutions, NFT platforms
• Google Ads Management - PPC campaigns, conversion optimization
• Software Development - Custom software, enterprise solutions

We use modern technologies including React, Next.js, TypeScript, Node.js, Python, and more.

Contact us for a free consultation to discuss your project requirements.""",
                'metadata': {'source': 'fallback', 'title': 'About NexGenTeck'}
            },
            {
                'content': """PAGE: Our Services
URL: https://nexgenteck.com/services

WEB DEVELOPMENT
We build modern, responsive websites using the latest technologies. Our web development services include:
• Custom website design and development
• React and Next.js applications
• E-commerce platforms
• Content management systems
• Progressive web apps
• Website maintenance and support

MOBILE APP DEVELOPMENT
Native and cross-platform mobile applications for iOS and Android:
• React Native development
• Flutter applications
• Native iOS (Swift) and Android (Kotlin)
• App store optimization
• Mobile UI/UX design

E-COMMERCE SOLUTIONS
Complete online store solutions:
• Shopify development
• WooCommerce integration
• Custom e-commerce platforms
• Payment gateway integration
• Inventory management systems""",
                'metadata': {'source': 'fallback', 'title': 'Services Overview'}
            },
            {
                'content': """PAGE: Contact NexGenTeck
URL: https://nexgenteck.com/contact

Get in touch with our team for your digital transformation needs.

CONTACT INFORMATION:
• Email: info@nexgenteck.com
• Phone: Available on request
• Location: Serving clients globally

HOW WE WORK:
1. Initial Consultation - We discuss your requirements and goals
2. Proposal & Planning - Detailed project plan and timeline
3. Development - Agile development with regular updates
4. Testing & QA - Thorough testing before launch
5. Launch & Support - Deployment and ongoing maintenance

We offer competitive pricing and flexible engagement models.
Contact us today for a free consultation!""",
                'metadata': {'source': 'fallback', 'title': 'Contact Information'}
            }
        ]
        
        logger.info("Using fallback content")
        return fallback
