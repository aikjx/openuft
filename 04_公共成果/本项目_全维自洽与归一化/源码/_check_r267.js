// r267 HTML 图载体检：假 document + 记录型 canvas ctx，逐点校验 isFinite 与越界。
const fs = require("fs");
const path = require("path");

const htmlPath = process.argv[2];
const html = fs.readFileSync(htmlPath, "utf8");

// 抽 <script> 内容（忽略含 src= 的外链）
const scripts = [];
const re = /<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;
let m;
while ((m = re.exec(html)) !== null) scripts.push(m[1]);
if (scripts.length === 0) { console.log("NO_SCRIPT"); process.exit(1); }

const calls = [];
let bad = 0;
let nonFinite = 0;
let outside = 0;

const W = 1040, H = 470; // cv1 尺寸；cv2 通过 canvas 元素自带尺寸区分
function mkCtx(w, h) {
  return {
    fillStyle: "", strokeStyle: "", font: "", textAlign: "", textBaseline: "",
    beginPath() { calls.push(["beginPath"]); },
    moveTo(x, y) { rec("moveTo", x, y, w, h); },
    lineTo(x, y) { rec("lineTo", x, y, w, h); },
    stroke() { calls.push(["stroke"]); },
    fillRect(x, y, ww, hh) {
      // 只看矩形的两个对角点是否落在画布内
      rec("fillRect", x, y, w, h);
      rec("fillRect.end", x + ww, y + hh, w, h);
    },
    fillText(t, x, y) { calls.push(["fillText", String(t)]); rec("fillText", x, y, w, h); },
    measureText(t) { return { width: String(t).length * 6 }; },
    clearRect() {}, save() {}, restore() {},
  };
}
function rec(kind, x, y, w, h) {
  calls.push([kind, x, y]);
  if (!isFinite(x) || !isFinite(y)) { nonFinite++; console.log("NONFINITE", kind, x, y); return; }
  if (x < -1 || x > w + 1 || y < -1 || y > h + 1) {
    outside++;
    if (outside <= 6) console.log("OUTSIDE", kind, x.toFixed(2), y.toFixed(2), "box", w, h);
  }
}

const canvases = {};
for (const mm of html.matchAll(/<canvas[^>]*id="([^"]+)"[^>]*width="(\d+)"[^>]*height="(\d+)"/g)) {
  canvases[mm[1]] = { width: +mm[2], height: +mm[3] };
}
if (Object.keys(canvases).length === 0) { console.log("NO_CANVAS"); process.exit(1); }

global.document = {
  getElementById(id) {
    const c = canvases[id];
    if (!c) return null;
    return { width: c.width, height: c.height, getContext() { return mkCtx(c.width, c.height); } };
  },
};

let err = null;
try {
  for (const s of scripts) { (0, eval)(s); }
} catch (e) {
  err = e;
}

console.log("canvases:", JSON.stringify(canvases));
console.log("calls:", calls.length);
console.log("nonFinite:", nonFinite);
console.log("outside:", outside);
console.log("error:", err ? String(err) : "none");
console.log("placeholders_left:", (html.match(/__[A-Z]+__/g) || []).length);
console.log("verdict:", (!err && nonFinite === 0 && outside === 0) ? "OK" : "BAD");
process.exit((!err && nonFinite === 0 && outside === 0) ? 0 : 2);
