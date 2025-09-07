import re
import json
from typing import List, Dict, Tuple

def parse_basic_info(text: str) -> Tuple[str, str, List[str], str, int]:
    """解析基础信息列"""
    # 提取名称
    name_match = re.search(r"\*\*名称\*\*：(.+?)\*\*种族", text)
    name = name_match.group(1).strip() if name_match else ""
    
    # 提取种族
    race_match = re.search(r"\*\*种族\*\*：(.+?)\*\*出现场所", text)
    race = race_match.group(1).strip() if race_match else ""
    
    # 提取出现场所
    location_match = re.search(r"\*\*出现场所\*\*：(.+?)\*\*职业等级", text)
    location_str = location_match.group(1).strip() if location_match else ""
    locations = [loc.strip() for loc in location_str.split("、") if loc.strip()]
    
    # 提取职业等级
    job_match = re.search(r"\*\*职业等级\*\*：(.+?)$", text)
    if job_match:
        job_level = job_match.group(1).strip()
        level_match = re.search(r"Lv(\d+)$", job_level)
        level = int(level_match.group(1)) if level_match else 0
        job = re.sub(r"Lv\d+$", "", job_level).strip()
    else:
        job, level = "", 0
    
    return name, race, locations, job, level

def parse_combat(text: str) -> Tuple[List[str], List[str]]:
    """解析战斗特性列"""
    # 分割特殊技能和咒文部分
    special_text = ""
    spells_text = ""
    
    if "**特殊技能**" in text:
        skill_match = re.search(r"\*\*特殊技能\*\*：(.+?)(\*\*咒文\*\*|$)", text, re.DOTALL)
        special_text = skill_match.group(1).strip() if skill_match else ""
    
    if "**咒文**" in text:
        spells_match = re.search(r"\*\*咒文\*\*：(.+?)$", text, re.DOTALL)
        spells_text = spells_match.group(1).strip() if spells_match else ""
    
    # 处理特殊技能
    special_skills = []
    if special_text and special_text != "无":
        # 按数字编号分割技能
        skills = re.split(r"\d+\.\s*", special_text)
        special_skills = [skill.strip().replace("\n", "") 
                         for skill in skills if skill.strip() and skill.strip() != "无"]
    
    # 处理咒文
    spells = []
    if spells_text and spells_text != "无":
        # 按顿号或数字编号分割咒文
        if "、" in spells_text:
            spells = [spell.strip() for spell in spells_text.split("、")]
        else:
            spells_split = re.split(r"\d+\.\s*", spells_text)
            spells = [spell.strip().replace("\n", "") 
                     for spell in spells_split if spell.strip() and spell.strip() != "无"]
    
    return special_skills, spells

def parse_rare_items(text: str) -> List[str]:
    """解析稀有道具列"""
    if not text or text == "无":
        return []
    
    # 按数字编号分割道具
    items = re.split(r"\d+\.\s*", text)
    return [
        item.strip().replace("\n", "").replace("\\", "")
        for item in items if item.strip()
    ]

def parse_monster_table(md_content: str) -> List[Dict]:
    """解析整个怪物表格"""
    monsters = []
    lines = md_content.split("\n")
    
    # 定位表格起始行
    start_index = 0
    for i, line in enumerate(lines):
        if line.startswith("| 序号 |"):
            start_index = i + 2  # 跳过表头和分隔行
            break
    
    # 解析数据行
    for line in lines[start_index:]:
        if not line.startswith("|"):
            continue
            
        columns = [col.strip() for col in line.split("|")[1:-1]]
        if len(columns) < 5:
            continue
            
        try:
            # 解析各列
            monster_id = int(columns[0])
            name, race, locations, job, level = parse_basic_info(columns[1])
            special_skills, spells = parse_combat(columns[2])
            rare_items = parse_rare_items(columns[3])
            ability = columns[4].replace("\n", " ").strip()
            
            monsters.append({
                "id": monster_id,
                "name": name,
                "race": race,
                "location": locations,
                "job": job,
                "level": level,
                "special_skills": special_skills,
                "spells": spells,
                "rare_items": rare_items,
                "ability": ability
            })
        except Exception as e:
            print(f"解析错误 (ID:{columns[0]}): {str(e)}")
    
    return monsters

# 示例使用
if __name__ == "__main__":
    with open("dataSource/monster.Data.md", "r", encoding="utf-8") as f:
        md_content = f.read()
    
    monsters = parse_monster_table(md_content)
    
    # 保存为JSON
    with open("monsters.json", "w", encoding="utf-8") as f:
        json.dump(monsters, f, ensure_ascii=False, indent=2)
    
    print(f"成功解析 {len(monsters)} 个怪物数据")

    # 校验129和130号怪物
    print("\n校验129号怪物:")
    print(json.dumps([m for m in monsters if m["id"] == 129][0], ensure_ascii=False, indent=2))
    
    print("\n校验130号怪物:")
    print(json.dumps([m for m in monsters if m["id"] == 130][0], ensure_ascii=False, indent=2))