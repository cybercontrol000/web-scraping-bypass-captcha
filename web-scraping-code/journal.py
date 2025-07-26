import asyncio
import subprocess
import time
from playwright.async_api import async_playwright

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
DEBUG_PORT = 9222
USER_DATA_DIR = r"C:\msedge-debug-profile"

BING_URL = "https://www.bing.com"
SEARCH_QUERY = "https://www.wsj.com"

CLASSES = [
    "headline-text", "contain-headline-text", "container__headline-text",
    "has-text-black", "aprev-title", "entry__title", "title",
    "e1sf124z8 css-b4ychf-HeadlineTextBlock", "e1sf124z8 css-k3sea5n-HeadlineTextBlock",
    "e1sf124z8 css-1qw2665-HeadlineTextBlock", "e1sf124z8 css-1bx5v3n-HeadlineTextBlock",
    "e1sf124z8 css-19935vf-HeadlineTextBlock", "css-ot5prs-Headline eyvddzz6"
]

TAGS = ["h2", "h3", "a", "li", "h4", "div", "span"]

async def estrai_titoli_durante_scroll(page):
    titoli = set()
    print("📖 Estrazione titoli in corso durante lo scroll...")

    posizione_precedente = -1

    while True:
        # Estrazione prima dello scroll (in caso ci siano già nuovi elementi caricati)
        for tag in TAGS:
            for classe in CLASSES:
                selettore = f"{tag}.{classe.replace(' ', '.')}"
                elementi = await page.query_selector_all(selettore)
                for el in elementi:
                    try:
                        testo = await el.inner_text()
                        testo = testo.strip()
                        if testo and testo not in titoli:
                            titoli.add(testo)
                            print(f"📰 {testo}")
                    except:
                        continue

        # Scroll della pagina
        await page.mouse.wheel(0, 1000)
        await asyncio.sleep(2)

        # Controllo se siamo arrivati in fondo
        posizione_attuale = await page.evaluate("window.scrollY")
        altezza_massima = await page.evaluate("document.body.scrollHeight - window.innerHeight")
        if posizione_attuale >= altezza_massima or posizione_attuale == posizione_precedente:
            break
        posizione_precedente = posizione_attuale

    print(f"\n✅ Estrazione completata. Titoli trovati: {len(titoli)}")

async def attendi_link_wsj(page, timeout=20):
    print("🔎 Cerco link WSJ...")

    try:
        await page.wait_for_selector(".b_algo", timeout=10000)
    except:
        print("❌ Bing non ha caricato i risultati.")
        return None

    start = time.time()
    while time.time() - start < timeout:
        links = await page.query_selector_all("a")
        for link in links:
            href = await link.get_attribute("href") or ""
            testo = await link.inner_text() or ""
            if "wsj.com" in href.lower() and "wall street" in testo.lower():
                print(f"🔗 Trovato: {testo.strip()} ({href[:60]})")
                return link
        await asyncio.sleep(1)

    return None

async def main():
    print("🚀 Avvio Edge con profilo debug...")
    subprocess.Popen([
        EDGE_PATH,
        f"--remote-debugging-port={DEBUG_PORT}",
        f"--user-data-dir={USER_DATA_DIR}"
    ])
    print("🕓 Attendo il browser...")
    time.sleep(8)

    async with async_playwright() as pw:
        browser = None
        for _ in range(5):
            try:
                browser = await pw.chromium.connect_over_cdp(f"http://127.0.0.1:{DEBUG_PORT}")
                break
            except:
                print("⏳ Ritento connessione a Edge...")
                time.sleep(2)

        if not browser:
            print("❌ Impossibile connettersi al browser.")
            return

        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await context.new_page()

        await page.goto(BING_URL, wait_until="networkidle")
        print(f"⌨️ Digito query '{SEARCH_QUERY}'...")
        await page.fill("textarea#sb_form_q", SEARCH_QUERY)
        await page.keyboard.press("Enter")

        wsj_link = await attendi_link_wsj(page)
        if not wsj_link:
            print("❌ Nessun link WSJ trovato.")
            return

        await wsj_link.scroll_into_view_if_needed()
        box = await wsj_link.bounding_box()
        if box:
            await page.mouse.move(box["x"] + 5, box["y"] + 5)
            await asyncio.sleep(1)

        new_tab_promise = context.wait_for_event("page")
        await wsj_link.click()
        wsj_page = await new_tab_promise

        await wsj_page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)

        await estrai_titoli_durante_scroll(wsj_page)

        print("\n🎉 Fine! Browser lasciato aperto per eventuali controlli manuali.")
        print("💤 Premi CTRL+C per terminare manualmente lo script.")
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
