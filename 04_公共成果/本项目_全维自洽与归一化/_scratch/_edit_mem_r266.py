# -*- coding: utf-8 -*-
# 更新 MEMORY.md：r266 登记。Edits 1/2 用字符串替换；Edit 3 用行定位插入（避免整行精确匹配）。
import io, os, shutil, sys
MEM = os.path.join("D:/a10/aikjx/code/my_lib/.workbuddy/memory/MEMORY.md")
BAK = os.path.join("D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/_scratch","_MEMORY_before_r266_edit.md")
if not os.path.exists(BAK):
    shutil.copy(MEM, BAK)
s = io.open(MEM, encoding="utf-8", newline="").read()

# Edit 1: 下一轮字段
o1 = "- 已占卷 **r243–r265**（r246 是正式卷·观测统计层；r247 元审计层已补登 README）。**下一轮 r266 起，但必先实测 r266/r267/r268，度数须经 G13/GU08 机器核定。**"
n1 = "- 已占卷 **r243–r266**（r246 是正式卷·观测统计层；r247 元审计层已补登 README；**r266 力的大统一方程层·SURVIVE>0 不占度**）。**下一轮 r267 起，但必先实测 r267/r268/r269，度数须经 G13/GU08 机器核定。**"
assert s.count(o1)==1, ("EDIT1", s.count(o1))
s = s.replace(o1, n1)

# Edit 2: 不计入度数链者
o2 = "★**不计入度数链者**：r252 / r254 / r255 / r258 / r262 / r265（SURVIVE>0 或 PASS 型复现层）。"
n2 = "★**不计入度数链者**：r252 / r254 / r255 / r258 / r262 / r265 / r266（SURVIVE>0 或 PASS 型复现层；r266 候选 37 度但 SURVIVE>0 不占）。"
assert s.count(o2)==1, ("EDIT2", s.count(o2))
s = s.replace(o2, n2)

# Edit 3: 在 section 四 末尾（r265 一句话之后）插入 r266 一句话
r266_line = ("  - r266 力的大统一方程（V9.3 第九章）：★★★**数值复现高保真**——§9.4 F_E=230.71 N / F_G=-1.867e-34 N / 比值 1.2356e36 与独立 SI 库仑/牛顿重算完全一致；§9.3 强/弱力程 lambda 即 pi0/W 康普顿波长（标准物理）。★★★**结构判词：『力的大统一』= Yukawa/Proca 模板重包装**——四力共用 F=s hbar c q1 q2 (1/r^2+1/(lambda r)) e^{-r/lambda}，力程差别仅由 lambda（媒介子康普顿波长）定，非第一性原理推导。★★**几何本源(V7)=定义恒等式**：q_G=m/m_P 代入即 F=G m1 m2/r^2，残差精确 0；与 r264「内生=0」一致，常数层仍外部输入（书自承 B01-B03）。★**唯一诚实偏差**：弱力灭绝书值 1.25e-177 vs 精确 1.12e-177（约 12% 取整），量级一致；★**书诚实声明玩具耦合**（g^2=179.7、g_W^2=1 仅方法演示）=> 对靶有利。★条目 10（PASS 10/FAIL 0）、控制组 4/4、守卫 5/5、rc=0；定价 2^1=2 严格 SURVIVE 2/0 => **SURVIVE>0 => 不占度数链（候选 37 度但不占）**。")
lines = s.split("\n")
idx = [i for i,ln in enumerate(lines) if ln.startswith("- r265 引力波预言：")]
assert len(idx)==1, ("EDIT3 anchor", len(idx))
ins = idx[0]+1
# 若该行后已是 r266（幂等保护）则跳过
if not (ins < len(lines) and lines[ins].startswith("  - r266 力的大统一方程")):
    lines.insert(ins, r266_line)
s = "\n".join(lines)

io.open(MEM, "w", encoding="utf-8", newline="").write(s)
print("MEMORY.md updated OK")
