import re

def process_document(text):
    sections = re.split(r'(#### [^\n]+\n)', text)[1:]
    result = []
    
    for i in range(0, len(sections), 2):
        section_header = sections[i]
        section_content = sections[i+1]
        
        current_monster = None
        processed_lines = []
        lines = section_content.split('\n')
        
        for line in lines:
            if not line.strip() or '|---' in line:
                # 保留空行和分隔线
                processed_lines.append(line)
                continue
                
            if line.startswith('|') and '陷阱难度' not in line:
                # 表格数据行
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 4:
                    monster = parts[3]
                    if monster != '-' and monster != '':
                        current_monster = monster
                    
                    # 替换怪物列为当前怪物
                    if (monster == '-' or monster == '') and current_monster:
                        parts[3] = current_monster
                    
                    # 重建行并保持原有空格对齐
                    new_line = f"| {parts[1]} | {parts[2].ljust(10)} | {parts[3]} |"
                    processed_lines.append(new_line)
                else:
                    processed_lines.append(line)
            else:
                # 表头行或其他内容
                processed_lines.append(line)
        
        result.append(section_header)
        result.append('\n'.join(processed_lines))
    
    return '\n'.join(result)

# 示例使用
if __name__ == "__main__":
    with open('dataSource\item.RareItemDropData.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    processed_content = process_document(content)
    
    with open('dataSource\item.RareItemDropData.md', 'w', encoding='utf-8') as f:
        f.write(processed_content)