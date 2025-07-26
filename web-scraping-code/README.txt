# 🧭 Advanced Web Scraping: Extracting WSJ Headlines Using Edge and Playwright

This Python script automates the extraction of news headlines from the Wall Street Journal by controlling Microsoft Edge using CDP (Chrome DevTools Protocol) and Playwright.

## 📦 Requirements
- Python 3.9+
- Microsoft Edge installed
- Playwright installed (`pip install playwright && playwright install`)

## ▶️ How It Works
1. Launches Edge in remote debug mode
2. Connects to the browser via CDP
3. Navigates to Bing and searches for WSJ
4. Finds and clicks on the correct WSJ link
5. Opens the page in a new tab
6. Automatically scrolls the WSJ homepage
7. Extracts and prints article titles

## 💻 Main Functions
- `attendi_link_wsj`: Searches Bing results for a link to WSJ
- `estrai_titoli_durante_scroll`: Scrolls the WSJ page and extracts headline text using known tag/class patterns

## 💖 Support This Project
Enjoy this script? Consider supporting:
- [PayPal](https://www.paypal.me/YOURNAME)
- [Patreon](https://www.patreon.com/YOURNAME)


line by line code explanation:

import asyncio                    # Enables asynchronous programming
import subprocess              # Launches Edge browser in debug mode
import time                          # Provides delay/sleep functionalities
from playwright.async_api import async_playwright  # Core Playwright async API

EDGE_PATH = r"...msedge.exe"            # Full path to Edge browser executable
DEBUG_PORT = 9222                               # Port for remote debugging via CDP
USER_DATA_DIR = r"...debug-profile" # Custom browser user profile path

BING_URL = "https://www.bing.com"                 # Bing search page
SEARCH_QUERY = "https://www.wsj.com"        # Target site

CLASSES = [...]     # List of HTML classes possibly containing headlines
TAGS = [...]           # HTML tags where text headlines are commonly nested


Scrolls the page and extracts headlines using tag/class combinations.

titoli = set()                             # Stores unique headlines
posizione_precedente = -1   # Used to detect end-of-scroll

Loops over tag/class combinations:

for tag in TAGS:
    for classe in CLASSES:
        selettore = f"{tag}.{classe.replace(' ', '.')}"  # Format CSS selector
        elementi = await page.query_selector_all(selettore)

Extract text if it exists:

for el in elementi:
    try:
        testo = await el.inner_text()      # Extracts inner text
        testo = testo.strip()                     # Removes extra spaces
        if testo and testo not in titoli:
            titoli.add(testo)
            print(f"📰 {testo}")                # Print the headline

Scroll the page and check position:

await page.mouse.wheel(0, 1000)             # Scrolls down
await asyncio.sleep(2)                                  # Wait for content to load

Detect bottom of page:

posizione_attuale = await page.evaluate(...)
altezza_massima = await page.evaluate(...)
if posizione_attuale >= altezza_massima or posizione_attuale == posizione_precedente:
    break

await page.wait_for_selector(".b_algo")      # Wait for search results


Search all links for "wsj.com":

links = await page.query_selector_all("a")
for link in links:
    href = await link.get_attribute("href")
    testo = await link.inner_text()
    if "wsj.com" in href.lower() and "wall street" in testo.lower():
        return link    # Return the correct result

---------------------------------------------------------------------------------

main()
Coordinates everything.

Launch Edge:

subprocess.Popen([
    EDGE_PATH,
    f"--remote-debugging-port={DEBUG_PORT}",
    f"--user-data-dir={USER_DATA_DIR}"
])
time.sleep(8)    # Wait for browser to be ready

Connect to browser via CDP:

browser = await pw.chromium.connect_over_cdp(...)


Create context and page:

context = browser.contexts[0] or await browser.new_context()
page = await context.new_page()

Open Bing and enter query:

await page.goto(BING_URL)
await page.fill("textarea#sb_form_q", SEARCH_QUERY)
await page.keyboard.press("Enter")

Wait for and click WSJ link:

wsj_link = await attendi_link_wsj(page)
await wsj_link.click()

Open new tab:

new_tab_promise = context.wait_for_event("page")
wsj_page = await new_tab_promise


Extract headlines:

await wsj_page.wait_for_load_state("networkidle")
await estrai_titoli_durante_scroll(wsj_page)

Keep browser open:

while True:
    await asyncio.sleep(3600)    # Prevent browser from closing




































