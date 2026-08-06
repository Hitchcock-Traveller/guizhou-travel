#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V13 全量新功能追加脚本 - 严格只增不减"""

import re

SRC = '/app/data/所有对话/主对话/用户上传/guizhou-travel-site/index.html'

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

# ========== 新增CSS ==========
V13_CSS = '''
/* ===== 新增样式开始 ===== */

/* 1.1 板块标题淡入上浮 */
@keyframes addFadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.section-header.add-fade-up {
  opacity: 0;
  transform: translateY(20px);
}
.section-header.add-fade-up.add-visible {
  animation: addFadeUp 0.7s ease-out forwards;
}

/* 1.2 按钮/卡片悬停微放大 */
.add-hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.add-hover-lift:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

/* 1.3 当前阅读板块指示器 */
.add-indicator {
  position: fixed;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 100;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px 6px;
  background: rgba(15,22,50,0.6);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(0,212,170,0.2);
  border-radius: 20px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.add-indicator.add-indicator-show {
  opacity: 1;
  pointer-events: auto;
}
.add-indicator-item {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}
.add-indicator-item:hover {
  background: rgba(0,212,170,0.2);
  border-color: rgba(0,212,170,0.4);
}
.add-indicator-item.add-indicator-active {
  background: rgba(0,212,170,0.25);
  border-color: #00d4aa;
  transform: scale(1.15);
  box-shadow: 0 0 10px rgba(0,212,170,0.4);
}
.add-indicator-tooltip {
  position: absolute;
  left: 38px;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(15,22,50,0.95);
  color: #fff;
  font-size: 11px;
  padding: 4px 10px;
  border-radius: 6px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease;
  border: 1px solid rgba(0,212,170,0.3);
}
.add-indicator-item:hover .add-indicator-tooltip {
  opacity: 1;
}
@media (max-width: 768px) {
  .add-indicator { display: none; }
}

/* 1.4 行前清单勾选动画 */
.checklist-item.add-check-anim .checklist-checkbox {
  position: relative;
  overflow: hidden;
}
.checklist-item.add-check-anim.active .checklist-checkbox::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 12px;
  height: 8px;
  border-left: 2px solid #fff;
  border-bottom: 2px solid #fff;
  transform: translate(-50%, -60%) rotate(-45deg) scale(0);
  transform-origin: center;
  animation: addCheckMark 0.35s ease-out forwards;
}
@keyframes addCheckMark {
  0% { transform: translate(-50%, -60%) rotate(-45deg) scale(0); }
  50% { transform: translate(-50%, -60%) rotate(-45deg) scale(1.2); }
  100% { transform: translate(-50%, -60%) rotate(-45deg) scale(1); }
}

/* 2.1 行程总览浮层 */
.add-overview-btn {
  position: fixed;
  bottom: 80px;
  right: 16px;
  z-index: 99;
  background: linear-gradient(135deg, #00d4aa, #00b894);
  color: #fff;
  border: none;
  padding: 12px 18px;
  border-radius: 30px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0,212,170,0.4);
  transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.3s ease;
}
.add-overview-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,212,170,0.5);
}
.add-overview-panel {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 200;
  background: rgba(10,14,39,0.95);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border-top: 1px solid rgba(0,212,170,0.3);
  border-radius: 20px 20px 0 0;
  padding: 20px;
  transform: translateY(100%);
  transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  max-height: 70vh;
  overflow-y: auto;
}
.add-overview-panel.add-overview-open {
  transform: translateY(0);
}
.add-overview-mask {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 199;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}
.add-overview-mask.add-overview-open {
  opacity: 1;
  pointer-events: auto;
}
.add-overview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(0,212,170,0.2);
}
.add-overview-title {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
}
.add-overview-close {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: rgba(255,255,255,0.1);
  border: none;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.add-overview-timeline {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 8px;
  -webkit-overflow-scrolling: touch;
}
.add-overview-day {
  flex: 0 0 110px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.add-overview-day:hover {
  background: rgba(0,212,170,0.1);
  border-color: rgba(0,212,170,0.4);
  transform: translateY(-2px);
}
.add-overview-day-num {
  font-size: 20px;
  font-weight: 800;
  color: #00d4aa;
}
.add-overview-day-label {
  font-size: 10px;
  color: rgba(255,255,255,0.5);
  margin-bottom: 4px;
}
.add-overview-day-title {
  font-size: 11px;
  color: #fff;
  line-height: 1.3;
}

/* 2.2 贵州小知识轮播 */
.add-knowledge-bar {
  padding: 14px 20px;
  background: linear-gradient(90deg, rgba(240,192,64,0.08), rgba(0,212,170,0.08));
  border-top: 1px solid rgba(240,192,64,0.15);
  border-bottom: 1px solid rgba(0,212,170,0.15);
  overflow: hidden;
  position: relative;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.add-knowledge-text {
  font-size: 13px;
  color: var(--text-main, #e8ecf8);
  opacity: 0;
  transition: opacity 0.5s ease;
  text-align: center;
  max-width: 90%;
}
.add-knowledge-text.add-knowledge-show {
  opacity: 1;
}
.add-knowledge-icon {
  margin-right: 8px;
}

/* 2.3 预算计算器切换 */
.add-budget-toggle {
  display: inline-flex;
  align-items: center;
  background: rgba(255,255,255,0.08);
  border-radius: 20px;
  padding: 3px;
  margin-left: 10px;
  vertical-align: middle;
}
.add-budget-toggle-btn {
  padding: 4px 12px;
  border: none;
  background: transparent;
  color: var(--text-sub, #8892b0);
  font-size: 11px;
  font-weight: 600;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.add-budget-toggle-btn.add-budget-toggle-active {
  background: var(--primary, #00d4aa);
  color: #0a0e27;
}

/* 3.1 Hero背景Canvas粒子 */
#add-hero-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}
.hero { position: relative; overflow: hidden; }

/* 3.2 SVG地图城市悬停高亮 */
.route-map circle.route-node {
  transition: all 0.25s ease;
  cursor: pointer;
}
.route-map circle.route-node:hover {
  filter: url(#nodeGlow) brightness(1.3);
  r: 11;
}
.add-map-tooltip {
  position: absolute;
  pointer-events: none;
  background: rgba(15,22,50,0.95);
  color: #fff;
  font-size: 12px;
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid rgba(0,212,170,0.4);
  z-index: 50;
  opacity: 0;
  transition: opacity 0.2s ease;
  white-space: nowrap;
  transform: translate(-50%, -120%);
}
.add-map-tooltip.add-map-tooltip-show {
  opacity: 1;
}

/* 4.1 旅行日记 */
.add-diary-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 12px;
  margin-top: 8px;
  background: rgba(240,192,64,0.15);
  border: 1px solid rgba(240,192,64,0.3);
  color: #f0c040;
  border-radius: 16px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}
.add-diary-btn:hover {
  background: rgba(240,192,64,0.25);
  transform: translateY(-1px);
}
.add-diary-area {
  margin-top: 8px;
  display: none;
}
.add-diary-area.add-diary-open {
  display: block;
  animation: addFadeUp 0.3s ease-out;
}
.add-diary-textarea {
  width: 100%;
  min-height: 60px;
  padding: 8px 10px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(240,192,64,0.25);
  border-radius: 8px;
  color: var(--text-main, #e8ecf8);
  font-size: 12px;
  font-family: inherit;
  resize: vertical;
  box-sizing: border-box;
}
.add-diary-textarea:focus {
  outline: none;
  border-color: #f0c040;
}
.add-diary-status {
  font-size: 10px;
  color: rgba(240,192,64,0.7);
  margin-top: 4px;
}

/* 4.2 景点打卡 */
.add-checkin-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  margin-left: 8px;
  background: rgba(0,212,170,0.1);
  border: 1px solid rgba(0,212,170,0.3);
  color: #00d4aa;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  vertical-align: middle;
}
.add-checkin-btn:hover {
  background: rgba(0,212,170,0.2);
}
.add-checkin-btn.add-checkin-done {
  background: rgba(0,212,170,0.25);
  border-color: #00d4aa;
  color: #00d4aa;
}
.add-checkin-badge {
  display: inline-block;
  width: 14px;
  height: 14px;
  background: #00d4aa;
  color: #0a0e27;
  border-radius: 50%;
  font-size: 9px;
  text-align: center;
  line-height: 14px;
  font-weight: 900;
  margin-left: 4px;
  vertical-align: middle;
}

/* ===== 新增样式结束 ===== */
'''

