import datetime
import re

def extract_parts_dynamic_old(dirname):
    parts = dirname.split('_')
    test_date = '_'.join(parts[:3])
    test_car_id = parts[6]

    # 提取 行泊场景（可能是多个下划线的部分）
    pilot_start_index = 7
    pilot_end_index = len(parts) - 2  # 真值格式 和 真值类型 占据最后两个部分
    gt_pilot_parking = '_'.join(parts[pilot_start_index:pilot_end_index])
    
    gt_format = parts[-2]
    data_type = parts[-1]

    return test_date, test_car_id, gt_pilot_parking, gt_format, data_type

def extract_parts_dynamic(input_str):
    # 枚举值列表
    pilot_enum_values = ['indoor_parking', 'outdoor_parking', 'pilot']
    
    # 定义时间戳的正则表达式模式
    timestamp_pattern = r'^\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}'
    
    # 提取时间戳部分
    match = re.match(timestamp_pattern, input_str)
    if not match:
        raise ValueError("无法识别时间戳")
    timestamp = match.group(0)
    date_parts = timestamp.split("_")[:3]
    test_date = "_".join(date_parts)
    # 剩余部分
    remaining_str = input_str[len(timestamp) + 1:]  # 跳过时间戳后的下划线
    
    # 查找第一个出现的枚举值
    for enum_value in pilot_enum_values:
        if enum_value in remaining_str:
            parts = remaining_str.split(f"_{enum_value}_", 1)
            if len(parts) == 2:
                vehicle_id = parts[0]
                format_and_type = parts[1].split("_")
                
                if len(format_and_type) != 2:
                    raise ValueError("格式或类型部分解析失败")
                
                return test_date,vehicle_id,enum_value,format_and_type[0],format_and_type[1]
    raise ValueError("未找到有效的枚举值")

def convert_unix_to_formatted_date(unix_timestamp_ms):
    # 将毫秒级时间戳转换为秒级时间戳
    unix_timestamp_seconds = unix_timestamp_ms / 1000
    dt_object = datetime.fromtimestamp(unix_timestamp_seconds)
    
    # 格式化日期时间为指定格式
    formatted_date = dt_object.strftime("%Y_%m_%d_%H_%M_%S")
    
    return formatted_date