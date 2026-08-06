# -*- coding: utf-8 -*-
import re

filepath = '/app/data/所有对话/主对话/用户上传/guizhou-travel-site/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Update version number in title
# ============================================================
content = content.replace(
    u'贵州避暑自驾之旅 7天6晚 V16',
    u'贵州避暑自驾之旅 7天6晚 V17'
)

# ============================================================
# 2. Replace add_portalConfig - remove gradient, keep emoji/title/sub
# ============================================================
old_config = r"""var add_portalConfig = {
  route: { emoji: '\ud83d\uddfa\ufe0f', title: '\u8def\u7ebf\u603b\u89c8', sub: '7\u5929\u73af\u7ebf \u00b7 2000km', gradient: 'linear-gradient(135deg, #0d9488, #065f46)' },
  itinerary: { emoji: '\ud83d\udcc5', title: '\u6bcf\u65e5\u884c\u7a0b', sub: '7\u59296\u665a\u8be6\u60c5', gradient: 'linear-gradient(135deg, #7c3aed, #4c1d95)' },
  temperature: { emoji: '\ud83c\udf21\ufe0f', title: '\u6c14\u6e29\u5bf9\u6bd4', sub: '\u907f\u669114-26\u2103', gradient: 'linear-gradient(135deg, #ea580c, #9a3412)' },
  budget: { emoji: '\ud83d\udcb0', title: '\u9884\u7b97', sub: '6000-8000\u5143', gradient: 'linear-gradient(135deg, #16a34a, #14532d)' },
  drone: { emoji: '\ud83d\ude81', title: '\u822a\u62cd\u6307\u5357', sub: '\u98de\u884c\u6307\u5357', gradient: 'linear-gradient(135deg, #2563eb, #1e3a5f)' },
  checklist: { emoji: '\u2705', title: '\u884c\u524d\u6e05\u5355', sub: '12\u9879\u5f85\u786e\u8ba4', gradient: 'linear-gradient(135deg, #0891b2, #164e63)' },
  summary: { emoji: '\ud83d\udc68\u200d\ud83d\udc69\u200d\ud83d\udc67\u200d\ud83d\udc66', title: '\u4eb2\u5b50\u91ce\u9493', sub: '\u6d3b\u52a8\u6c47\u603b', gradient: 'linear-gradient(135deg, #db2777, #831843)' },
  'must-do': { emoji: '\u2728', title: '\u6b64\u884c\u5fc5\u505a', sub: '8\u4e2a\u5fc5\u4f53\u9a8c', gradient: 'linear-gradient(135deg, #ca8a04, #713f12)' }
};"""

new_config = """var add_portalConfig = {
  route: { emoji: '\\ud83d\\uddfa\\ufe0f', title: '\\u8def\\u7ebf\\u603b\\u89c8', sub: '7\\u5929\\u73af\\u7ebf \\u00b7 2000km' },
  itinerary: { emoji: '\\ud83d\\udcc5', title: '\\u6bcf\\u65e5\\u884c\\u7a0b', sub: '7\\u59296\\u665a\\u8be6\\u60c5' },
  temperature: { emoji: '\\ud83c\\udf21\\ufe0f', title: '\\u6c14\\u6e29\\u5bf9\\u6bd4', sub: '\\u907f\\u669114-26\\u2103' },
  budget: { emoji: '\\ud83d\\udcb0', title: '\\u9884\\u7b97', sub: '6000-8000\\u5143' },
  drone: { emoji: '\\ud83d\\ude81', title: '\\u822a\\u62cd\\u6307\\u5357', sub: '\\u98de\\u884c\\u6307\\u5357' },
  checklist: { emoji: '\\u2705', title: '\\u884c\\u524d\\u6e05\\u5355', sub: '12\\u9879\\u5f85\\u786e\\u8ba4' },
  summary: { emoji: '\\ud83d\\udc68\\u200d\\ud83d\\udc69\\u200d\\ud83d\\udc67\\u200d\\ud83d\\udc66', title: '\\u4eb2\\u5b50\\u91ce\\u9493', sub: '\\u6d3b\\u52a8\\u6c47\\u603b' },
  'must-do': { emoji: '\\u2728', title: '\\u6b64\\u884c\\u5fc5\\u505a', sub: '8\\u4e2a\\u5fc5\\u4f53\\u9a8c' }
};"""