# 在第一个 </style> 前插入CSS
html = html.replace('</style>', V13_CSS + '</style>', 1)

# ========== 新增HTML ==========

# 3.1 Canvas: 在hero section 内，scroll-hint 之前追加 canvas
# 找到 <div class="scroll-hint">
canvas_html = '  <canvas id="add-hero-canvas"></canvas>\n'
# 在 scroll-hint 前插入
html = html.replace('  <div class="scroll-hint">', canvas_html + '  <div class="scroll-hint">', 1)

# 2.2 贵州小知识轮播 - 在 tips section 和 must-do section 之间插入
knowledge_html = '''
<!-- ===== V13 贵州小知识轮播 ===== -->
<div class="add-knowledge-bar" id="addKnowledgeBar">
  <span class="add-knowledge-icon">💡</span>
  <span class="add-knowledge-text add-knowledge-show" id="addKnowledgeText">贵州被誉为"中国凉都"，夏季平均气温仅23℃</span>
</div>
'''

# 插入在 tips 的 </section> 之后，must-do 之前
# 找 tips section 结束位置
html = html.replace(
    '</section>\n\n\n<!-- ========== V12 此行必做 ========== -->',
    '</section>\n' + knowledge_html + '\n<!-- ========== V12 此行必做 ========== -->',
    1
)

