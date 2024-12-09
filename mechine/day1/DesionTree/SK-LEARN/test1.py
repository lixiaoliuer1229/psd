from datetime import datetime

# 毫秒时间戳
timestamp_ms = 1732179972539

# 转换为秒级时间戳
timestamp_s = timestamp_ms / 1000.0

# 解析为日期时间
dt = datetime.fromtimestamp(timestamp_s)

# 格式化为包含毫秒的字符串
formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
print(formatted_time)