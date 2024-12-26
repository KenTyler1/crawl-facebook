# import pandas as pd
# import json

# # Đường dẫn file JSON và Excel
# json_file_path = "D:/trainning/facebookData.json"
# excel_file_path = "D:/trainning/Tracking GROW - GT NCC RETAILER RECCO PROGRAM - @20241016 (1).xlsx"

# # Đọc dữ liệu từ file JSON
# try:
#     with open(json_file_path, 'r', encoding='utf-8') as json_file:
#         json_data = json.load(json_file)
#         print("Dữ liệu JSON cần mapping:")
#         for entry in json_data:
#             print(json.dumps(entry, indent=4, ensure_ascii=False))
# except FileNotFoundError:
#     print(f"Không tìm thấy file JSON tại {json_file_path}.")
#     exit()

# # Đọc dữ liệu từ sheet "tracking poster", bỏ qua 3 dòng đầu
# try:
#     urls_df = pd.read_excel(excel_file_path, sheet_name="tracking poster", engine='openpyxl', skiprows=3)
# except FileNotFoundError:
#     print(f"Không tìm thấy file Excel tại {excel_file_path}.")
#     exit()
# except ValueError as e:
#     print(f"Lỗi khi đọc file Excel: {e}")
#     exit()

# # Thiết lập lại tên cột
# urls_df.columns = ["Type Store", "Shop Code", "Shop Name", "Shop Address", "District", "Province", "Sub Region", "Link bài post", "Likes", "Comments", "Shared"]

# # In dữ liệu trước khi cập nhật
# print("\nDữ liệu trước khi cập nhật:")
# print(urls_df[["Link bài post", "Likes", "Comments", "Shared"]].head())

# # Lấy dữ liệu từ JSON để thêm vào Excel
# likes_list = []
# comments_list = []
# shared_list = []

# for entry in json_data:
#     for post in entry["data"]:
#         likes_list.append(post.get("likes", 0))
#         comments_list.append(post.get("commentsCount", 0))
#         shared_list.append(post.get("shares", 0))

# # Đảm bảo số lượng dữ liệu khớp với số dòng trong Excel
# rows_count = len(urls_df)
# likes_list = (likes_list + [None] * rows_count)[:rows_count]
# comments_list = (comments_list + [None] * rows_count)[:rows_count]
# shared_list = (shared_list + [None] * rows_count)[:rows_count]

# # Gán dữ liệu vào DataFrame
# urls_df["Likes"] = likes_list
# urls_df["Comments"] = comments_list
# urls_df["Shared"] = shared_list

# # In dữ liệu sau khi cập nhật
# print("\nDữ liệu sau khi cập nhật:")
# print(urls_df[["Link bài post", "Likes", "Comments", "Shared"]].head())

# # Ghi lại vào file Excel
# try:
#     with pd.ExcelWriter(excel_file_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
#         urls_df.to_excel(writer, sheet_name="tracking poster", index=False)
#     print(f"Dữ liệu đã được cập nhật trong sheet 'tracking poster' của file Excel: {excel_file_path}")
# except PermissionError:
#     print("Không thể ghi vào file Excel. Hãy đảm bảo file không được mở bởi ứng dụng khác.")
#     print("Thay vào đó, ghi vào file mới...")

# import pandas as pd
# import json

# # Đường dẫn file JSON và Excel
# json_file_path = 'facebooks_scraped_data.json'  # Đường dẫn file JSON
# excel_file = "D:/trainning/Route plan - PND retailer recco - NW Store List_MB @241016.xlsx"  # Đường dẫn file Excel
# output_excel_file = "Updated_Route plan - PND retailer recco - NW Store List_MB @241016.xlsx"  # File Excel lưu

# # Đọc file JSON
# def read_json(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         data = []
#         for line in file:
#             try:
#                 cleaned_line = line.strip().rstrip(',')
#                 if cleaned_line:
#                     data.append(json.loads(cleaned_line))
#             except json.JSONDecodeError as e:
#                 print(f"JSON decode error: {e}")
#         return data

# # Đọc dữ liệu từ JSON
# json_data = read_json(json_file_path)

# # Đọc file Excel
# urls_df = pd.read_excel(excel_file, sheet_name="Tracking 3 Brand", engine='openpyxl')

# # Xử lý dữ liệu: Ánh xạ các trường từ JSON với các URL trong Excel
# for data in json_data:
#     url = data.get("url")
#     likes = data.get("likes", 0)
#     shares = data.get("shares", 0)
#     comments = data.get("comments", 0)

#     # Tìm dòng tương ứng trong file Excel
#     row_index = urls_df[urls_df["LINK FB"] == url].index

#     if not row_index.empty:
#         # Nếu URL đã tồn tại, cập nhật dữ liệu
#         urls_df.loc[row_index, "LIKE2"] = likes
#         urls_df.loc[row_index, "Share3"] = shares
#         urls_df.loc[row_index, "Comment4"] = comments
#     else:
#         # Nếu URL chưa tồn tại, thêm dòng mới
#         new_row = {"URL": url, "LIKE2": likes, "Share3": shares, "Comment4": comments}
#         urls_df = pd.concat([urls_df, pd.DataFrame([new_row])], ignore_index=True)

# # Lưu file Excel sau khi cập nhật
# urls_df.to_excel(output_excel_file, index=False, engine='openpyxl')

# print(f"Dữ liệu đã được cập nhật và lưu tại: {output_excel_file}")


import pandas as pd
import json

# Đường dẫn file Excel và file JSON
excel_file = "D:/trainning/Engegamet 22.11.xlsx"
json_file = "facebook_results.json"
output_file = "D:/trainning/Engegamet_Updated.xlsx"

# Đọc dữ liệu từ file JSON
with open(json_file, "r", encoding="utf-8") as f:
    json_data = json.load(f)

# Chuyển JSON thành DataFrame
json_df = pd.DataFrame(json_data[:-1])  # Bỏ phần summary cuối cùng nếu có

# Đọc dữ liệu từ file Excel
excel_df = pd.read_excel(excel_file, sheet_name="Engegament_Post", engine="openpyxl")

# Đổi tên cột để dễ làm việc
excel_df.columns = ["STT", "Sub Region", "REGION", "No. MVB/MVB", "Cột2", "Store Name", "Province", "LINK FB",
                    "Link bài post", "LIKE", "Share", "Comment"]

# Cập nhật cột LIKE, Share, Comment dựa trên Link bài post
for index, row in excel_df.iterrows():
    matching_row = json_df[json_df["url"] == row["Link bài post"]]
    if not matching_row.empty:
        excel_df.at[index, "LIKE"] = matching_row.iloc[0]["likes"]
        excel_df.at[index, "Share"] = matching_row.iloc[0]["shares"]
        excel_df.at[index, "Comment"] = matching_row.iloc[0]["comments"]

# Lưu lại file Excel đã cập nhật
excel_df.to_excel(output_file, sheet_name="Engegament_Post", index=False)

print(f"Dữ liệu đã được cập nhật và lưu tại: {output_file}")