# 如果上面没匹配上，尝试备选
if 'add-knowledge-bar' not in html:
    html = html.replace(
        'id="must-do"',
        'id="must-do-notused" style="display:none"'
    )  # 不会触发，做个标记

# 2.1 行程总览浮层 HTML - 加在 body 末尾前
overview_html = '''
<!-- ===== V13 行程总览浮层 ===== -->
<div class="add-overview-mask" id="addOverviewMask" onclick="add_toggleOverview(false)"></div>
<div class="add-overview-panel" id="addOverviewPanel">
  <div class="add-overview-header">
    <div class="add-overview-title">📋 7天行程总览</div>
    <button class="add-overview-close" onclick="add_toggleOverview(false)" aria-label="关闭">×</button>
  </div>
  <div class="add-overview-timeline" id="addOverviewTimeline"></div>
</div>
<button class="add-overview-btn" id="addOverviewBtn" onclick="add_toggleOverview(true)">📋 行程总览</button>

<!-- ===== V13 当前阅读指示器 ===== -->
<div class="add-indicator" id="addIndicator"></div>

<!-- ===== V13 SVG地图tooltip ===== -->
<div class="add-map-tooltip" id="addMapTooltip"></div>
'''

# 在最后一个 </body> 前插入
html = html.replace('</body>', overview_html + '</body>', 1)

# ========== 新增JS ==========

