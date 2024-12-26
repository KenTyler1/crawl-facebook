import os
import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_profile_path = "C:/Users/tonyk/AppData/Local/Google/Chrome/User Data"
profile_directory = "Default"  

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={chrome_profile_path}")
options.add_argument(f"--profile-directory={profile_directory}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

excel_file = "D:/trainning/Route plan - PND retailer recco - NW Store List_MB @241016.xlsx"
urls_df = pd.read_excel(excel_file, sheet_name="Tracking 3 Brand", engine='openpyxl')

urls_df.columns = ["STT", "Sub Region", "REGION", "No. MVB/MVB", "Cột2", "Store Name", "Province", "DSM", "SR", "FB link", "Note", "Đủ/Chưa đủ điều kiện", "Tình trạng hợp đồng", "Send Poster Check", "Status", "LINK FB", "LIKE2", "Share3", "Comment4", "Link bài post", "LIKE", "Share", "Comment", "Column3", "Column4", "Column5"]

urls = urls_df["LINK FB"].dropna().tolist()

output_file = "single.json"

if not os.path.exists(output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("")

def parse_number(value):
    """
    Chuyển đổi chuỗi dạng '1,3K', '13K', hoặc '2,5M' thành số nguyên.
    """
    try:
        if "K" in value:
            return int(float(value.replace("K", "").replace(",", ".")) * 1000)
        elif "M" in value:
            return int(float(value.replace("M", "").replace(",", ".")) * 1000000)
        else:
            return int(value.replace(",", ""))
    except ValueError:
        return 0
    
def scroll_down(driver, pause_time=3, max_scrolls=50, scroll_step=500):
    """
    Cuộn trang để tải thêm nội dung.
    
    :param driver: Trình điều khiển Selenium.
    :param pause_time: Thời gian dừng giữa mỗi lần cuộn.
    :param max_scrolls: Số lần cuộn tối đa.
    :param scroll_step: Khoảng cách cuộn (đơn vị: pixel).
    """
    for _ in range(max_scrolls):
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        time.sleep(pause_time)  

        new_height = driver.execute_script("return document.body.scrollHeight")
        current_scroll_position = driver.execute_script("return window.pageYOffset + window.innerHeight")
        
        if current_scroll_position >= new_height:
            break

def scrape_facebook_post(url):
    try:
        driver.get(url)
        time.sleep(5)  

        scroll_down(driver)

        like_spans = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.x1e558r4"))
        )
        
        total_likes = 0
        for span in like_spans:
            like_count = parse_number(span.text.strip())  
            total_likes += like_count

        all_spans = driver.find_elements(By.CSS_SELECTOR, "span.html-span.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1hl2dhg.x16tdsg8.x1vvkbs.x1sur9pj.xkrqix3")
        
        total_comments = 0
        total_shares = 0


        print(f"Tìm thấy {len(all_spans)} thẻ span.")  # Log tổng số thẻ

        for span in all_spans:
            span_text = span.text.strip()  # Lấy nội dung văn bản của span
            print(f"Đang xử lý thẻ span: '{span_text}'")  # Log nội dung

            if "bình luận" in span_text:
                try:
                    comment_count = int(span_text.split()[0].replace(",", ""))
                    total_comments += comment_count
                    print(f"  -> Thêm {comment_count} vào total_comments. Tổng hiện tại: {total_comments}")
                except ValueError:
                    print(f"Lỗi parse comment_count: {span_text}")

            elif "chia sẻ" in span_text:
                try:
                    share_count = int(span_text.split()[0].replace(",", ""))
                    total_shares += share_count
                    print(f"  -> Thêm {share_count} vào total_shares. Tổng hiện tại: {total_shares}")
                except ValueError:
                    print(f"Lỗi parse share_count: {span_text}")
                    
        return {
            "url": url,
            "likes": total_likes,
            "comments": total_comments,
            "shares": total_shares,
        }
    except Exception as e:
        print(f"Lỗi khi scrape {url}: {e}")
        return {"url": url, "likes": 0, "comments": 0, "shares": 0}

all_results = []

for idx, url in enumerate(urls):
    print(f"Scraping {idx + 1}/{len(urls)}: {url}")
    result = scrape_facebook_post(url)
    all_results.append(result) 

    with open(output_file, "a", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)
        f.write(",\n")

total_likes = sum(item["likes"] for item in all_results)
total_comments = sum(item["comments"] for item in all_results)
total_shares = sum(item["shares"] for item in all_results)

with open(output_file, "a", encoding="utf-8") as f:
    summary = {
        "total_likes": total_likes,
        "total_comments": total_comments,
        "total_shares": total_shares,
    }
    json.dump(summary, f, ensure_ascii=False)
    f.write("\n")  

driver.quit()
print(f"Scraping hoàn tất! Tổng kết: {summary}")