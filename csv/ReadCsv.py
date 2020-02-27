import csv

csvPath = '../data/tem.txt'
#  csv的编码格式为utf-8无BOM格式
with open(csvPath, newline='', encoding='UTF-8') as csvFile:
  rows = csv.DictReader(csvFile)
  for row in rows:
    print(row)


with open('../out/tem.csv', 'w') as _csv:
  writer = csv.DictWriter(_csv, fieldnames=['name', 'lon', 'lat'])
  # 写入列标题，即DictWriter构造方法的fieldnames参数
  writer.writeheader()
  for row in rows:
    writer.writerow({'name': row['name'], 'lon': row['lon'], 'lat': row['lat']})

