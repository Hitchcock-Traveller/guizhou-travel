#!/usr/bin/env python3
"""
V11 地图更新脚本 - 替换简略SVG为真实地理数据
- 替换贵州省轮廓路径为GeoJSON生成的真实边界
- 替换路线节点为基于真实地理坐标的位置
- 替换中国小地图为真实省份轮廓
"""
import json, re, os

TARGET = os.path.join(os.path.dirname(__file__), '..', 'index.html')
MAP_DATA = os.path.join(os.path.dirname(__file__), 'map_data.json')
CHINA_DATA = os.path.join(os.path.dirname(__file__), 'china_mini_map.json')

def main():
    with open(TARGET, 'r', encoding='utf-8') as f:
        html = f.read()
    with open(MAP_DATA, 'r', encoding='utf-8') as f:
        map_data = json.load(f)
    with open(CHINA_DATA, 'r', encoding='utf-8') as f:
        china_data = json.load(f)
    
    orig_len = len(html)
    changes = []
    
    # 1. Replace Guizhou province outline (the two identical Q-curve paths)
    old_guizhou_fill = 'M120,100 Q200,70 300,60 Q420,55 550,80 Q620,95 680,140 Q710,175 700,220 Q705,280 690,330 Q680,390 640,430 Q580,470 500,480 Q400,490 300,475 Q220,460 160,430 Q110,400 90,350 Q80,300 85,250 Q90,180 120,100 Z'
    new_path = map_data['province_path']
    
    if old_guizhou_fill in html:
        html = html.replace(old_guizhou_fill, new_path)
        changes.append("贵州省轮廓: 简略Q曲线 → 真实GeoJSON边界(355段)")
    else:
        print("[WARN] Old Guizhou outline not found")
    
    # 2. Replace route node positions
    # Old positions → new real geographic positions
    node_replacements = {
        # 贵阳 D1/D2
        ('cx="380" cy="280"', 'cx="380" cy="280"'): (f'cx="{map_data["route_nodes"]["贵阳"][0]}" cy="{map_data["route_nodes"]["贵阳"][1]}"', '贵阳'),
        # 黄果树
        ('cx="280" cy="320"', 'cx="280" cy="320"'): (f'cx="{map_data["route_nodes"]["黄果树"][0]}" cy="{map_data["route_nodes"]["黄果树"][1]}"', '黄果树'),
        # 织金洞
        ('cx="310" cy="220"', 'cx="310" cy="220"'): (f'cx="{map_data["route_nodes"]["织金洞"][0]}" cy="{map_data["route_nodes"]["织金洞"][1]}"', '织金洞'),
        # 毕节
        ('cx="250" cy="160"', 'cx="250" cy="160"'): (f'cx="{map_data["route_nodes"]["毕节"][0]}" cy="{map_data["route_nodes"]["毕节"][1]}"', '毕节'),
        # 六盘水
        ('cx="180" cy="340"', 'cx="180" cy="340"'): (f'cx="{map_data["route_nodes"]["六盘水"][0]}" cy="{map_data["route_nodes"]["六盘水"][1]}"', '六盘水'),
        # 乌蒙大草原
        ('cx="150" cy="200"', 'cx="150" cy="200"'): (f'cx="{map_data["route_nodes"]["乌蒙大草原"][0]}" cy="{map_data["route_nodes"]["乌蒙大草原"][1]}"', '乌蒙大草原'),
        # 万峰林
        ('cx="200" cy="420"', 'cx="200" cy="420"'): (f'cx="{map_data["route_nodes"]["万峰林"][0]}" cy="{map_data["route_nodes"]["万峰林"][1]}"', '万峰林'),
    }
    
    nodes_moved = 0
    for (old_pos, _), (new_pos, name) in node_replacements.items():
        if old_pos in html:
            # Replace all occurrences of this position (circle, outer ring, label rect, text)
            count = html.count(old_pos)
            html = html.replace(old_pos, new_pos)
            nodes_moved += 1
    
    if nodes_moved:
        changes.append(f"路线节点: {nodes_moved}个节点移至真实地理位置")
    
    # 3. Update route path lines
    nodes = map_data['route_nodes']
    # Main route: 贵阳→黄果树→织金洞→毕节→六盘水→乌蒙→万峰林
    new_route_path = f"M{nodes['贵阳'][0]},{nodes['贵阳'][1]} L{nodes['黄果树'][0]},{nodes['黄果树'][1]} L{nodes['织金洞'][0]},{nodes['织金洞'][1]} L{nodes['毕节'][0]},{nodes['毕节'][1]} L{nodes['六盘水'][0]},{nodes['六盘水'][1]} L{nodes['乌蒙大草原'][0]},{nodes['乌蒙大草原'][1]} L{nodes['万峰林'][0]},{nodes['万峰林'][1]}"
    
    old_route_path = "M380,280 L380,280 L280,320 L310,220 L250,160 L180,340 L150,200 L200,420"
    if old_route_path in html:
        html = html.replace(old_route_path, new_route_path)
        changes.append("路线连线: 更新为真实地理坐标路径")
    
    # Return path
    old_return = "M200,420 Q300,380 380,280"
    new_return = f"M{nodes['万峰林'][0]},{nodes['万峰林'][1]} Q{(nodes['万峰林'][0]+nodes['贵阳'][0])/2+30},{(nodes['万峰林'][1]+nodes['贵阳'][1])/2} {nodes['贵阳'][0]},{nodes['贵阳'][1]}"
    if old_return in html:
        html = html.replace(old_return, new_return)
        changes.append("返程路线: 更新为真实地理坐标")
    
    # 4. Update China mini-map
    old_china_outline = 'M35,25 L55,18 L75,15 L95,18 L110,25 L115,40 L108,55 L100,68 L85,75 L70,78 L55,72 L45,60 L38,45 Z'
    if old_china_outline in html:
        html = html.replace(
            old_china_outline,
            china_data['china_paths']
        )
        changes.append("中国小地图: 简略轮廓 → 真实省份边界")
    
    # 5. Replace Guizhou ellipse in China mini-map with real highlight
    old_guizhou_ellipse = '<ellipse cx="58" cy="55" rx="8" ry="6" fill="rgba(255,107,53,0.6)" stroke="#ff6b35" stroke-width="1"/>'
    if old_guizhou_ellipse in html:
        html = html.replace(
            old_guizhou_ellipse,
            f'<path d="{china_data["guizhou_paths"]}" fill="rgba(255,107,53,0.6)" stroke="#ff6b35" stroke-width="1.5"/>'
        )
        changes.append("中国小地图贵州高亮: 椭圆 → 真实省界高亮")
    
    # Write back
    with open(TARGET, 'w', encoding='utf-8') as f:
        f.write(html)
    
    new_len = len(html)
    print(f"地图更新完成: {orig_len} → {new_len} bytes ({new_len-orig_len:+d})")
    for c in changes:
        print(f"  ✓ {c}")
    print(f"总计 {len(changes)} 项修改")

if __name__ == '__main__':
    main()
