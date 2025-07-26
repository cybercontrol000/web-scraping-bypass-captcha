**# 🧭 Advanced Web Scraping: Extracting WSJ Headlines Using Edge and Playwright**



**This Python script automates the extraction of news headlines from the Wall Street Journal by controlling Microsoft Edge using CDP (Chrome DevTools Protocol) and Playwright.**



**## 📦 Requirements**

**- Python 3.9+**

**- Microsoft Edge installed or modify it to use chrome and other browsers**

**- Playwright installed (`pip install playwright \&\& playwright install`)**



**## ▶️ How It Works**

**1. Launches Edge in remote debug mode**

**2. Connects to the browser via CDP**

**3. Navigates to Bing and searches for WSJ**

**4. Finds and clicks on the correct WSJ link**

**5. Opens the page in a new tab**

**6. Automatically scrolls the WSJ homepage**

**7. Extracts and prints article titles**



**## 💻 Main Functions**

**- `attendi\_link\_wsj`: Searches Bing results for a link to WSJ**

**- `estrai\_titoli\_durante\_scroll`: Scrolls the WSJ page and extracts headline text using known tag/class patterns**



**## 💖 Support This Project**

**Enjoy this script? Consider supporting:**

**- \[PayPal](https://www.paypal.me/YOURNAME)**

**- \[Patreon](https://www.patreon.com/YOURNAME)**



**--------------------------------------------------------------------------------------------**



##### line by line code explanation:



**import asyncio                    # Enables asynchronous programming**

**import subprocess              # Launches Edge browser in debug mode**

**import time                          # Provides delay/sleep functionalities**

**from playwright.async\_api import async\_playwright  # Core Playwright async API**



**EDGE\_PATH = r"...msedge.exe"            # Full path to Edge browser executable**

**DEBUG\_PORT = 9222                               # Port for remote debugging via CDP**

**USER\_DATA\_DIR = r"...debug-profile" # Custom browser user profile path**



**BING\_URL = "https://www.bing.com"                 # Bing search page**

**SEARCH\_QUERY = "https://www.wsj.com"        # Target site**



**CLASSES = \[...]     # List of HTML classes possibly containing headlines**

**TAGS = \[...]           # HTML tags where text headlines are commonly nested**





**Scrolls the page and extracts headlines using tag/class combinations.**



**titoli = set()                             # Stores unique headlines**

**posizione\_precedente = -1   # Used to detect end-of-scroll**



**Loops over tag/class combinations:**



**for tag in TAGS:**

    **for classe in CLASSES:**

        **selettore = f"{tag}.{classe.replace(' ', '.')}"  # Format CSS selector**

        **elementi = await page.query\_selector\_all(selettore)**



**Extract text if it exists:**



**for el in elementi:**

    **try:**

        **testo = await el.inner\_text()      # Extracts inner text**

        **testo = testo.strip()                     # Removes extra spaces**

        **if testo and testo not in titoli:**

            **titoli.add(testo)**

            **print(f"📰 {testo}")                # Print the headline**



**Scroll the page and check position:**



**await page.mouse.wheel(0, 1000)             # Scrolls down**

**await asyncio.sleep(2)                                  # Wait for content to load**



**Detect bottom of page:**



**posizione\_attuale = await page.evaluate(...)**

**altezza\_massima = await page.evaluate(...)**

**if posizione\_attuale >= altezza\_massima or posizione\_attuale == posizione\_precedente:**

    **break**



**await page.wait\_for\_selector(".b\_algo")      # Wait for search results**





**Search all links for "wsj.com":**



**links = await page.query\_selector\_all("a")**

**for link in links:**

    **href = await link.get\_attribute("href")**

    **testo = await link.inner\_text()**

    **if "wsj.com" in href.lower() and "wall street" in testo.lower():**

        **return link    # Return the correct result**



**---------------------------------------------------------------------------------**



**main()**

**Coordinates everything.**



**Launch Edge:**



**subprocess.Popen(\[**

    **EDGE\_PATH,**

    **f"--remote-debugging-port={DEBUG\_PORT}",**

    **f"--user-data-dir={USER\_DATA\_DIR}"**

**])**

**time.sleep(8)    # Wait for browser to be ready**



**Connect to browser via CDP:**



**browser = await pw.chromium.connect\_over\_cdp(...)**





**Create context and page:**



**context = browser.contexts\[0] or await browser.new\_context()**

**page = await context.new\_page()**



**Open Bing and enter query:**



**await page.goto(BING\_URL)**

**await page.fill("textarea#sb\_form\_q", SEARCH\_QUERY)**

**await page.keyboard.press("Enter")**



**Wait for and click WSJ link:**



**wsj\_link = await attendi\_link\_wsj(page)**

**await wsj\_link.click()**



**Open new tab:**



**new\_tab\_promise = context.wait\_for\_event("page")**

**wsj\_page = await new\_tab\_promise**





**Extract headlines:**



**await wsj\_page.wait\_for\_load\_state("networkidle")**

**await estrai\_titoli\_durante\_scroll(wsj\_page)**



**Keep browser open:**



**while True:**

    **await asyncio.sleep(3600)    # Prevent browser from closing**











































































