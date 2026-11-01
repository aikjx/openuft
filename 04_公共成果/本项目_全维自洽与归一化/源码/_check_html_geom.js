// 通用 HTML 几何体检（Node 桩）——按各 svg 自身 viewBox 校验，不截图
// 校验项：坐标有限且落在 [0,W]/[0,H]；rect 宽高非负且非零；rect 右/下边界不越界；
//         path 采样点不越界；表格容器 innerHTML 已填充且无 NaN/undefined。
const fs = require('fs');
const path = process.argv[2];
if (!path) { console.log('用法: node _check_html_geom.js <file.html>'); process.exit(2); }
const html = fs.readFileSync(path, 'utf8');

// 1) 解析每个 svg 的 viewBox
const VB = {};
const reSvg = /<svg\s+id="([^"]+)"\s+viewBox="0 0 ([\d.]+) ([\d.]+)"/g;
let m;
while ((m = reSvg.exec(html)) !== null) VB[m[1]] = [parseFloat(m[2]), parseFloat(m[3])];
if (!Object.keys(VB).length) { console.log('FAIL 未解析到任何 <svg id=... viewBox="0 0 W H">'); process.exit(2); }

// 2) 抽出内联脚本
const sm = html.match(/<script>([\s\S]*?)<\/script>/);
if (!sm) { console.log('FAIL 未找到内联 script'); process.exit(2); }
const code = sm[1];

// 3) DOM 桩
const rec = {};          // id -> 记录到的图元
const box = {};          // id -> 容器对象
function mkEl(tag) {
  const o = {
    tag, attrs: {}, children: [], textContent: '',
    setAttribute(k, v) { this.attrs[k] = String(v); },
    appendChild(c) { this.children.push(c); return c; }
  };
  return o;
}
global.document = {
  createElementNS(ns, tag) {
    const e = mkEl(tag);
    // 图元要同时进「当前 svg」的记录表
    const orig = e.appendChild.bind(e);
    e.appendChild = function (c) { return orig(c); };
    return e;
  },
  createElement(tag) { return mkEl(tag); },
  getElementById(id) {
    if (!box[id]) {
      box[id] = {
        id, innerHTML: '', children: [],
        appendChild(c) {
          this.children.push(c);
          if (rec[id]) rec[id].push(c);
          return c;
        }
      };
      rec[id] = [];
    }
    return box[id];
  }
};

// 4) 跑脚本；appendChild 时把图元归到「最近一次 getElementById 的 svg」
let cur = null;
const gid = global.document.getElementById.bind(global.document);
global.document.getElementById = function (id) { cur = id; return gid(id); };
const _origCreate = global.document.createElementNS;
global.document.createElementNS = function (ns, tag) {
  const e = _origCreate(ns, tag);
  const push = e.appendChild.bind(e);
  e.appendChild = function (c) { return push(c); };
  // 包一层：appendChild 到 svg 容器时由容器负责记录
  return e;
};

let err = 0;
try {
  eval(code);
} catch (e) {
  console.log('FAIL 脚本抛异常:', e.message);
  process.exit(2);
}

// 5) 逐 svg 校验
for (const id of Object.keys(VB)) {
  const [W, H] = VB[id];
  // 从容器 children 里取图元（appendChild 已记录）
  const items = (box[id] && box[id].children) || [];
  if (!items.length) { console.log(`FAIL ${id} 无任何图元（viewBox ${W}x${H}）`); err++; continue; }
  const bad = [];
  const seen = new Set();
  for (const el of items) {
    if (seen.has(el)) continue;
    seen.add(el);
    const a = el.attrs || {};
    const num = (k) => (a[k] === undefined ? undefined : parseFloat(a[k]));

    // 单点坐标
    const pts = [['cx', W], ['cy', H], ['x', W], ['y', H],
                 ['x1', W], ['y1', H], ['x2', W], ['y2', H]];
    for (const [k, lim] of pts) {
      const v = num(k);
      if (v === undefined) continue;
      if (!isFinite(v)) bad.push(`${el.tag}.${k}=${a[k]} 非有限`);
      else if (v < -2 || v > lim + 2) bad.push(`${el.tag}.${k}=${v} 越界(0..${lim})`);
    }
    const r = num('r');
    if (r !== undefined && (!isFinite(r) || r < 0)) bad.push(`${el.tag}.r=${a.r} 非法`);

    // 矩形：宽高 + 边界
    if (el.tag === 'rect') {
      const w = num('width'), h = num('height'), x = num('x'), y = num('y');
      if (!isFinite(w) || !isFinite(h)) bad.push('rect width/height 非有限');
      else {
        if (w < 0) bad.push(`rect.width=${w} 为负（坐标系方向算反）`);
        if (h < 0) bad.push(`rect.height=${h} 为负`);
        if (w === 0) bad.push(`rect(fill=${a.fill}) 宽度为 0 ⇒ 不可见`);
        if (h === 0 && a.fill !== undefined) bad.push(`rect(fill=${a.fill}) 高度为 0 ⇒ 不可见`);
        if (isFinite(x) && x + Math.max(w, 0) > W + 2) bad.push(`rect 右边界 ${(x + w).toFixed(1)} 越界 W=${W}`);
        if (isFinite(y) && y + Math.max(h, 0) > H + 2) bad.push(`rect 下边界 ${(y + h).toFixed(1)} 越界 H=${H}`);
      }
    }

    // path
    if (a.d) {
      const nums = (a.d.match(/-?\d+(?:\.\d+)?/g) || []).map(Number);
      for (let i = 0; i + 1 < nums.length; i += 2) {
        const x = nums[i], y = nums[i + 1];
        if (!isFinite(x) || !isFinite(y)) { bad.push('path 含 NaN'); break; }
        if (x < -2 || x > W + 2 || y < -2 || y > H + 2) { bad.push(`path 点(${x},${y}) 越界`); break; }
      }
    }
  }
  console.log(`${id} (${W}x${H}): 图元 ${seen.size} 个, 越界 ${bad.length}`);
  bad.slice(0, 6).forEach(b => console.log('   ! ' + b));
  if (bad.length) err++;
}

// 6) 非 svg 容器（表格）必须被填充
for (const id of Object.keys(box)) {
  if (VB[id]) continue;
  const s = box[id].innerHTML || '';
  if (s.length < 10) { console.log(`FAIL 容器 ${id} innerHTML 过短(${s.length}) ⇒ 未填充`); err++; }
  if (/NaN|undefined/.test(s)) { console.log(`FAIL 容器 ${id} 含 NaN/undefined`); err++; }
}

console.log(err === 0 ? 'GEOMETRY-OK rc=0' : `GEOMETRY-FAIL rc=${err}`);
process.exit(err === 0 ? 0 : 2);
