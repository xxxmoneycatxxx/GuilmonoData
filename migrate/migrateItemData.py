import re
import json
from collections import defaultdict

def parse_rare_items(md_content):
    """解析稀有道具文档"""
    category_pattern = r"## ([\u4e00-\u9fa0]+、.+?) 共 \d+ 种"
    table_pattern = r"\| (\d+)\s+\| (.+?)\s+\| (.+?)\s+\| (.+?)\s+\| (.+?)\s+\|"
    
    items = []
    current_category = ""
    
    for line in md_content.split('\n'):
        # 匹配类别标题
        category_match = re.match(category_pattern, line)
        if category_match:
            current_category = category_match.group(1).split('、', 1)[1]
            continue
            
        # 匹配表格行
        table_match = re.match(table_pattern, line)
        if table_match and current_category:
            no, name, locations, ability, value = table_match.groups()
            # 清理掉落地点和价值数据
            clean_locations = [loc.strip() for loc in locations.split('、')]
            clean_value = int(value.replace('GP', '').replace(',', '').strip())
            
            items.append({
                "id": len(items) + 1,
                "name": name.strip(),
                "category": current_category,
                "location": clean_locations,
                "ability": ability.strip(),
                "craft": "",  # 初始化为空，后续填充
                "value": clean_value
            })
    return items

def parse_craft_data(md_content):
    """解析合成公式文档"""
    craft_pattern = r"\| (.+?)\s+\| (.+?)\s+\| (.+?)\s+\|"
    crafts = defaultdict(list)
    in_craft_section = False
    
    for line in md_content.split('\n'):
        if "## 二、变化合成" in line:
            in_craft_section = True
            continue
        if not in_craft_section:
            continue
            
        craft_match = re.match(craft_pattern, line)
        if craft_match:
            material, catalyst, result = craft_match.groups()
            crafts[result.strip()].append(f"{material.strip()} + {catalyst.strip()}")
    return crafts

def merge_craft_info(items, crafts):
    """合并合成公式到道具数据"""
    for item in items:
        if "道具合成" in item["location"]:
            item_name = re.sub(r"※.+$", "", item["name"]).strip()
            if item_name in crafts:
                item["craft"] = " 或 ".join(crafts[item_name])
    return items

# 主流程
with open("dataSource/item.RareItemData.md", "r", encoding="utf-8") as f:
    rare_items = parse_rare_items(f.read())

with open("dataSource/item.ItemCraftData.md", "r", encoding="utf-8") as f:
    craft_data = parse_craft_data(f.read())

final_items = merge_craft_info(rare_items, craft_data)

# 保存JSON
with open("rare_items.json", "w", encoding="utf-8") as f:
    json.dump(final_items, f, ensure_ascii=False, indent=2)