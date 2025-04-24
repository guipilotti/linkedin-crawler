
import time
import os
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Configurações
li_at = os.environ.get("LI_AT")
spreadsheet_name = "Linkedin_Assistant"
sheet_name = "PostsFeed"
linkedin_url = "https://www.linkedin.com/search/results/content/?keywords=intelig%C3%AAncia%20artificial%20OR%20produto%20OR%20tecnologia&network=%5B%22F%22%5D&sortBy=%22date_posted%22"

# Setup do navegador headless
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("https://www.linkedin.com")
driver.add_cookie({"name": "li_at", "value": li_at, "domain": ".linkedin.com"})
driver.get(linkedin_url)
time.sleep(5)

# Scroll
for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

posts_data = []
posts = driver.find_elements(By.CLASS_NAME, "update-components-text")

for post in posts:
    try:
        texto = post.text.strip()
        if texto and len(texto) > 30:
            parent = post.find_element(By.XPATH, "..")
            link = parent.get_attribute("href") or ""
            autor = parent.get_attribute("aria-label") or ""
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            posts_data.append((texto, link, autor, timestamp))
    except:
        continue

driver.quit()

# Conecta à planilha
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open(spreadsheet_name).worksheet(sheet_name)
dados_existentes = sheet.col_values(1)

# Insere apenas novos posts
for texto, link, autor, data in posts_data:
    if texto not in dados_existentes:
        sheet.append_row([texto, link, autor, data, "Novo"])
        print(f"[✔] Post adicionado: {texto[:50]}...")

print("✅ Crawler finalizado.")
