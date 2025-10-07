from playwright.sync_api import sync_playwright

with sync_playwright() as p:
  browser = p.firefox.launch(headless=False)
  page = browser.new_page()

  page.goto("https://ebible.org/cbk/MAT01.htm")
  page.wait_for_selector("ul.tnav")

  with open("data/raw/chavacano/bible.txt", "w", encoding="utf-8") as f:
    while True:
      book = page.locator(
        "xpath=/html/body/ul[contains(concat(' ', normalize-space(@class), ' '),' tnav ')]/li[1]/a"
      ).text_content()

      chapter = page.locator(
        "xpath=/html/body/ul[contains(concat(' ', normalize-space(@class), ' '),' tnav ')]/li[3]/a"
      ).text_content()

      body = page.locator(
        "xpath=/html/body//div[contains(concat(' ', normalize-space(@class), ' '),' main ')]"
      ).text_content()

      next_page_btn = page.locator(
        "xpath=/html/body/ul[contains(concat(' ', normalize-space(@class), ' '),' tnav ')]/li[4]/a"
      )

      f.write(f"{book} {chapter}\n")
      f.write(f"{body}\n")

      if book == "El Revelacion" and chapter == "22":
        break

      if not next_page_btn or not next_page_btn.is_visible():
        break

      next_page_btn.click()
      page.wait_for_selector("ul.tnav")

    browser.close()
  print("Scraped chavacano ✓")