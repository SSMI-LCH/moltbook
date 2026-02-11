#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Moltbook Crawler
Crawls content from https://www.moltbook.com/ specifically targeting elements with class 'animate-fadeIn'.
"""

import time
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TARGET_URL = "https://www.moltbook.com/"

def build_driver(headless: bool = True, window_size: str = "1920,1080") -> webdriver.Chrome:
    """
    Builds and returns a Chrome WebDriver instance.
    """
    opts = ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")

    opts.add_argument(f"--window-size={window_size}")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--lang=ko-KR")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=opts)

    # Mitigate potential automation detection
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"},
    )
    return driver

def crawl_moltbook(headless: bool = True) -> List[Dict[str, str]]:
    """
    Crawls moltbook.com for elements with class 'animate-fadeIn'.
    Returns a list of dictionaries containing the text and outerHTML of found elements.
    """
    driver = None
    items = []
    try:
        driver = build_driver(headless=headless)
        driver.get(TARGET_URL)

        # Wait for the page to load and at least one target element to be present
        # Wait for the page to load and at least one target element to be present
        # User requested: class="flex-1 min-w-0"
        target_css = ".flex-1.min-w-0"
        wait = WebDriverWait(driver, 15)
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, target_css)))
            # Brief sleep to allow for dynamic content to settle
            time.sleep(3) 
        except Exception as e:
            print(f"Warning: Timeout waiting for target elements. {e}")

        elements = driver.find_elements(By.CSS_SELECTOR, target_css)

        for idx, elem in enumerate(elements):
            try:
                title_elem = elem.find_element(By.TAG_NAME, "h3")
                title = title_elem.text.strip()
            except:
                title = "No Title"

            try:
                desc_elem = elem.find_element(By.TAG_NAME, "p")
                description = desc_elem.text.strip()
            except:
                description = "No Description"

            if title or description:
                items.append({
                    "id": idx,
                    "title": title,
                    "description": description,
                    "text": elem.text.strip(), # Keep full text just in case
                    "html": elem.get_attribute("outerHTML")
                })
        
        return items

    except Exception as e:
        print(f"Error during crawling: {e}")
        return []
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    # Test execution
    data = crawl_moltbook(headless=False)
    print(f"Crawled {len(data)} items.")
    for item in data[:3]:
        print(f"- {item['text'][:50]}...")