content = content.replace(old_config, new_config)

# ============================================================
# 3. Replace .add-portal-header CSS - unified dark color
# ============================================================
old_header_css = """.add-portal-header {
  position: relative;
  padding: 50px 20px 20px;
  text-align: center;
  min-height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}"""

new_header_css = """.add-portal-header {
  position: relative;
  padding: 44px 20px 16px;
  text-align: center;
  min-height: 80px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  background: linear-gradient(180deg, #1a2332 0%, #0f172a 100%);
}"""

content = content.replace(old_header_css, new_header_css)

# ============================================================
# 4. Hide the large decorative emoji in header
# ============================================================
old_emoji_css = """.add-portal-header-emoji {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 4rem;
  opacity: 0.15;
  line-height: 1;
  pointer-events: none;
}"""

new_emoji_css = """.add-portal-header-emoji {
  display: none;
}"""

content = content.replace(old_emoji_css, new_emoji_css)

# ============================================================
# 5. Add L3 header CSS and itin-l2 CSS after the portal section CSS
#    Insert before "/* ===== V16 Portal View System End ===== */"
# ============================================================
v17_new_css = """
/* --- V17: Level 3+ Header (更精简) --- */
.add-portal-header.add-header-l3 {
  padding: 44px 20px 12px;
  min-height: 56px;
  background: #0f172a;
}
.add-header-l3 .add-portal-subtitle {
  display: none;
}
.add-header-l3 .add-portal-title {
  font-size: 1.1rem;
}

/* --- V17: L2 Itinerary - 所有day-card折叠，header可点击钻入L3 --- */
.add-itin-l2 .day-card .itinerary-body {
  display: none !important;
}
.add-itin-l2 .day-card .itinerary-header {
  cursor: pointer;
  position: relative;
}
.add-itin-l2 .day-card .itinerary-header .toggle-icon {
  display: none;
}
.add-itin-l2 .day-card .itinerary-header::after {
  content: '\\203a';
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.6rem;
  color: var(--primary);
  opacity: 0.6;
}
.add-itin-l2 .itinerary-card.open .itinerary-body {
  display: none !important;
}

/* --- V17: L3 单天展开样式 --- */
.add-day-expanded .itinerary-body {
  display: block !important;
}

/* --- V17: L3+ 隐藏底部导航 --- */
.add-header-l3 ~ .add-portal-nav,
.add-portal-overlay.add-no-bottom-nav .add-portal-nav {
  display: none !important;
}

"""

content = content.replace(
    '/* ===== V16 Portal View System End ===== */',
    v17_new_css + '/* ===== V16 Portal View System End ===== */'
)

# ============================================================
# 6. Replace the entire JS portal system
# ============================================================
# Find the start and end markers
start_marker = '// ===== V16 Portal View System 开始 ====='
end_marker = '// ===== V16 Portal View System 结束 ====='

start_idx = content.index(start_marker)
end_idx = content.index(end_marker) + len(end_marker)

