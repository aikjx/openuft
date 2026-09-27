#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""读取 V3.2_Qball_scan.json / V3.2_radiation.json，生成自包含可视化 HTML 落进 openuft。"""
import json, os

base = os.path.dirname(os.path.abspath(__file__))
scan = json.load(open(os.path.join(base, "V3.2_Qball_scan.json"), encoding="utf-8"))
rad  = json.load(open(os.path.join(base, "V3.2_radiation.json"), encoding="utf-8"))

rows  = [r for r in scan["rows"] if r.get("converged")]
om    = [r["omega"] for r in rows]
eq    = [r["EQ"] for r in rows]
q     = [r["Q"] for r in rows]
mdp   = rad["model_rows"]
meps  = [m["eps"] for m in mdp]
mdpp  = [m["dP_over_P"] for m in mdp]

def arr(x): return "[" + ",".join(("%.6f" % v) for v in x) + "]"

html = """<!DOCTYPE html>
<html lang="zh" style="margin:0;padding:0;">
<head><meta charset="utf-8">
<title>TUFT V3.2 方向B · Q-ball 解族与加速辐射</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
<style>html,body{height:100%;margin:0;font-family:system-ui,Segoe UI,Microsoft YaHei,sans-serif;background:#fff}
.c{width:96%;max-width:1100px;margin:14px auto}.t{font-size:15px;font-weight:600;margin:10px 2px 2px}
.s{font-size:11px;color:#666;margin:0 2px 6px}.chart{width:100%;height:400px}
.note{font-size:11px;color:#555;line-height:1.5;margin:8px 2px 18px;border-left:3px solid #ddd;padding-left:8px}</style>
</head><body>
<div class="c"><div class="t">Q-ball 解族与稳定性边界（omega 全谱）</div>
<div class="s">修复候选 V1=1.2/V2=0.4/M2=0.4，c=1 天然单位 · 数据：V3.2_Qball_scan.json · 红线：L3=0，示范参数非粒子身份</div>
<div id="c1" class="chart"></div>
<div class="note">E0/Q 呈 U 形：最小 0.434@omega~0.184（Q 极大点）；对照衰变阈值 m=sqrt(M2/2)=0.4472（红色虚线），电荷稳定窗仅 omega 属于[0.18,0.25]，余量约3%；低/高 omega 端可衰变。Q=2omegaN 在 omega~0.184 取极大233，dE0/dQ~omega 校验比值0.76-0.99。</div></div>
<div class="c"><div class="t">形变源附加辐射 deltaP/P vs 非绝热形变参数 eps=a*R_core/c^2</div>
<div class="s">deltaP/P=K*eps^2（K=1 示意）· 数据：V3.2_radiation.json · 刚性共加速 deltaP=0（形状无关）</div>
<div id="c2" class="chart"></div>
<div class="note">deltaP 只来自内部形变：eps-&gt;0（弱加速/小尺寸）deltaP-&gt;0 与来稿弱极限一致；eps=0.1-&gt;1%、0.5-&gt;25%、1-&gt;100%（饱和前）。③ 为构造模型（B 级），deltaP 绝对系数 K 待动力学/全时域仿真确认。</div></div>
<script>
var om=@@OM@@, eq=@@EQ@@, q=@@Q@@, meps=@@MEPS@@, mdpp=@@MDPP@@;
var m=0.447214;
var opt1={tooltip:{trigger:'axis',triggerOn:'mousemove|click',renderMode:'richText',confine:true},
 grid:{left:52,right:52,top:36,bottom:40,containLabel:true},
 legend:{top:4,itemWidth:13,itemHeight:10,textStyle:{fontSize:11}},
 xAxis:{type:'value',name:'omega',nameTextStyle:{fontSize:11},axisLabel:{fontSize:11}},
 yAxis:[{type:'value',name:'E0/Q',nameTextStyle:{fontSize:11},axisLabel:{fontSize:11},min:0.3,max:1.6},
        {type:'value',name:'Q',nameTextStyle:{fontSize:11},axisLabel:{fontSize:11}}],
 series:[
  {name:'E0/Q',type:'line',data:om.map(function(x,i){return [x,eq[i]]}),smooth:true,symbolSize:6,lineStyle:{width:2},
   markLine:{symbol:'none',label:{formatter:'decay threshold m=0.447',fontSize:10,position:'insideEndTop'},
     data:[{yAxis:m,lineStyle:{type:'dashed',color:'#c00'}}]}},
  {name:'Q',type:'line',yAxisIndex:1,data:om.map(function(x,i){return [x,q[i]]}),smooth:true,symbolSize:6,lineStyle:{width:2}}
 ]};
var opt2={tooltip:{trigger:'axis',triggerOn:'mousemove|click',renderMode:'richText',confine:true},
 grid:{left:52,right:24,top:36,bottom:40,containLabel:true},
 legend:{top:4,itemWidth:13,itemHeight:10,textStyle:{fontSize:11}},
 xAxis:{type:'value',name:'eps=a*R_core/c^2',nameTextStyle:{fontSize:11},axisLabel:{fontSize:11},max:1.1},
 yAxis:{type:'value',name:'deltaP/P',nameTextStyle:{fontSize:11},axisLabel:{fontSize:11},min:0},
 series:[{name:'deltaP/P=K*eps^2',type:'line',data:meps.map(function(x,i){return [x,mdpp[i]]}),smooth:true,symbolSize:6,lineStyle:{width:2}}]};
var c1=echarts.init(document.getElementById('c1'));c1.setOption(opt1);
var c2=echarts.init(document.getElementById('c2'));c2.setOption(opt2);
window.addEventListener('resize',function(){c1.resize();c2.resize();});
</script>
</body></html>
"""
html = (html.replace("@@OM@@", arr(om)).replace("@@EQ@@", arr(eq))
            .replace("@@Q@@", arr(q))
            .replace("@@MEPS@@", arr(meps)).replace("@@MDPP@@", arr(mdpp)))

out = os.path.join(base, "V3.2_全谱与辐射_可视化.html")
with open(out, "w", encoding="utf-8") as fh:
    fh.write(html)
print("written:", out, len(html), "bytes")
