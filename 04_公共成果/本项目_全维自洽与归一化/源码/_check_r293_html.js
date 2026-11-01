// 坐标域体检（Node 桩）——不截图，直接跑内联脚本并检查每个几何量是否落在 viewBox 内
const fs = require('fs');
const path = process.argv[2];
const html = fs.readFileSync(path, 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.log('FAIL 未找到内联 script'); process.exit(2); }
const code = m[1];

const rec = {};   // svgId -> [{tag, attrs}]
let curSvg = null;

function mkEl(tag) {
  const o = { tag, attrs: {}, children: [], textContent: '',
    setAttribute(k, v) { this.attrs[k] = v; },
    appendChild(c) { this.children.push(c); if (curSvg) rec[curSvg].push(c); return c; }
  };
  return o;
}

const svgById = {};
global.document = {
  createElementNS(ns, tag) { return mkEl(tag); },
  createElement(tag) { return mkEl(tag); },
  getElementById(id) {
    if (!svgById[id]) {
      svgById[id] = { id, innerHTML: '', children: [], appendChild(c) { this.children.push(c); if (rec[id]) rec[id].push(c); } };
      rec[id] = [];
    }
    curSvg = id;
    return svgById[id];
  }
};

// 每个 svg 的 viewBox 高度
const VB = { svgMain: [680, 300], svgRuler: [680, 150], svgPool: [680, 150] };

let err = 0;
try {
  // 重置 curSvg 语义：脚本里先 getElementById 再 appendChild
  eval(code);
} catch (e) {
  console.log('FAIL 脚本抛异常:', e.message);
  process.exit(2);
}

for (const id of Object.keys(VB)) {
  const [W, H] = VB[id];
  const items = rec[id] || [];
  if (!items.length) { console.log(`FAIL ${id} 无任何图元`); err++; continue; }
  let bad = [];
  for (const el of items) {
    const a = el.attrs;
    // 数值型几何量
    const checks = [];
    if (a.cx !== undefined) checks.push(['cx', +a.cx, W]);
    if (a.cy !== undefined) checks.push(['cy', +a.cy, H]);
    if (a.x !== undefined) checks.push(['x', +a.x, W]);
    if (a.y !== undefined) checks.push(['y', +a.y, H]);
    if (a.x1 !== undefined) checks.push(['x1', +a.x1, W]);
    if (a.y1 !== undefined) checks.push(['y1', +a.y1, H]);
    if (a.x2 !== undefined) checks.push(['x2', +a.x2, W]);
    if (a.y2 !== undefined) checks.push(['y2', +a.y2, H]);
    if (a.r !== undefined) checks.push(['r', +a.r, Math.min(W, H)]);
    for (const [k, v, lim] of checks) {
      if (!isFinite(v)) bad.push(`${el.tag}.${k}=${v} 非有限`);
      else if (v < -2 || v > lim + 2) bad.push(`${el.tag}.${k}=${v} 越界(0..${lim})`);
    }
    // 矩形：宽高必须非负，且 x+w / y+h 不得越界（本卷曾因 x 轴反向把两个底色分区算成负宽 ⇒ 宽度退化为 0、分区整个消失）
    if (el.tag === 'rect') {
      const w = +a.width, h = +a.height, x = +a.x, y = +a.y;
      if (!isFinite(w) || !isFinite(h)) bad.push('rect width/height 非有限');
      else {
        if (w < 0) bad.push(`rect.width=${w} 为负（坐标系方向算反）`);
        if (h < 0) bad.push(`rect.height=${h} 为负`);
        if (w === 0) bad.push(`rect(${a.fill}) 宽度为 0 ⇒ 该图元不可见`);
        if (x + w > W + 2) bad.push(`rect 右边界 ${(x + w).toFixed(1)} 越界 W=${W}`);
        if (y + h > H + 2) bad.push(`rect 下边界 ${(y + h).toFixed(1)} 越界 H=${H}`);
      }
    }
    // path d
    if (a.d) {
      const nums = a.d.match(/-?\d+(\.\d+)?/g) || [];
      for (let i = 0; i < nums.length; i += 2) {
        const x = +nums[i], y = +nums[i + 1];
        if (!isFinite(x) || !isFinite(y)) { bad.push('path 含 NaN'); break; }
        if (x < -2 || x > W + 2 || y < -2 || y > H + 2) { bad.push(`path 点(${x},${y}) 越界`); break; }
      }
    }
  }
  console.log(`${id}: 图元 ${items.length} 个, 越界 ${bad.length}`);
  bad.slice(0, 6).forEach(b => console.log('   ! ' + b));
  if (bad.length) err++;
}

// 表格类容器文本体检
for (const id of Object.keys(svgById)) {
  if (VB[id]) continue;
  const c = svgById[id];
  if (c.innerHTML === undefined) { console.log(`FAIL ${id} 未填充 innerHTML`); err++; }
  else if (c.innerHTML.length < 10) { console.log(`WARN ${id} innerHTML 过短 (${c.innerHTML.length})`); }
}

// 关键字符体检：确保没有 NaN / undefined 漏进 HTML
for (const id of Object.keys(svgById)) {
  const s = svgById[id].innerHTML || '';
  if (/NaN|undefined/.test(s)) { console.log(`FAIL ${id} 含 NaN/undefined`); err++; }
}
console.log(err === 0 ? 'GEOMETRY-OK rc=0' : `GEOMETRY-FAIL rc=${err}`);
process.exit(err === 0 ? 0 : 2);