V13_JS = '''
// ===== 新增脚本开始 =====

(function() {
  'use strict';

  // ===== 1.1 板块标题淡入上浮 =====
  function add_initFadeUp() {
    var headers = document.querySelectorAll('.section-header');
    for (var i = 0; i < headers.length; i++) {
      headers[i].classList.add('add-fade-up');
    }
    if (!('IntersectionObserver' in window)) {
      for (var j = 0; j < headers.length; j++) {
        headers[j].classList.add('add-visible');
      }
      return;
    }
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('add-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });
    for (var k = 0; k < headers.length; k++) {
      observer.observe(headers[k]);
    }
  }

  // ===== 1.2 按钮/卡片悬停微放大 =====
  function add_initHoverLift() {
    var selectors = '.tip-card, .hotel-card, .food-card, .must-do-card, .summary-card, .meal-card';
    var cards = document.querySelectorAll(selectors);
    for (var i = 0; i < cards.length; i++) {
      cards[i].classList.add('add-hover-lift');
    }
  }

  // ===== 1.3 当前阅读板块指示器 =====
  var add_sectionData = [
    { id: 'hero', icon: '🏠', label: '首页' },
    { id: 'route', icon: '🗺️', label: '路线总览' },
    { id: 'itinerary', icon: '📋', label: '每日行程' },
    { id: 'temperature', icon: '🌡️', label: '气温' },
    { id: 'budget', icon: '💰', label: '预算' },
    { id: 'drone', icon: '🚁', label: '航拍' },
    { id: 'checklist', icon: '✅', label: '行前清单' },
    { id: 'summary', icon: '👨‍👩‍👧‍👦', label: '亲子野钓' },
    { id: 'tips', icon: '🚗', label: '自驾须知' },
    { id: 'must-do', icon: '✨', label: '此行必做' }
  ];

  function add_initIndicator() {
    var container = document.getElementById('addIndicator');
    if (!container) return;
    var html = '';
    for (var i = 0; i < add_sectionData.length; i++) {
      var item = add_sectionData[i];
      html += '<div class="add-indicator-item" data-target="' + item.id + '">' +
              '<span>' + item.icon + '</span>' +
              '<span class="add-indicator-tooltip">' + item.label + '</span>' +
              '</div>';
    }
    container.innerHTML = html;

    // 点击跳转
    var items = container.querySelectorAll('.add-indicator-item');
    for (var j = 0; j < items.length; j++) {
      items[j].addEventListener('click', function(e) {
        var targetId = this.getAttribute('data-target');
        var target = document.getElementById(targetId);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    }

    // 滚动监听
    add_updateIndicator();
    window.addEventListener('scroll', add_updateIndicator, { passive: true });
  }

  function add_updateIndicator() {
    var container = document.getElementById('addIndicator');
    if (!container) return;
    var scrollY = window.scrollY || window.pageYOffset;
    var vh = window.innerHeight;

    // 显示/隐藏
    if (scrollY > 200) {
      container.classList.add('add-indicator-show');
    } else {
      container.classList.remove('add-indicator-show');
    }

    // 找到当前最接近视口中心的section
    var centerY = scrollY + vh * 0.4;
    var bestId = null;
    var bestDist = Infinity;
    for (var i = 0; i < add_sectionData.length; i++) {
      var sec = document.getElementById(add_sectionData[i].id);
      if (!sec) continue;
      var rect = sec.getBoundingClientRect();
      var secTop = rect.top + scrollY;
      var secBottom = secTop + rect.height;
      if (centerY >= secTop && centerY <= secBottom) {
        bestId = add_sectionData[i].id;
        break;
      }
      var dist = Math.min(Math.abs(centerY - secTop), Math.abs(centerY - secBottom));
      if (dist < bestDist) {
        bestDist = dist;
        bestId = add_sectionData[i].id;
      }
    }

    var items = container.querySelectorAll('.add-indicator-item');
    for (var j = 0; j < items.length; j++) {
      if (items[j].getAttribute('data-target') === bestId) {
        items[j].classList.add('add-indicator-active');
      } else {
        items[j].classList.remove('add-indicator-active');
      }
    }
  }

  // ===== 1.4 行前清单勾选动画 =====
  function add_initCheckAnim() {
    var items = document.querySelectorAll('.checklist-item');
    for (var i = 0; i < items.length; i++) {
      items[i].classList.add('add-check-anim');
    }
  }

  // ===== 2.1 行程总览浮层 =====
  function add_initOverview() {
    var timeline = document.getElementById('addOverviewTimeline');
    if (!timeline) return;
    // 从DOM中提取day-card信息（主路线前7个）
    var dayCards = document.querySelectorAll('#route-main-cards .day-card');
    var daysData = [];
    for (var i = 0; i < Math.min(7, dayCards.length); i++) {
      var card = dayCards[i];
      var numEl = card.querySelector('.day-num');
      var titleEl = card.querySelector('.day-title');
      daysData.push({
        num: numEl ? numEl.textContent : (i + 1),
        title: titleEl ? titleEl.textContent : 'D' + (i + 1)
      });
    }
    var html = '';
    for (var j = 0; j < daysData.length; j++) {
      var d = daysData[j];
      html += '<div class="add-overview-day" onclick="add_jumpToDay(' + j + ')">' +
              '<div class="add-overview-day-label">DAY</div>' +
              '<div class="add-overview-day-num">' + d.num + '</div>' +
              '<div class="add-overview-day-title">' + d.title + '</div>' +
              '</div>';
    }
    timeline.innerHTML = html;
  }

  function add_toggleOverview(show) {
    var panel = document.getElementById('addOverviewPanel');
    var mask = document.getElementById('addOverviewMask');
    if (!panel || !mask) return;
    if (show) {
      panel.classList.add('add-overview-open');
      mask.classList.add('add-overview-open');
      document.body.style.overflow = 'hidden';
    } else {
      panel.classList.remove('add-overview-open');
      mask.classList.remove('add-overview-open');
      document.body.style.overflow = '';
    }
  }

  function add_jumpToDay(index) {
    var dayCards = document.querySelectorAll('#route-main-cards .day-card');
    if (dayCards[index]) {
      add_toggleOverview(false);
      setTimeout(function() {
        dayCards[index].scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 300);
    }
  }

  // ===== 2.2 贵州小知识轮播 =====
  var add_knowledgeList = [
    '贵州被誉为"中国凉都"，夏季平均气温仅23℃',
    '贵州是全国唯一没有平原支撑的省份，素有"八山一水一分田"之说',
    '茅台酒产自贵州遵义仁怀市，是中国国酒',
    '黄果树瀑布是亚洲最大的瀑布，高77.8米，宽101米',
    '贵州话"摆龙门阵"就是聊天、讲故事的意思',
    '织金洞被誉为"中国溶洞之王"，洞内恒温16℃',
    '贵州是世界知名山地旅游目的地，山地占比92.5%',
    '"酸汤鱼"是贵州苗族特色名菜，酸汤由番茄发酵而成',
    '乌蒙大草原是西南地区海拔最高、面积最大的高原草场',
    '贵州荔波喀斯特是世界自然遗产，被称为"地球腰带上的绿宝石"'
  ];
  var add_knowledgeIndex = 0;
  var add_knowledgeTimer = null;
  var add_knowledgePaused = false;

  function add_initKnowledge() {
    var textEl = document.getElementById('addKnowledgeText');
    if (!textEl) return;
    add_knowledgeIndex = 0;
    add_knowledgeTimer = setInterval(add_nextKnowledge, 5000);

    // visibilitychange 暂停
    document.addEventListener('visibilitychange', function() {
      if (document.hidden) {
        add_knowledgePaused = true;
      } else {
        add_knowledgePaused = false;
      }
    });
  }

  function add_nextKnowledge() {
    if (add_knowledgePaused) return;
    var textEl = document.getElementById('addKnowledgeText');
    if (!textEl) return;
    textEl.classList.remove('add-knowledge-show');
    setTimeout(function() {
      add_knowledgeIndex = (add_knowledgeIndex + 1) % add_knowledgeList.length;
      textEl.textContent = add_knowledgeList[add_knowledgeIndex];
      textEl.classList.add('add-knowledge-show');
    }, 500);
  }

  // ===== 2.3 预算计算器人均/总计切换 =====
  var add_budgetMode = 'total'; // total | per
  var add_budgetOriginalTotal = 0;

  function add_initBudgetToggle() {
    var summaryLabel = document.querySelector('.budget-summary-label');
    if (!summaryLabel) return;
    var toggleHtml = '<span class="add-budget-toggle">' +
      '<button class="add-budget-toggle-btn add-budget-toggle-active" onclick="add_switchBudget(\\'total\\')" id="addBudgetTotalBtn">总计</button>' +
      '<button class="add-budget-toggle-btn" onclick="add_switchBudget(\\'per\\')" id="addBudgetPerBtn">人均</button>' +
      '</span>';
    summaryLabel.innerHTML = summaryLabel.innerHTML + toggleHtml;
  }

  function add_switchBudget(mode) {
    if (add_budgetMode === mode) return;
    add_budgetMode = mode;
    var totalBtn = document.getElementById('addBudgetTotalBtn');
    var perBtn = document.getElementById('addBudgetPerBtn');
    var totalEl = document.getElementById('budget-total');
    var perEl = document.getElementById('budget-per-person');
    if (totalBtn && perBtn) {
      if (mode === 'total') {
        totalBtn.classList.add('add-budget-toggle-active');
        perBtn.classList.remove('add-budget-toggle-active');
      } else {
        perBtn.classList.add('add-budget-toggle-active');
        totalBtn.classList.remove('add-budget-toggle-active');
      }
    }
    if (totalEl && perEl) {
      if (mode === 'per') {
        totalEl.style.display = 'none';
        perEl.style.fontSize = '28px';
        perEl.style.fontWeight = '900';
      } else {
        totalEl.style.display = '';
        perEl.style.fontSize = '';
        perEl.style.fontWeight = '';
      }
    }
  }

  // ===== 3.1 Hero背景Canvas粒子 =====
  var add_particles = [];
  var add_particleCanvas = null;
  var add_particleCtx = null;
  var add_particleAnimId = null;
  var add_mouseX = -9999;
  var add_mouseY = -9999;

  function add_shouldRunParticles() {
    var w = window.innerWidth;
    var dpr = window.devicePixelRatio || 1;
    // 屏幕<360px 或 (dpr>2 且 屏幕<400px) 或 prefers-reduced-motion
    if (w < 360) return false;
    if (dpr > 2 && w < 400) return false;
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return false;
    return true;
  }

  function add_initParticles() {
    if (!add_shouldRunParticles()) return;
    var canvas = document.getElementById('add-hero-canvas');
    if (!canvas) return;
    var hero = document.getElementById('hero');
    if (!hero) return;
    add_particleCanvas = canvas;
    add_particleCtx = canvas.getContext('2d');
    var w = hero.offsetWidth;
    var h = hero.offsetHeight;
    canvas.width = w;
    canvas.height = h;

    // 创建粒子
    var colors = ['rgba(240,192,64,', 'rgba(0,212,170,'];
    add_particles = [];
    var count = 30;
    for (var i = 0; i < count; i++) {
      add_particles.push({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.3,
        r: Math.random() * 3 + 1.5,
        color: colors[Math.floor(Math.random() * colors.length)],
        alpha: Math.random() * 0.3 + 0.1
      });
    }

    // 鼠标移动
    hero.addEventListener('mousemove', function(e) {
      var rect = hero.getBoundingClientRect();
      add_mouseX = e.clientX - rect.left;
      add_mouseY = e.clientY - rect.top;
    });
    hero.addEventListener('mouseleave', function() {
      add_mouseX = -9999;
      add_mouseY = -9999;
    });

    // resize
    window.addEventListener('resize', function() {
      if (!add_particleCanvas) return;
      var hw = hero.offsetWidth;
      var hh = hero.offsetHeight;
      add_particleCanvas.width = hw;
      add_particleCanvas.height = hh;
    });

    add_animateParticles();
  }

  function add_animateParticles() {
    if (!add_particleCtx || !add_particleCanvas) return;
    var ctx = add_particleCtx;
    var w = add_particleCanvas.width;
    var h = add_particleCanvas.height;
    ctx.clearRect(0, 0, w, h);

    for (var i = 0; i < add_particles.length; i++) {
      var p = add_particles[i];

      // 鼠标避让
      if (add_mouseX > 0 && add_mouseY > 0) {
        var dx = p.x - add_mouseX;
        var dy = p.y - add_mouseY;
        var dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 80) {
          var force = (80 - dist) / 80;
          p.x += (dx / dist) * force * 1.5;
          p.y += (dy / dist) * force * 1.5;
        }
      }

      p.x += p.vx;
      p.y += p.vy;

      // 边界反弹
      if (p.x < 0 || p.x > w) p.vx *= -1;
      if (p.y < 0 || p.y > h) p.vy *= -1;
      p.x = Math.max(0, Math.min(w, p.x));
      p.y = Math.max(0, Math.min(h, p.y));

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = p.color + p.alpha + ')';
      ctx.fill();
    }

    add_particleAnimId = requestAnimationFrame(add_animateParticles);
  }

  // ===== 3.2 SVG地图城市悬停高亮 =====
  function add_initMapHover() {
    var maps = document.querySelectorAll('.route-map');
    var tooltip = document.getElementById('addMapTooltip');
    if (!tooltip) return;

    for (var m = 0; m < maps.length; m++) {
      var map = maps[m];
      var container = map.closest('.route-map-container') || map.parentElement;
      if (!container.style.position || container.style.position === 'static') {
        container.style.position = 'relative';
      }

      var nodes = map.querySelectorAll('circle.route-node');
      for (var i = 0; i < nodes.length; i++) {
        (function(node) {
          node.addEventListener('mouseenter', function(e) {
            // 找附近text
            var text = '';
            var siblings = node.parentNode.querySelectorAll('text');
            var cx = parseFloat(node.getAttribute('cx'));
            var cy = parseFloat(node.getAttribute('cy'));
            var closest = null;
            var minDist = Infinity;
            for (var j = 0; j < siblings.length; j++) {
              var t = siblings[j];
              var tx = parseFloat(t.getAttribute('x'));
              var ty = parseFloat(t.getAttribute('y'));
              if (isNaN(tx) || isNaN(ty)) continue;
              var d = Math.sqrt((tx - cx) * (tx - cx) + (ty - cy) * (ty - cy));
              if (d < minDist && d < 80) {
                minDist = d;
                closest = t;
              }
            }
            if (closest) text = closest.textContent;

            tooltip.textContent = text || '贵州景点';
            tooltip.classList.add('add-map-tooltip-show');
          });

          node.addEventListener('mousemove', function(e) {
            var rect = container.getBoundingClientRect();
            tooltip.style.left = (e.clientX - rect.left) + 'px';
            tooltip.style.top = (e.clientY - rect.top) + 'px';
          });

          node.addEventListener('mouseleave', function() {
            tooltip.classList.remove('add-map-tooltip-show');
          });
        })(nodes[i]);
      }
    }
  }

  // ===== 4.1 旅行日记 =====
  function add_initDiary() {
    var dayCards = document.querySelectorAll('.day-card');
    for (var i = 0; i < dayCards.length; i++) {
      (function(card, idx) {
        var dayNum = idx + 1;
        var bodyInner = card.querySelector('.itinerary-body-inner');
        if (!bodyInner) return;

        var btn = document.createElement('button');
        btn.className = 'add-diary-btn';
        btn.innerHTML = '✏️ 写两句';
        btn.onclick = function() {
          var area = card.querySelector('.add-diary-area');
          if (area) {
            area.classList.toggle('add-diary-open');
            var ta = area.querySelector('textarea');
            if (ta && area.classList.contains('add-diary-open')) {
              ta.focus();
            }
          }
        };

        var area = document.createElement('div');
        area.className = 'add-diary-area';
        area.innerHTML = '<textarea class="add-diary-textarea" placeholder="记录今天的旅行心情..." oninput="add_saveDiary(' + dayNum + ', this.value)"></textarea>' +
                          '<div class="add-diary-status">💾 自动保存到本地</div>';

        bodyInner.appendChild(btn);
        bodyInner.appendChild(area);

        // 恢复内容
        var saved = null;
        try {
          saved = localStorage.getItem('guizhou_diary_D' + dayNum);
        } catch (e) {}
        if (saved) {
          var ta = area.querySelector('textarea');
          if (ta) ta.value = saved;
        }
      })(dayCards[i], i);
    }
  }

  function add_saveDiary(dayNum, value) {
    try {
      localStorage.setItem('guizhou_diary_D' + dayNum, value);
    } catch (e) {}
  }

  // ===== 4.2 景点打卡 =====
  function add_initCheckin() {
    // 给每个 day-title 景点标题添加打卡按钮
    var dayTitles = document.querySelectorAll('.day-title');
    for (var i = 0; i < dayTitles.length; i++) {
      (function(titleEl, idx) {
        var text = titleEl.textContent.trim().replace(/\s+/g, '_').substring(0, 30);
        var key = 'guizhou_checkin_' + text;
        var btn = document.createElement('button');
        btn.className = 'add-checkin-btn';
        btn.innerHTML = '📍 打卡';
        var done = false;
        try {
          done = localStorage.getItem(key) === '1';
        } catch (e) {}
        if (done) {
          btn.classList.add('add-checkin-done');
          btn.innerHTML = '✓ 已打卡<span class="add-checkin-badge">✓</span>';
        }
        btn.onclick = function(e) {
          e.stopPropagation();
          var isDone = btn.classList.contains('add-checkin-done');
          if (isDone) {
            btn.classList.remove('add-checkin-done');
            btn.innerHTML = '📍 打卡';
            try { localStorage.removeItem(key); } catch (err) {}
          } else {
            btn.classList.add('add-checkin-done');
            btn.innerHTML = '✓ 已打卡<span class="add-checkin-badge">✓</span>';
            try { localStorage.setItem(key, '1'); } catch (err) {}
          }
        };
        titleEl.appendChild(btn);
      })(dayTitles[i], i);
    }
  }

  // ===== 初始化 =====
  function add_initAll() {
    try { add_initFadeUp(); } catch (e) { console.warn('fadeUp init error', e); }
    try { add_initHoverLift(); } catch (e) { console.warn('hoverLift init error', e); }
    try { add_initIndicator(); } catch (e) { console.warn('indicator init error', e); }
    try { add_initCheckAnim(); } catch (e) { console.warn('checkAnim init error', e); }
    try { add_initOverview(); } catch (e) { console.warn('overview init error', e); }
    try { add_initKnowledge(); } catch (e) { console.warn('knowledge init error', e); }
    try { add_initBudgetToggle(); } catch (e) { console.warn('budgetToggle init error', e); }
    try { add_initParticles(); } catch (e) { console.warn('particles init error', e); }
    try { add_initMapHover(); } catch (e) { console.warn('mapHover init error', e); }
    try { add_initDiary(); } catch (e) { console.warn('diary init error', e); }
    try { add_initCheckin(); } catch (e) { console.warn('checkin init error', e); }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', add_initAll);
  } else {
    add_initAll();
  }

  // 暴露到全局
  window.add_toggleOverview = add_toggleOverview;
  window.add_jumpToDay = add_jumpToDay;
  window.add_switchBudget = add_switchBudget;
  window.add_saveDiary = add_saveDiary;

})();

// ===== 新增脚本结束 =====
'''

# 在最后一个 </script> 前插入
# 找到最后一个 </script> 位置（第6171行附近，主脚本结束）
last_script_pos = html.rfind('</script>')
if last_script_pos != -1:
    html = html[:last_script_pos] + V13_JS + html[last_script_pos:]

# 写回
with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

import os
size = os.path.getsize(SRC)
print(f'文件大小: {size} 字节 ({size/1024:.1f} KB)')
print(f'剩余空间: {409600 - size} 字节')
