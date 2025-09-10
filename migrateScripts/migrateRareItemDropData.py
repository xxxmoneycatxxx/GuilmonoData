import json
import re

def chinese_to_arabic(num_str):
    """将中文数字转换为阿拉伯数字"""
    num_map = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15, '十六': 16, '十七': 17, '十八': 18, '十九': 19,
        '二十': 20, '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24, '二十五': 25, '二十六': 26, '二十七': 27, '二十八': 28, '二十九': 29,
        '三十': 30, '三十一': 31, '三十二': 32, '三十三': 33, '三十四': 34, '三十五': 35, '三十六': 36, '三十七': 37, '三十八': 38, '三十九': 39,
        '四十': 40, '四十一': 41, '四十二': 42, '四十三': 43, '四十四': 44, '四十五': 45, '四十六': 46, '四十七': 47, '四十八': 48, '四十九': 49,
        '五十': 50
    }
    return num_map.get(num_str, 0)

def parse_document(document):
    """解析文档并转换为JSON格式"""
    dungeons = []
    
    # 分割文档为各个地下城部分
    dungeon_sections = re.split(r'####\s+', document.strip())
    dungeon_sections = [sec.strip() for sec in dungeon_sections if sec.strip()]
    
    for section in dungeon_sections:
        # 提取序号和名称
        header_match = re.match(r'([一二三四五六七八九十]+)、(.+?)\s*$', section.split('\n')[0])
        if not header_match:
            continue
            
        chinese_num = header_match.group(1)
        name = header_match.group(2).strip()
        dungeon_id = chinese_to_arabic(chinese_num)
        
        # 提取表格部分
        table_lines = []
        in_table = False
        for line in section.split('\n')[1:]:
            line = line.strip()
            if line.startswith('|--') or line.startswith('|---'):
                in_table = True
                continue
            if in_table and line.startswith('|'):
                table_lines.append(line)
        
        # 解析表格内容
        items = []
        for line in table_lines:
            columns = [col.strip() for col in line.split('|') if col.strip()]
            if len(columns) < 3:
                continue
                
            # 处理稀有标记和名称
            item_name = columns[0]
            is_rare = item_name.startswith('★')
            
            # 即使有★标记也保留在名称中
            # isRare字段用于标识稀有度，名称保持原始格式
            
            # 处理陷阱难度
            trap_difficulty = columns[1] if columns[1] != '-' else ""
            
            # 创建物品对象
            item = {
                "name": item_name,  # 保留★标记
                "isRare": is_rare,  # 单独标记稀有度
                "trap_difficulty": trap_difficulty,
                "drop_monster": columns[2]
            }
            items.append(item)
        
        # 创建地下城对象
        dungeon = {
            "id": dungeon_id,
            "name": name,
            "items": items
        }
        dungeons.append(dungeon)
    
    return dungeons

# 示例使用
if __name__ == "__main__":
    with open('dataSource\item.RareItemDropData.md', 'r', encoding='utf-8') as f:
        document_content = f.read()
    
    json_data = parse_document(document_content)
    
    with open('dungeons.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print("转换完成，结果已保存到 dungeons.json")