new_js = """// ===== V17 Portal View System 开始 =====

// V17: 导航栈系统 - 多层钻入
var add_navStack = [];
// 每个元素: {level: number, sectionId: string, extra: object}
// level 1 = 入口网格(不在栈中)
// level 2 = 板块门户页
// level 3 = 板块内详情（如某天行程详情）

var add_isMobileView = false;
var add_sectionParents = {};

var add_portalConfig = {
  route: { emoji: '\\ud83d\\uddfa\\ufe0f', title: '\\u8def\\u7ebf\\u603b\\u89c8', sub: '7\\u5929\\u73af\\u7ebf \\u00b7 2000km' },
  itinerary: { emoji: '\\ud83d\\udcc5', title: '\\u6bcf\\u65e5\\u884c\\u7a0b', sub: '7\\u59296\\u665a\\u8be6\\u60c5' },
  temperature: { emoji: '\\ud83c\\udf21\\ufe0f', title: '\\u6c14\\u6e29\\u5bf9\\u6bd4', sub: '\\u907f\\u669114-26\\u2103' },
  budget: { emoji: '\\ud83d\\udcb0', title: '\\u9884\\u7b97', sub: '6000-8000\\u5143' },
  drone: { emoji: '\\ud83d\\ude81', title: '\\u822a\\u62cd\\u6307\\u5357', sub: '\\u98de\\u884c\\u6307\\u5357' },
  checklist: { emoji: '\\u2705', title: '\\u884c\\u524d\\u6e05\\u5355', sub: '12\\u9879\\u5f85\\u786e\\u8ba4' },
  summary: { emoji: '\\ud83d\\udc68\\u200d\\ud83d\\udc69\\u200d\\ud83d\\udc67\\u200d\\ud83d\\udc66', title: '\\u4eb2\\u5b50\\u91ce\\u9493', sub: '\\u6d3b\\u52a8\\u6c47\\u603b' },
  'must-do': { emoji: '\\u2728', title: '\\u6b64\\u884c\\u5fc5\\u505a', sub: '8\\u4e2a\\u5fc5\\u4f53\\u9a8c' }
};

function add_checkMobile() {
  add_isMobileView = window.innerWidth <= 768;
}

function add_storeParent(id) {
  var el = document.getElementById(id);
  if (el && !add_sectionParents[id]) {
    add_sectionParents[id] = el.parentNode;
  }
}

function add_storeAllParents() {
  var keys = Object.keys(add_portalConfig);
  for (var i = 0; i < keys.length; i++) {
    add_storeParent(keys[i]);
  }
}

function add_buildPortalHeader(sectionId, level) {
  var cfg = add_portalConfig[sectionId];
  if (!cfg) return null;
  var header = document.createElement('div');
  header.className = 'add-portal-header';
  if (level >= 3) {
    header.classList.add('add-header-l3');
  }
  // No inline style for gradient - unified CSS handles it

  var emojiSpan = document.createElement('span');
  emojiSpan.className = 'add-portal-header-emoji';
  emojiSpan.textContent = cfg.emoji;

  var backBtn = document.createElement('button');
  backBtn.className = 'add-portal-back';
  backBtn.textContent = '\\u2190 \\u8fd4\\u56de';
  backBtn.addEventListener('click', function() { add_goBack(); });

  var title = document.createElement('h2');
  title.className = 'add-portal-title';
  title.textContent = cfg.title;

  var subtitle = document.createElement('div');
  subtitle.className = 'add-portal-subtitle';
  subtitle.textContent = cfg.sub;

  header.appendChild(emojiSpan);
  header.appendChild(backBtn);
  header.appendChild(title);
  header.appendChild(subtitle);
  return header;
}

function add_updateNav(sectionId) {
  var navItems = document.querySelectorAll('.add-portal-nav-item');
  for (var i = 0; i < navItems.length; i++) {
    if (navItems[i].getAttribute('data-target') === sectionId) {
      navItems[i].classList.add('add-nav-active');
    } else {
      navItems[i].classList.remove('add-nav-active');
    }
  }
}

function add_hideAllInWrapper() {
  var wrapper = document.getElementById('add-sections-wrapper');
  if (!wrapper) return;
  var allSections = wrapper.querySelectorAll('.section.mobile-accordion');
  var allDividers = wrapper.querySelectorAll('.mountain-divider, .wave-divider');
  var allKnowledge = wrapper.querySelectorAll('.add-knowledge-bar');
  for (var i = 0; i < allSections.length; i++) {
    allSections[i].style.display = 'none';
    allSections[i].classList.remove('add-section-active', 'add-itin-summary', 'add-itin-l2', 'add-in-portal');
  }
  for (var j = 0; j < allDividers.length; j++) {
    allDividers[j].style.display = 'none';
  }
  for (var k = 0; k < allKnowledge.length; k++) {
    allKnowledge[k].style.display = 'none';
  }
}

function add_restoreAllInWrapper() {
  var wrapper = document.getElementById('add-sections-wrapper');
  if (!wrapper) return;
  var allSections = wrapper.querySelectorAll('.section.mobile-accordion');
  var allDividers = wrapper.querySelectorAll('.mountain-divider, .wave-divider');
  var allKnowledge = wrapper.querySelectorAll('.add-knowledge-bar');
  for (var i = 0; i < allSections.length; i++) {
    allSections[i].style.display = '';
    allSections[i].classList.remove('add-section-active', 'add-itin-summary', 'add-itin-l2', 'add-in-portal');
  }
  for (var j = 0; j < allDividers.length; j++) {
    allDividers[j].style.display = '';
  }
  for (var k = 0; k < allKnowledge.length; k++) {
    allKnowledge[k].style.display = '';
  }
}

function add_prepareSection(sectionId) {
  var section = document.getElementById(sectionId);
  if (!section) return null;

  add_storeParent(sectionId);

  section.classList.add('add-section-active', 'add-in-portal');
  section.classList.remove('accordion-collapsed');
  section.style.display = '';

  // For itinerary: add L2 summary mode (all folded, click to drill down)
  if (sectionId === 'itinerary') {
    section.classList.add('add-itin-l2');
    // Remove any previous L3 state
    var dayCards = section.querySelectorAll('.day-card');
    for (var i = 0; i < dayCards.length; i++) {
      dayCards[i].style.display = '';
      dayCards[i].classList.remove('add-day-expanded');
    }
    // Bind header click for drill-down to L3
    var dayHeaders = section.querySelectorAll('.day-card .itinerary-header');
    for (var j = 0; j < dayHeaders.length; j++) {
      (function(header, idx) {
        if (header.dataset.addDrillBind) return;
        header.dataset.addDrillBind = '1';
        header.addEventListener('click', function(e) {
          e.preventDefault();
          e.stopPropagation();
          add_drillDownItinerary(idx);
        });
      })(dayHeaders[j], j);
    }
  }

  return section;
}

function add_returnSection(sectionId) {
  var section = document.getElementById(sectionId);
  if (!section) return;
  section.classList.remove('add-section-active', 'add-itin-summary', 'add-itin-l2', 'add-in-portal');

  // Reset itinerary cards
  if (sectionId === 'itinerary') {
    var dayCards = section.querySelectorAll('.day-card');
    for (var i = 0; i < dayCards.length; i++) {
      dayCards[i].style.display = '';
      dayCards[i].classList.remove('add-day-expanded');
    }
  }

  if (add_sectionParents[sectionId]) {
    add_sectionParents[sectionId].appendChild(section);
  }
}

// ============================================================
// V17: Core navigation functions
// ============================================================

function add_openPortal(sectionId) {
  if (!add_isMobileView) return;

  add_storeAllParents();

  var overlay = document.getElementById('add-portal-overlay');
  var portalContent = document.getElementById('add-portal-content');
  var section = document.getElementById(sectionId);
  if (!overlay || !portalContent || !section) return;

  // Reset nav stack
  add_navStack = [{level: 2, sectionId: sectionId}];

  // Hide all sections in wrapper
  add_hideAllInWrapper();

  // Prepare the section
  var prepared = add_prepareSection(sectionId);
  if (!prepared) return;

  // Clear portal content
  portalContent.innerHTML = '';

  // Build and add portal header (level 2)
  var header = add_buildPortalHeader(sectionId, 2);
  if (header) {
    portalContent.appendChild(header);
  }

  // Move section into portal
  portalContent.appendChild(prepared);

  // Add fade-in animation
  prepared.classList.add('add-portal-section-enter');
  setTimeout(function() {
    prepared.classList.remove('add-portal-section-enter');
  }, 300);

  // Show overlay
  overlay.classList.remove('add-portal-closing', 'add-no-bottom-nav');
  overlay.classList.add('add-portal-open');

  // Show bottom nav (L2 shows nav)
  var nav = document.getElementById('add-portal-nav');
  if (nav) nav.classList.add('add-nav-visible');

  add_updateNav(sectionId);

  // Prevent body scroll
  document.body.style.overflow = 'hidden';

  // Scroll overlay to top
  overlay.scrollTop = 0;

  // Re-trigger fade-in animations
  var fadeEls = prepared.querySelectorAll('.fade-in');
  for (var i = 0; i < fadeEls.length; i++) {
    fadeEls[i].classList.add('visible');
  }

  // Animate temp bars if temperature section
  if (sectionId === 'temperature' && typeof animateTempBars === 'function') {
    setTimeout(animateTempBars, 300);
  }

  // Update checklist progress if checklist section
  if (sectionId === 'checklist' && typeof updateChecklistProgress === 'function') {
    setTimeout(updateChecklistProgress, 100);
  }
}

function add_goBack() {
  if (add_navStack.length <= 1) {
    // Stack empty or only grid level -> close portal
    add_closePortal();
  } else {
    // Pop current level
    add_navStack.pop();
    var prev = add_navStack[add_navStack.length - 1];

    if (prev.level === 2) {
      // Go back to section overview (L2)
      add_showLevel2(prev.sectionId);
    } else if (prev.level >= 3) {
      // Go back to deeper level (unlikely in current design but supported)
      add_showLevel3(prev.sectionId, prev.extra);
    }
  }
}

function add_showLevel2(sectionId) {
  var overlay = document.getElementById('add-portal-overlay');
  var portalContent = document.getElementById('add-portal-content');
  if (!overlay || !portalContent) return;

  // Get current section from portal content
  var section = document.getElementById(sectionId);
  if (!section) return;

  // Reset section to L2 state
  section.classList.remove('add-itin-l2');
  var dayCards = section.querySelectorAll('.day-card');
  for (var i = 0; i < dayCards.length; i++) {
    dayCards[i].style.display = '';
    dayCards[i].classList.remove('add-day-expanded');
  }

  // Re-apply L2 state
  if (sectionId === 'itinerary') {
    section.classList.add('add-itin-l2');
  }

  // Rebuild header at L2
  portalContent.innerHTML = '';
  var header = add_buildPortalHeader(sectionId, 2);
  if (header) {
    portalContent.appendChild(header);
  }
  portalContent.appendChild(section);

  // Show bottom nav
  overlay.classList.remove('add-no-bottom-nav');
  var nav = document.getElementById('add-portal-nav');
  if (nav) nav.classList.add('add-nav-visible');

  add_updateNav(sectionId);

  // Scroll to top
  overlay.scrollTop = 0;
}

// V17: Drill down into itinerary day detail (Level 3)
function add_drillDownItinerary(dayIndex) {
  // Push to nav stack
  add_navStack.push({level: 3, sectionId: 'itinerary', extra: {dayIndex: dayIndex}});

  var overlay = document.getElementById('add-portal-overlay');
  var portalContent = document.getElementById('add-portal-content');
  var section = document.getElementById('itinerary');
  if (!section) return;

  var cards = section.querySelectorAll('.day-card');

  // Hide all cards except the target
  for (var i = 0; i < cards.length; i++) {
    cards[i].style.display = (i === dayIndex) ? '' : 'none';
  }

  // Expand the target card
  var targetCard = cards[dayIndex];
  targetCard.classList.add('add-day-expanded');
  if (targetCard.classList.contains('itinerary-card')) {
    targetCard.classList.add('open');
  }

  // Remove L2 class
  section.classList.remove('add-itin-l2');

  // Update header to L3 style
  var header = portalContent.querySelector('.add-portal-header');
  if (header) {
    header.classList.add('add-header-l3');
    // Extract day info from the card header
    var cardHeader = targetCard.querySelector('.itinerary-header');
    if (cardHeader) {
      var titleEl = header.querySelector('.add-portal-title');
      var leftInfo = cardHeader.querySelector('.itinerary-header-left');
      if (titleEl && leftInfo) {
        titleEl.textContent = leftInfo.textContent.trim().replace(/\\s+/g, ' ');
      }
      var subEl = header.querySelector('.add-portal-subtitle');
      if (subEl) subEl.style.display = 'none';
    }
  }

  // Hide bottom nav
  if (overlay) overlay.classList.add('add-no-bottom-nav');
  var nav = document.getElementById('add-portal-nav');
  if (nav) nav.classList.remove('add-nav-visible');

  // Scroll to top
  if (overlay) overlay.scrollTop = 0;
}

// V17: Generic Level 3 drill-down (for future use)
function add_showLevel3(sectionId, extra) {
  if (sectionId === 'itinerary' && extra && extra.dayIndex !== undefined) {
    // Re-show the specific day
    var overlay = document.getElementById('add-portal-overlay');
    var portalContent = document.getElementById('add-portal-content');
    var section = document.getElementById('itinerary');
    if (!section) return;

    var cards = section.querySelectorAll('.day-card');
    for (var i = 0; i < cards.length; i++) {
      cards[i].style.display = (i === extra.dayIndex) ? '' : 'none';
    }
    var targetCard = cards[extra.dayIndex];
    targetCard.classList.add('add-day-expanded');
    section.classList.remove('add-itin-l2');

    var header = portalContent.querySelector('.add-portal-header');
    if (header) {
      header.classList.add('add-header-l3');
      var cardHeader = targetCard.querySelector('.itinerary-header');
      if (cardHeader) {
        var titleEl = header.querySelector('.add-portal-title');
        var leftInfo = cardHeader.querySelector('.itinerary-header-left');
        if (titleEl && leftInfo) {
          titleEl.textContent = leftInfo.textContent.trim().replace(/\\s+/g, ' ');
        }
        var subEl = header.querySelector('.add-portal-subtitle');
        if (subEl) subEl.style.display = 'none';
      }
    }

    if (overlay) overlay.classList.add('add-no-bottom-nav');
    var nav = document.getElementById('add-portal-nav');
    if (nav) nav.classList.remove('add-nav-visible');
    if (overlay) overlay.scrollTop = 0;
  }
}

function add_closePortal() {
  var overlay = document.getElementById('add-portal-overlay');
  var currentEntry = add_navStack.length > 0 ? add_navStack[0] : null;
  var currentSectionId = currentEntry ? currentEntry.sectionId : null;

  if (!overlay || !currentSectionId) return;

  // Closing animation
  overlay.classList.add('add-portal-closing');

  setTimeout(function() {
    // Return section to original parent
    add_returnSection(currentSectionId);

    // Restore all sections in wrapper
    add_restoreAllInWrapper();

    // Clear portal content
    var portalContent = document.getElementById('add-portal-content');
    if (portalContent) portalContent.innerHTML = '';

    // Hide overlay
    overlay.classList.remove('add-portal-open');
    overlay.classList.remove('add-portal-closing');
    overlay.classList.remove('add-no-bottom-nav');

    // Hide bottom nav
    var nav = document.getElementById('add-portal-nav');
    if (nav) nav.classList.remove('add-nav-visible');

    // Restore body scroll
    document.body.style.overflow = '';

    // Collapse expanded day cards
    var expandedCards = document.querySelectorAll('.day-card.add-day-expanded');
    for (var i = 0; i < expandedCards.length; i++) {
      expandedCards[i].classList.remove('add-day-expanded');
    }

    // Reset nav stack
    add_navStack = [];

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'instant' });
  }, 300);
}

function add_switchPortalSection(sectionId) {
  var currentEntry = add_navStack.length > 0 ? add_navStack[add_navStack.length - 1] : null;
  var currentSectionId = currentEntry ? currentEntry.sectionId : null;

  if (!currentSectionId || sectionId === currentSectionId) return;

  var portalContent = document.getElementById('add-portal-content');
  if (!portalContent) return;

  // Return current section to original parent
  add_returnSection(currentSectionId);

  // Reset stack to new section at L2
  add_navStack = [{level: 2, sectionId: sectionId}];

  // Prepare new section
  var prepared = add_prepareSection(sectionId);
  if (!prepared) return;

  // Clear portal content
  portalContent.innerHTML = '';

  // Build and add portal header
  var header = add_buildPortalHeader(sectionId, 2);
  if (header) {
    portalContent.appendChild(header);
  }

  // Move section into portal
  portalContent.appendChild(prepared);

  // Add fade-in animation
  prepared.classList.add('add-portal-section-enter');
  setTimeout(function() {
    prepared.classList.remove('add-portal-section-enter');
  }, 300);

  // Update nav
  add_updateNav(sectionId);

  // Show bottom nav (switching always goes to L2)
  var overlay = document.getElementById('add-portal-overlay');
  if (overlay) {
    overlay.classList.remove('add-no-bottom-nav');
  }
  var nav = document.getElementById('add-portal-nav');
  if (nav) nav.classList.add('add-nav-visible');

  // Scroll overlay to top
  if (overlay) overlay.scrollTop = 0;

  // Re-trigger fade-in animations
  var fadeEls = prepared.querySelectorAll('.fade-in');
  for (var i = 0; i < fadeEls.length; i++) {
    fadeEls[i].classList.add('visible');
  }

  // Animate temp bars if temperature section
  if (sectionId === 'temperature' && typeof animateTempBars === 'function') {
    setTimeout(animateTempBars, 300);
  }

  // Update checklist progress if checklist section
  if (sectionId === 'checklist' && typeof updateChecklistProgress === 'function') {
    setTimeout(updateChecklistProgress, 100);
  }
}

function add_initPortal() {
  add_checkMobile();

  // Store all parents upfront
  add_storeAllParents();

  // Bind entry card clicks
  var cards = document.querySelectorAll('.add-entry-card');
  for (var i = 0; i < cards.length; i++) {
    cards[i].addEventListener('click', function() {
      var target = this.getAttribute('data-target');
      if (target) add_openPortal(target);
    });
  }

  // Bind bottom nav clicks
  var navItems = document.querySelectorAll('.add-portal-nav-item');
  for (var j = 0; j < navItems.length; j++) {
    navItems[j].addEventListener('click', function() {
      var target = this.getAttribute('data-target');
      if (target) add_switchPortalSection(target);
    });
  }

  // Handle resize: reset portal on desktop
  var resizeTimer;
  window.addEventListener('resize', function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function() {
      var wasMobile = add_isMobileView;
      add_checkMobile();
      if (!add_isMobileView && add_navStack.length > 0) {
        add_closePortal();
      }
    }, 250);
  });
}

// Init on DOMContentLoaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', function() {
    add_initPortal();
  });
} else {
  add_initPortal();
}

// ===== V17 Portal View System 结束 ====="""

content = content[:start_idx] + new_js + content[end_idx:]

# ============================================================
# 7. Update portal system comments
# ============================================================
content = content.replace(
    '/* ===== V16 Portal View System Start ===== */',
    '/* ===== V17 Portal View System Start ===== */'
)
content = content.replace(
    '/* ===== V16 Portal View System End ===== */',
    '/* ===== V17 Portal View System End ===== */'
)

# ============================================================
# 8. Also update the CSS comment
# ============================================================
content = content.replace(
    '// ===== V16 Portal View System 开始 =====',
    '// ===== V17 Portal View System 开始 ====='
)

# ============================================================
# Write result
# ============================================================
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("V17 upgrade complete!")
print("File size:", len(content.encode('utf-8')), "bytes")
