import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import random

chrome_profile_path = "C:/Users/tonyk/AppData/Local/Google/Chrome/User Data"
profile_directory = "Default"  

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={chrome_profile_path}")
options.add_argument(f"--profile-directory={profile_directory}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")
options.add_argument("--headless")  # Chạy không giao diện
options.add_argument("--disable-gpu")  # Tắt GPU (tùy chọn)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

excel_file = "D:/trainning/Engegamet 22.11.xlsx" 
urls_df = pd.read_excel(excel_file, sheet_name="Engegament_Post", engine='openpyxl')

urls_df.columns = ["STT", "Sub Region", "REGION", "No. MVB/MVB", "Cột2", "Store Name", "Province", "LINK FB", "Link bài post", "LIKE", "Share", "Comment"]

urls = urls_df["Link bài post"].dropna().tolist()

all_results = []

def scroll_down(driver, pause_time=1, max_scrolls=3):
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        current_scroll_position = driver.execute_script("return window.pageYOffset + window.innerHeight")
        if current_scroll_position >= new_height:
            break

def get_likes():
    total_likes = 0
    try:
        likes_elements = driver.execute_script("""
            return Array.from(document.querySelectorAll('span.x1e558r4'))
                        .filter(el => el.classList.length === 1);
        """)
        for elem in likes_elements:
            likes_text = elem.text
            if likes_text.isdigit():
                total_likes += int(likes_text)
        print(f"Total likes found: {total_likes}")
        return total_likes
    except Exception as e:
        print("Error fetching likes:", e)
        return 0

def get_engagement_counts():
    try:
        likes = get_likes()  # Gọi hàm để lấy likes

        all_spans = driver.find_elements(By.CSS_SELECTOR, "span.html-span.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1hl2dhg.x16tdsg8.x1vvkbs.x1sur9pj.xkrqix3")
        
        total_comments = 0
        total_shares = 0

        print(f"Tìm thấy {len(all_spans)} thẻ span.")  # Log tổng số thẻ

        for span in all_spans:
            span_text = span.text.strip()  # Lấy nội dung văn bản của span
            print(f"Đang xử lý thẻ span: '{span_text}'")  # Log nội dung

            if "bình luận" or "comment" or "comments" in span_text:
                try:
                    comment_count = int(span_text.split()[0].replace(",", ""))
                    total_comments += comment_count
                    print(f"  -> Thêm {comment_count} vào total_comments. Tổng hiện tại: {total_comments}")
                except ValueError:
                    print(f"Lỗi parse comment_count: {span_text}")

            elif "chia sẻ" or "share" or "shares" in span_text:
                try:
                    share_count = int(span_text.split()[0].replace(",", ""))
                    total_shares += share_count
                    print(f"  -> Thêm {share_count} vào total_shares. Tổng hiện tại: {total_shares}")
                except ValueError:
                    print(f"Lỗi parse share_count: {span_text}")

        return likes, total_comments, total_shares

    except Exception as e:
        print("Error fetching engagement counts:", e)
        return 0, 0, 0

def save_to_json(data, filename="facebook_results.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

for idx, url in enumerate(urls):
    print(f"Scraping {idx + 1}/{len(urls)}: {url}")
    try:
        driver.get(url)
        time.sleep(5)
        scroll_down(driver)

        # Lấy dữ liệu engagement
        likes, comments, shares = get_engagement_counts()
        result = {
            "url": url,
            "likes": likes,
            "comments": comments,
            "shares": shares,
        }
        all_results.append(result)

        print(f"  -> Comments: {comments}, Shares: {shares}")
    except Exception as e:
        print(f"Lỗi khi scrape {url}: {e}")

# Tính tổng cộng
total_comments = sum([r["comments"] for r in all_results])
total_shares = sum([r["shares"] for r in all_results])

summary = {
    "total_comments": total_comments,
    "total_shares": total_shares,
}

# Lưu kết quả và tổng cộng vào JSON
all_results.append({"summary": summary})
save_to_json(all_results)

# Đóng trình điều khiển
driver.quit()
print(f"Scraping hoàn tất! Tổng bình luận: {total_comments}, Tổng chia sẻ: {total_shares}")
# 12 698