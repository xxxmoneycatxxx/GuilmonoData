from flask import Flask, render_template, request, json
app = Flask(__name__)

# 加载数据
with open('rare_items.json', encoding='utf-8') as f:
    rare_items = json.load(f)
    
with open('monsters.json', encoding='utf-8') as f:
    monsters = json.load(f)

@app.route('/')
def index():
    # 获取所有唯一地点和类别
    locations = sorted(set(loc for m in monsters for loc in m['location']))
    categories = sorted(set(item['category'] for item in rare_items))
    return render_template('index.html', locations=locations, categories=categories)

@app.route('/search_by_location', methods=['POST'])
def search_by_location():
    location = request.form['location']
    
    # 查询怪物数据（添加更多字段）
    location_monsters = []
    for m in monsters:
        if location in m['location']:
            monster_data = {
                'id': m['id'],
                'name': m['name'],
                'race': m['race'],
                'level': m['level'],
                'rare_items': ', '.join(m['rare_items']),
                'ability': m['ability'],  # 完整能力字段
                'special_skills': m['special_skills'],
                'spells': m['spells']
            }
            location_monsters.append(monster_data)
    
    # 查询装备数据（添加更多字段）
    location_items = []
    for item in rare_items:
        if any(location in loc for loc in item['location']):
            item_data = {
                'id': item['id'],
                'name': item['name'],
                'category': item['category'],
                'ability': item['ability'],
                'craft': item['craft'],
                'value': item['value']
            }
            location_items.append(item_data)
    
    return render_template(
        'location_result.html',
        location=location,
        monsters=location_monsters,
        items=location_items
    )

@app.route('/search_by_category', methods=['POST'])
def search_by_category():
    category = request.form['category']
    
    # 查询该类别的所有装备
    category_items = [
        {
            'name': item['name'],
            'location': ', '.join(item['location']),
            'ability': item['ability']
        }
        for item in rare_items if item['category'] == category
    ]
    
    return render_template(
        'category_result.html',
        category=category,
        items=category_items
    )

if __name__ == '__main__':
    app.run(debug=True)