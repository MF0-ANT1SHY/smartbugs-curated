import json
import csv

# 读取JSON文件
with open('vulnerabilities.json', 'r') as file:
    data = json.load(file)

# 准备CSV文件的行
rows = []

for contract in data:
    name = contract['name']
    for vulnerability in contract['vulnerabilities']:
        category = vulnerability['category']
        rows.append((name, category))

# 写入CSV文件
with open('vulnerabilities.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Category'])
    writer.writerows(rows)

print("CSV文件已成功生成。")