import json

def read_json(file_path):
    """Đọc dữ liệu từ file JSON khi file chứa nhiều đối tượng JSON liên tiếp."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip().rstrip(',')
            try:
                if line:
                    data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from line: {line}, Error: {str(e)}")
    return data

def write_json(data, file_path):
    """Ghi dữ liệu vào file JSON."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def filter_duplicates(data):
    """Lọc trùng lặp các mục dựa trên URL và giữ lại đối tượng có số likes, comments, và shares cao nhất."""
    filtered = {}
    for item in data:
        if 'url' in item:
            # Kiểm tra nếu URL đã có trong filtered và so sánh các giá trị
            if item['url'] in filtered:
                # Nếu có thì so sánh và cập nhật nếu item hiện tại có số liệu cao hơn
                if (item['likes'] > filtered[item['url']]['likes'] or
                    item['comments'] > filtered[item['url']]['comments'] or
                    item['shares'] > filtered[item['url']]['shares']):
                    filtered[item['url']] = item
            else:
                # Nếu URL chưa có trong filtered thì thêm vào
                filtered[item['url']] = item
    return list(filtered.values())


# Đường dẫn tới file JSON đầu vào và đầu ra
input_file_path = 'C:/Users/tonyk/Desktop/facebooks_scraped_data.json'
output_file_path = 'output.json'

# Đọc dữ liệu
data = read_json(input_file_path)

print(f"Số lượng đối tượng ban đầu: {len(data)}")

# Lọc trùng lặp
unique_data = filter_duplicates(data)

print(f"Số lượng đối tượng sau khi lọc: {len(unique_data)}")

# Ghi dữ liệu đã lọc vào file mới
write_json(unique_data, output_file_path)

print(f"Dữ liệu đã được xử lý và lưu vào {output_file_path}")
