# -*- coding: utf-8 -*-
r"""R11、R12、R13、R14、R15、R16 与 R17 七层判据的**外部**变异核验：从引擎外面改那几条算术，看谁变红。

为什么要有这个脚本：R11 的判据（$N\mid 3Q$）此前只在引擎内部被自己的门禁对照过，
"把它写错会不会有人发现"只存在于某一次对话的口头里 —— 而一个没人能重跑的读数等于没人看守。
本脚本把 `验证脚本/so10_reps.py` 连同它的依赖 `so10_chain.py` 整份复制进临时目录，
在副本上植入缺陷，再重跑整台引擎（副本的产出只落在它自己的目录里，不碰仓库那份报告），
要求三件事同时成立：

  * 基线（未植入）全绿，且它打印的门禁总数与磁盘上 `SO10表示论报告.json` 里的 `tests`
    条数**相等** —— 这条不是装饰：引擎的层是短路接线的（`sel_ok = run_selection_layer() if res_ok`），
    依赖缺失时它会只跑前几层就退出，若只要求"退出码非 0"就会把这种夹具塌陷当成捕获；
  * 每个变异体都必须被**点名到它那一层**（R11.x、R12.x、R13.x、R14.x、R15.x、R16.x 或 R17.x，由每例自带的 `layer` 决定，
    不是"任何一个 FAIL"）抓住（崩溃不算捕获），且它打印的读数至少动一个
    —— 门禁 PASS 数、或报告 §10 那句"允许 X 条、禁戒 Y 条"、或报告 §11 的三个读数
    （$\Gamma$ 的阶、$|\Gamma|$ 三条出处那一列、§11.5 那两条独立判法的同判列）、
    或报告 §12 的六个读数（候选群阶、核 $K$ 与其阶分布、同构型种数、集合相等的通道比、
    唯一例外的承载者、物质字称实现者个数）、
    或报告 §13 的十三处读数（乙账"甲账没有"的条件数、同态引理的比对方数与违例对数、形变加法
    的例外对数、三条恒等事的违例三元组、§13.3 那张三条路 × 两种约定的核表、§13.4 的
    "全部条件/单条最好/贪心核心/只半单/只 $U(1)$/两半之交"六张行数、两条即钉住的条件对数与
    总对数、§13.5 的四档网格行数与候选元数）、
    或报告 §14 的七处读数（那张整节表格行的行数与摘要、共轭对合的四处归零计数器、洛伦兹账三条
    机器的违例对、"标量半边为奇"那条机理等式的成立性、覆盖面的档数/类数/$d_{\min}$ 上下端、
    "只取非点号字母的那 8 条与 §10 集合相等"那三元组、$d=5$ 档不碰 $\nu^c$ 的那对计数），
    或报告 §14.8 的七处读数（四路核对"违例 N 条"那一半、$n=0..6$ 那张缩法表的七行、逐档缩法表的
    六行、"共给 2261 条／低估 668 条／最大重数 2"那一组、§10 接缝那对 $(8,2)$、"多缩法恰 16 条
    $=$ 8 加 8"那三元组、塔的逐层四读数 2261→8874→57735→467236），
    或报告 §14.9 的八处读数（三路互不等条数、"无重复名字必须退回缩法重数"的违例条数、
    $n\le6$ 那张 $(n,\text{组大小})$ 表的 30 行行集合摘要、四条教科书锚点的三路读数、
    "共 838 类／缩法 1028 条／剩 838 条／吃掉 190 条／$\times0.8152$"那一组、六个分区数的方括号、
    §10 接缝那句"结构数从 16 到 8"、管辖范围那句"$k_{\min}\ne0$ 的 755 类／1233 条"）。
    §14、§14.8 与 §14.9 三者分开切片：逐档表那种 `$n_f=…$、$n_s=…$` 打头的六列行在 §14 里另有六行，
    整节切片会串味（实测 12 行 vs 本节 6 行）；§14.9 那张三路表里"同名组大小"恰好是纯数字的那些行
    （$n=3$ 的 $3/2$、$n=4$ 的 $3$、$n=6$ 的 $4/3/2$）与 §14.8 的 $n=0..6$ 表**同形**（五个数字格），
    §14.8 的切片若一路取到 `## 15.` 就会把这两张表并成一张 $\Rightarrow$ 切片边界改为 `### 14.9`。
    这一条不是形式：只动三条路径里浮点那条的滑倒**不动**判决表（甲/乙仍然同意），动的是"甲乙丙一致"那条断言 $\Rightarrow$
    同一个数为什么要三台互不共享算术的机器各跑一遍，这里有一次实测读数；R13 的 h1 是同一族：
    路丙的 triality 号只出现在断言里、不出现在 §12 的任何数字里 $\Rightarrow$ 它动的只有 PASS 数，
    这正好把"门禁在看守报告里看不见的断言"这件事本身变成了读数；
  * 一条良性改动（只补尾注释，语义不动）不得误报，否则这台仪器是"永远红"而不是"能红"。
    良性例现在七层各一条：只测 R11 那侧的良性改动，等于没核对 §11、§12、§13、§14、§14.8 与 §14.9
    的读数在语义不动时**不**动。

R12 那四个变异体各自钉住报告 §11 的一个断言，且都落在**门禁**上而不是 `assert` 上 $\Rightarrow$
"报错"不会被当成"捕获"：色 $\mathbb Z_3$ 生成元换掉后两支不再互化（R12.1 的约定无关那条）、
阿贝尔群的元素阶多重集把单位元读成最大阶（R12.1 的"唯一命中"）、格的指数把不变因子**取和**
而不是取积（R12.2 的三条出处同数）、"在不在根格里"的第二条判法把坐标和的奇偶改成模 3
（R12.0 的两条独立判法同判）。

R13 那四个变异体同样落在门禁上，各自钉住 §12 的一个断言：路丙的标准 triality 号把 $3b$ 写成
$2b$ $\Rightarrow$ 丙与格读数不再成 $q_{\rm lat}\equiv 3q_{\rm std}$（R13.1，只动 PASS 数，见上）；
色类阶的枚举把类元读成对角粘合元（第 $ci$ 类的阶读成 $(ci,1,1)$ 的阶）$\Rightarrow$ §12.1 类表
"阶"列整体漂移、违背 `vords == [1,2,4,4]`（R13.0，动类表阶列）；注：这个位置第一轮植的是
"核的枚举少看在场谱的行"，两轮实测都是**中性变异**——少看 1 行、少看 10 行核都不动（核约束在
前 20 行已闭合），而真能把核放松的取法会先把通道循环的"陪集数 $\times|K|=$ 存活数"结构断言打断
$\Rightarrow$ 按本仪器"崩溃不算捕获"的规则，R13.2 的核枚举**无法从外面植红**，这条空白登记在
docstring 而不是台账；正向对照把"只弱 $\cap$ 只色"的两半**交集**写成**并集**
$\Rightarrow$ 半群读数退化、"全组允许 $=$ 两半交集"在多数通道不再成立（R13.6，动 §12.6 的通道比与
例外计数；第一轮这里植入的是"色半 and→or"，它把读数推到**零例外**，撞上引擎 claim 里那句
无守卫的 `exc[0]` ⇒ 引擎以 traceback 而非 FAIL 退出、被本仪器按规则判为未捕获——**这是一次
真伤，已由 `excpart` 三分支守卫修复**，仪器随后才改判得动）；
物质字称的实现者把相位判据取反（只数"逐场都 $\ne$ 目标相位"的元）$\Rightarrow$ 补集整批涌进来、
实现者个数偏离恰 2（R13.4，动 §12.4 的实现者数；注：第一版这里是"只按前 3 个场试"，实测前 3
个场就已把实现者钉成那 2 个 $\Rightarrow$ 中性变异，已换成取反版）。良性例 b3 给 `Kset = set(K)`
补尾注释，语义不动。

R14 那五个变异体落在 §13 的五处算术语境上，各自钉住该层的一条断言，且同样只落在**门禁**上：
乙账"其中多少条甲账没有"把差集读成交集（`set(condB) - set(spec)` 写成 `& set(spec)` ⇒ 304 掉到
61，R14.1 的"乙账严格更细"这一半不再成立）；子多重态内部"在不在根格里"那条判法把标签差向量循环
错位一位（$d_i$ 读成 $d_{i+1}$ ⇒ §13.2 的三条恒等事违例三元组从 0/0/0 变成 0/非零/0，而另两条
判法照旧干净 —— 这正是"三条判法各守一件事"的可证伪形式）；冗余度里"单条最好的一条"把 `min` 写成
`max`（R14.4 的 12 变成整格 432 ⇒ 那条"没有任何一条荷条件单独钉得住 $\Gamma$"被读成"最好的一条
恰好什么都不钉"）；形变的加法封闭性检查把 `not in charA` 写成 `in charA`（R14.0 的 158 对例外与
418 对命中整批互换 ⇒ 那条否定读数失去反向证据）；$t$ 网格把每档的周期 `den * CEN_U_PER` 写成
`den`（候选元数 216/432/864/2160 整体缩 3 倍 ⇒ "核不随网格走"这条对照连候选格都没数对）。
良性例 b4 给 `FULL = (1 << len(C)) - 1` 补尾注释，语义不动。

R15 那七个变异体落在 §14 的七处算术语境上，同样只落在**门禁**上：逐类单态结构总数去掉排列权重
（$\sum$ 单态数 而不乘 `perm_weight` ⇒ §14 那两张结构表的整列漂移）；"只取非点号字母"读成"至多含
一个点号字母"（`x['nd'] == 0` 写成 `<= 1` ⇒ 那句"扩基是超集、不是替换"的集合相等不再成立）；
"上移"读成"洛伦兹可行"（真值判 `x['kmin']` 换成 `is not None` ⇒ §14.3 的上移列读到别的数）；
群禁集合把"任一道判禁"读成"全部道判禁"（`any` 写成 `all` ⇒ §14.5 的群禁列与"指标禁 $=$ 群禁"
那条巧合整批改判）；"不碰 $\nu^c$（含其共轭）"读成名字恰等于 $\nu^c$（`'nu' in n` 写成
`n == 'nu^c'` ⇒ §14.6 那条"不碰"的计数改变）；覆盖面把 $d_{\min}$ 的上端读成下端（`maxd = max(`
写成 `min(` ⇒ "六档实际探到 $d=8$"被读成"只到 $d=3$"）；机理等式的"标量半边为奇"把 mod 2 写成
mod 4（⇒ §14.5 那条集合等式判成"不等"）。良性例 b5 给 §14 的 `key = lambda x: x['k']` 补尾注释，
语义不动。

R16 那六个变异体落在 §14.8 的六处算术语境上，同样只落在**门禁**上，且各自钉住该层的一条断言：
把"一类的缩法重数 $=$ 两侧各自接成自旋 $0$ 的重数之**积**"写成**和**（`cg_j0(nu+kk) * cg_j0(nd+kk)`
改成 `+` ⇒ R16.1 那句"只有 $1$ 条缩法 当且仅当 两侧指标数都不超过 $2$"不再成立，逐档表与
2261/668 整列漂移）；乙路二项式差把减号写成加号、丙路钩长公式把 $(m+1)!\,m!$ 写成 $m!\,m!$
（即把 Catalan 读成中心二项式）——这两条各钉一张票，动的都是"四路逐项相等、违例 0 条"里那
**违例**的一半（票与票之间不共享算术 ⇒ 一张票错不会连带别张票，正是"四张票"这句话的可证伪形式）；
丁路把对角余乘的**沿位累加**写成覆写（`row[...] += F(xv)` 改成 `=` ⇒ 方程组不再是
$\sum_i X^{(i)}T=0$ 而是"逐位单独归零"——**这正是本层写作时真踩过的那一处**，引擎里
`sl2_nullity` 的注释就是它留下的疤，故这一例是复现伤、不是虚构伤）；画线法那侧把
$\varepsilon_{10}$ 的 $-1$ 写成 $+1$（配对张量不再反对称 ⇒ 张成空间的秩与 Plücker 关系数一起动、
而 $(n-1)!!$ 那一列不动 —— 这条钉的是"三个画线法只撑出两个独立缩法"，也就是本节唯一一条
"多出来的关系"读数）；覆盖面把 $d\le6$ 读成 $d<6$（⇒ §14.8 那句"多缩法的类恰有 16 条 $=$ 8 条
无点号加其点号孪生 8 条"整批归零，"谁多重是边界清楚的一批"从此没有主体）。
良性例 b6 给 §14.8 的 `okc = [...]` 那行补一条尾部注释，语义不动。
一条如实登记的边界：甲路就是引擎原有的 `cg_j0`，它被全引擎共用 ⇒ 从外面改它会把别的层一起
拖红，测不到"本节这一张票"，所以甲路由 R16.0 里那句"四路在 $0..n$ 上逐项相等"反向看守
（乙丙丁任一错都让它变红），而不是由变异体看守。

R17 那五个变异体落在 §14.9 的四处算术语境上，同样只落在**门禁**上。前三个动的是那张
$(n,\text{组大小})$ 三路表：**丁**把 Grassmann 求值里的**逆序数符号**丢掉（`+ (c if inv % 2 == 0 else -c)`
写成 `+ c` ⇒ $\\varepsilon^{\\alpha\\beta}\\psi_\\alpha\\psi_\\beta$ 会读成 0，**这一处是本层写作时真踩过的伤**）
$\Rightarrow$ 只有丁那一列动三行（$(2,2)$ 的丁 1→0、$(6,2)$ 2→3、$(6,2+2+2)$ 1→0）、"三路互不等" 0→3，
两个锚点读成 (1,1,0) $\Rightarrow$ R17.0 与 R17.1 同红（137/139）；**乙**把 $\\Lambda^m(\\mathbb C^2)=0$ 的门槛从
$m\\ge3$ 抬到 $m\\ge4$ $\Rightarrow$ 只有乙那一列动四行（$(4,3)$、$(6,3)$、$(6,3+2)$、$(6,3+3)$ 的乙从 0 读成
1/2/1/1）、互不等 0→4，**锚点一个都不动**（四条锚点里没有"单一组三重同名"那一条）；**乙**再把
$m=2$ 那一格读成与 $m=1$ 同 $\Rightarrow$ 乙那一列动七行、互不等 0→7，两个锚点读成 (1,0,1)。
后两例动的都不是甲也不是丁 $\Rightarrow$ "三张互不共享算术的票"这句话的可证伪形式就是"改错一张、另两张照旧"。
**最要紧的是第四例**：把同名组的收集门槛 `v >= 2` 写成 `v >= 3`（成对的全同槽从此不再被反对称化）$\Rightarrow$
三路表**一字不动**、互不等仍是 0（甲乙丁读的是同一份组大小清单，三张票彼此**看不见**这个错误），动的全是类级
读数：存活 838→948、吃掉 190→80、$\\times0.8152\\to\\times0.9222$、分区里的"缩减"与"不变"两格同时塌成 0、
"判据看不见" 469→798、§10 接缝 16→12 $\Rightarrow$ 抓住它的是 R17.2 与 R17.3 那两组**钉住的数字**，而 R17.0 照旧绿
$\Rightarrow$ 一致性只在票与票之间作证，**定义本身**只由那八个钉住的读数看守。第五例把乙路 $j$-耦合的单态重数
乘积 `ju[0] * jd[0]` 只取半边 $\Rightarrow$ 三路表与互不等都不动，只有分区里"归零 40→20、缩减 110→130"
（八格总数一字不动）$\Rightarrow$ 那条分区断言与那条"存活 $=$ 判据覆盖类"的流断言各守一半。良性例 b7 给
§14.9 的 `ftab = [...]` 那行补一条尾部注释，语义不动。甲路的处境与 R16 同一条边界：它就是引擎共用的
那台零空间/阶梯秩机器，从外面改它会连别层一起拖红 $\Rightarrow$ 它由 R17.0 那句"三路逐项相等"反向看守。

一次**假红**如实登记（错在本仪器自己，不在引擎）：§14.9 锚点那一栏第一版写成 `sorted(set(...))`，
而四条锚点里合法地有两条同值 $(1,1,1)$ $\Rightarrow$ 集合把 4 次出现折成 3 个不同值 $\Rightarrow$
活体判据 `len(l_anch) == 4` **恒不满足** $\Rightarrow$ 基线被 `judge` 判成"不干净"，于是七个良性例**一次性全部误报**
（台账当时 35/43，`missed` 是空列表、`false_alarm` 里正是基线与全部良性例）。修的是判据而不是期望值：改成
**按出现顺序 `findall`**，顺带把"哪个锚点位动了"变成读数（集合表示法把这件事扔掉了，而上面 l1/l3 两例的
(1,1,0) 与 (1,0,1) 全靠那个顺序才分得开）。教训：任何"条数必须等于 $N$"的活体判据，$N$ 必须是**读数本身
允许重复的 occurrence 数**；拿 set 的大小去充当 occurrence 的条数，是一条永远红、而且永远红在错误一侧的规则
$\Rightarrow$ 它不与"引擎写错"对立，它与"引擎读对"对立。

两条负面结果如实登记（与 R13.2 同族，只记在这段散文里、不进台账的例数）：**(i)** 共轭签名的相位
那一步（同时翻 $Y$ 与 $B-L$）植错符号会把共轭字母送到一个**不存在**的标签上，引擎以 `KeyError`
traceback 退出而非 FAIL ⇒ 按"崩溃不算捕获"，这一处**无法从外面植红**；**(ii)** "含点号字母的类"
逐档计数把判据 $n_d$ 换成 $n_u$ 是**中性变异**（共轭对合让两半逐档同数，六个数一个都不动）⇒ 那一
列只核对数量、不核对它挂在哪一半上。**(i) 的教训是位置：能植红的位置必须下游有读数；(ii) 的教训是
判据：对称性把一对判据变成同一个判据时，这一列就不再是那条判据的证据。**

命名边界（如实登记）：文件名与台账名仍叫 `check_r11_mutation`，因为它从 R11 起家；它此刻覆盖
**七层**，这一件事由台账里的 `layers` 字段与每例的 `layer` 字段成文，不由文件名成文。

用法：python 维护脚本/check_r11_mutation.py    （慢：每一例都要把整台引擎跑一次完整自检，
      例数与层数不写死在这里 —— 由台账里的 `cases_total`、`layers`、`layer_mutants` 打印）
产出：与维护脚本同目录的 check_r11_mutation.json（本脚本是唯一写入者）
"""
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, '..', '验证脚本'))
TARGET = os.path.join(ENGINE, 'so10_reps.py')
DEPS = ('so10_chain.py', 'so10_reps.py')
OUT = os.path.join(HERE, 'check_r11_mutation.json')

TOTAL_RE = re.compile(r'（(\d+) 项，PASS (\d+)）')
FAIL_RE = re.compile(r'\[FAIL\]\s+(R\d+\.\d+[a-z]*)')
PAIR_RE = re.compile(r'允许 (\d+) 条、禁戒 (\d+) 条')
BLOCK = '低能算符的选择规则（R11）'
BLOCK2 = '完整残留离散规范群（R12）'
BLOCK3 = '422 链残留按 SU(4) 权格重做（R13）'
BLOCK4 = '行标号账与逐权重账（R14）'
BLOCK5 = '算符基覆盖面（R15）'
BLOCK6 = '类数→缩法重数（R16）'
BLOCK7 = '缩法→Fermi 存活（R17）'
# 报告 §11 里那四个读数：每个都印自 GLOB，也就是印自被植入缺陷的那段算术的下游。
G_SIZE_RE = re.compile(r'活下来 (\d+) 个')          # |Gamma|（R12.1 的枚举）
G_FLAG_RE = re.compile(r'\*\*不成立\*\*|\*\*不同\*\*|定不出唯一的群')   # 同判/互化/定名失败
G_IDX_RE = re.compile(r'\| (\d+)（不变因子')         # R12.2 三条出处的甲那一列
G_ROOT_RE = re.compile(r'\| (是 / 是|是 / 否|否 / 是|否 / 否) \|')      # R12.0 两条独立判法
# 报告 §12 的六个读数：先切出 §12 那一节再匹配，避免与 §10/§11 的同类散文互相污染。
SEC12_A, SEC12_B = '## 12.', '## 13.'
H_SIZE_RE = re.compile(r'共 (\d+) 个元')             # 全候选群 = 类 x 弱 x 弱（R13.0 的枚举）
H_K_RE = re.compile(r'K=\\{(.+?)\\}')                # 在场谱的核（R13.2 的特征标枚举）
H_KORD_RE = re.compile(r'阶分布 \[([\d, ]+)\]')       # K 的阶分布（R13.2）
H_BY_RE = re.compile(r'商后共 (\d+) 种同构型')         # R13.3 的同构型种数
H_INT_RE = re.compile(r'在 (\d+)/(\d+) 条通道成立')    # R13.6 集合相等按通道计
H_EXC_RE = re.compile(r'唯一例外是 (.+?) 那条')        # R13.6 唯一例外的承载者
H_MP_RE = re.compile(r'实现者恰 (\d+) 个')             # R13.4 物质字称实现者个数
H_TORD_RE = re.compile(r'\| \$(.+?)\$ \| \$(.+?)\$ \| (\d+) \|')  # §12.1 类表的"阶"列（R13.0）
# 报告 §13 的读数：同样先切出 §13 那一节，避免与 §11/§12 的同类散文互相污染。
SEC13_A, SEC13_B = '## 13.', '## 14.'
I_NOV_RE = re.compile(r'（其中 (\d+) 条甲账没有）')            # R14.1：乙账严格更细的那一半
I_HOMG_RE = re.compile(r'(\d+) 组\(群元, 条件\)')               # R14.0：同态引理比对了多少组
I_HOMB_RE = re.compile(r'比对，违例 (\d+)。')                   # R14.0：其中违例几组
I_ADD_RE = re.compile(r'有 (\d+) 对之和落在集合外')             # R14.0：那批形变不是子群
I_MIS_RE = re.compile(r'违例 (\d+) / (\d+) / (\d+)')            # R14.2：三条恒等事的违例三元组
I_KERN_RE = re.compile(r'^\| ([甲乙丙]) [^|]*\| (\d+) \| (\d+) \|$', re.M)  # R14.3：三条路 × 两约定
I_ALLK_RE = re.compile(r'^\| 全部 (\d+) 条 \| (\d+) \|$', re.M)  # R14.4：整条件集的核
I_ONEK_RE = re.compile(r'^\| 单条最好的一条 \| (\d+) \|$', re.M)  # R14.4：one_min
I_CORE_RE = re.compile(r'^\| 贪心核心 (\d+) 条 \| (\d+) \|$', re.M)  # R14.4：核心长度与到位后的核
I_HALF_RE = re.compile(r'^\| 只要求半单部分平凡 \| (\d+) \|$', re.M)  # R14.5：只半单
I_GU_RE = re.compile(r'^\| 只要求 \$U\(1\)_\{B-L\}\$ 半边平凡 \| (\d+) \|$', re.M)  # R14.5：只 U(1)
I_INT_RE = re.compile(r'^\| 两半之交 \| (\d+) \|$', re.M)       # R14.5：两半之交
I_PAIR_RE = re.compile(r'条件对共 (\d+) 对（占 (\d+) 对的')      # R14.4：population 的大小
I_GRID_RE = re.compile(r'^\| \$(\d+)/(\d+)\$ \| (\d+) \| (\d+) \| (\d+) \| (\S+) \|$', re.M)  # R14.6
# 报告 §14 的读数：同样是先切节再匹配。表格那一路不逐条列数，只数行数并对行集合取摘要 ——
# §14 有八张表，逐格钉住等于把整节的字节抄进台账；行集合一动就能现形，这就够"读数至少动一个"。
SEC14_A, SEC14_B = '## 14.', '## 15.'
J_ZERO_RE = re.compile(r'像不在类集里 (\d+) 条、\$3Q\$ 不反号 (\d+) 条、\$\(n_u,n_d\)\$ 不互换 (\d+) 条、'
                       r'两条通道的判决改变 (\d+) 条')                 # R15.2：共轭对合的四处归零
J_PAR_RE = re.compile(r'三台机器的违例 (\d+) / (\d+) 条')               # R15.3：整除判据 vs CG vs 玻色块
J_MECH_RE = re.compile(r'为奇"的那批 (相等|\*\*不等\*\*)')               # R15.4：指标禁/群禁分叉的机理
J_COVER_RE = re.compile(r'档共 (\d+) 个、签名类合计 (\d+) 条、\$d_\{\\min\}\$ 从 (\S+) 一直到 (\S+)')
J_EQ_RE = re.compile(r'字母的那 (\d+) 条与 §10 的 (\d+) 条\*\*集合相等\*\* (\S+)')  # R15.2：超集不是替换
J_DLN_RE = re.compile(r'\$d=5\$ 档 (\d+) 条 \$\\Delta L\\ne0\$ 里 (\d+) 条\*\*完全不碰\*\*')  # R15.5
# 报告 §14.8 的读数：**单独切片**（'### 14.8' 到 '### 14.9'），不用 §14 那一份。逐档表那种六列行
# 在 §14 里另有六行（实测整节 12 行 vs 本节 6 行）⇒ 整节切片会让一条只动 §14.8 的缺陷被别的行淹掉。
# 下界原本是 '## 15.'：§14.9 那份三路表里有六行的"同名组大小"格是纯数字，与 §14.8 的 $n=0..6$ 表同形
# ⇒ 同一条 K_T4 会把两节的行并成一张表数（实测 7 行 → 13 行），故边界挪到 '### 14.9'。
SEC148_A, SEC148_B = '### 14.8', '### 14.9'
K_TRI_RE = re.compile(r'四路在 \$0\.\.\d+\$ 上逐项相等、违例 (\d+) 条')                # R16.0：四张票同数
K_T4_RE = re.compile(r'^\| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|$', re.M)      # R16.0：$n=0..6$ 表
K_BIN_RE = re.compile(r'^\| \$n_f=(\d+)\$、\$n_s=(\d+)\$ \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|$',
                      re.M)                                                            # R16.1：逐档表
K_SUM_RE = re.compile(r'共给 (\d+) 条缩法（\$\\times([\d.]+)\$）.*?低估了 (\d+) 条；'
                      r'最大重数就是 (\d+)')                                            # R16.2：差额本身
K_SEAM_RE = re.compile(r'的 (\d+) 条 SM 单态 \$d=6\$ 类\*\*每一条\*\*都是 \$(\d+)\$ 条缩法')  # R16.2：§10 接缝
K_D6_RE = re.compile(r'多缩法的类恰有 (\d+) 条 \$=\$ 这 (\d+) 条无点号的加上它们的点号孪生 (\d+) 条')
K_TOWER_RE = re.compile(r'缩法总数从 (\d+) 到 (\d+)，再到 (\d+)、(\d+)')                # R16.1：塔的逐层
# 报告 §14.9 的读数：切片 '### 14.9' 到 '## 15.'。三路表那 30 行与 §14.8 的 $n=0..6$ 表同形
# ⇒ 两边各自切一节，谁也不并谁。
SEC149_A, SEC149_B = '### 14.9', '## 15.'
L_DIS_RE = re.compile(r'用例里三路互不等 (\d+) 条')                          # R17.0：三张票同数
L_UNU_RE = re.compile(r'缩法重数（违例 (\d+) 条）')                            # R17.0：无重复名字必须退回缩法重数
L_TAB_RE = re.compile(r'^\| (\d+) \| (\S+) \| (\d+) \| (\d+) \| (\d+) \|$', re.M)  # R17.0：$(n,\text{组大小})$ 表
L_ANCH_RE = re.compile(r'同名 \$=\(([\d, ]+)\)\$')                            # R17.0：四条教科书锚点
L_PRICE_RE = re.compile(r'可构建类共 (\d+) 个、缩法 (\d+) 条，过了反对称化剩 (\d+) 条 '
                        r'\$\\Rightarrow\$ 这一道削减吃掉 (\d+) 条（\$\\times([\d.]+)\$）')  # R17.2：价格
L_PART_RE = re.compile(r'反而变大类）\[([\d, ]+)\]')                            # R17.2：六个分区数
L_SEAM_RE = re.compile(r'结构数从 (\d+) 到 (\d+)')                             # R17.3：§10 接缝
L_SCOPE_RE = re.compile(r'可构建类 (\d+) 个（缩法 (\d+) 条）在本层\*\*只登记不判定\*\*')  # R17.4：管辖范围

# 锚点：每条都必须在源文件里**恰好出现一次**，否则整轮判 INVALID（锚点漂了不等于没植入）。
A_JIA = (b'    return int(t3) % n == 0', b'    return int(t3 / 3) % n == 0')
A_BING = (b'        ang = 2.0 * math.pi * float(a) * float(q)',
          b'        ang = math.pi * float(a) * float(q)')
A_T3Q = (b'    return sum(3 * f_bl(f) for f in fl)', b'    return 3 * f_bl(fl[0])')
A_HIT = (b"    hit4 = [x for x in c4 if x['singlet'] > 0]",
         b"    hit4 = [x for x in c4 if x['zero'] > 0]")
A_OK = (b'    return None if t3.denominator != 1 else int(t3) % 3',
        b'    return None if t3.denominator != 1 else int(t3) % 3  # inert: benign case')
# R12 侧：四个各钉住 §11 的一个断言，且都落在门禁条件上（不在 assert 上）=> 崩溃不会冒充捕获。
G_TRI = (b"    tri = (p + 2 * q) if conv == 'A' else (2 * p + q)",
         b"    tri = (p + q) if conv == 'A' else (2 * p + q)")
G_OO = (b'            oo = 1 if k == 0 else d // math.gcd(k, d)',
        b'            oo = d if k == 0 else d // math.gcd(k, d)')
G_IDX = (b'        idx *= x', b'        idx += x')
G_ZB = (b'and (sum(v).numerator % 2 == 0)', b'and (sum(v).numerator % 3 == 0)')
G_OK = (b'            (x[3] + y[3]) % CEN_U_PER)',
        b'            (x[3] + y[3]) % CEN_U_PER)  # inert: benign case')
# R13 侧：四个各钉住 §12 的一个断言，同样落在门禁条件上。
H_QSTD = (b'    return (int(lab[2]) + 2 * int(lab[0]) + 3 * int(lab[1])) % 4',
          b'    return (int(lab[2]) + 2 * int(lab[0]) + 2 * int(lab[1])) % 4')
H_K = (b'    vord_pairs = [corder((ci, 0, 0)) for ci in range(len(V))]',
       b'    vord_pairs = [corder((ci, 1, 1)) for ci in range(len(V))]')
H_CLO = (b'        wcapc = wko & clo', b'        wcapc = wko | clo')
H_MP = (b"          if all(FV[k]['sig'][i] == FV[k]['mpp'] for k in sorted(FV))]",
        b"          if all(FV[k]['sig'][i] != FV[k]['mpp'] for k in sorted(FV))]")
H_OK = (b'    Kset = set(K)', b'    Kset = set(K)  # inert: benign case')
# R14 侧：五个各钉住 §13 的一个断言，同样落在门禁条件上。
I_NOV = (b'    novel = sorted(set(condB) - set(spec))',
         b'    novel = sorted(set(condB) & set(spec))')
I_ROOT = (b'                d = [int(lab0[i]) - int(lab[i]) for i in range(4)]',
          b'                d = [int(lab0[i]) - int(lab[(i + 1) % 4]) for i in range(4)]')
I_ONE = (b'    one_min = min(ker_size([mC[k]]) for k in spec)',
         b'    one_min = max(ker_size([mC[k]]) for k in spec)')
I_ADD = (b'               if tuple(g_mod1(F(a[i]) + F(b[i])) for i in range(4)) not in charA]',
         b'               if tuple(g_mod1(F(a[i]) + F(b[i])) for i in range(4)) in charA]')
I_GRID = (b'              for aR in range(2) for t in range(den * CEN_U_PER)]',
          b'              for aR in range(2) for t in range(den)]')
I_OK = (b'    FULL = (1 << len(C)) - 1', b'    FULL = (1 << len(C)) - 1  # inert: benign case')


def A(a, b):
    """锚点里带中文的那几条只能写 str 字面量（源文件是 UTF-8，但 b'中文' 不是合法字面量）再编成字节。"""
    return (a.encode('utf-8'), b.encode('utf-8'))


# R15 侧：七个各钉住 §14 的一处算术语境，同样落在门禁条件上（不在 assert 上）。
J_PERM = (b"        tot = sum(x['singlet'] * perm_weight(x['cf'], n) for x in book[(n, 0)])",
          b"        tot = sum(x['singlet'] for x in book[(n, 0)])")
J_UND = (b"    und_only = [x for x in book[(4, 0)] if x['nd'] == 0]",
         b"    und_only = [x for x in book[(4, 0)] if x['nd'] <= 1]")
J_UPL = (b"    upl = dict((bn, sum(1 for x in rep[bn] if x['ok'] and x['kmin'])) for bn in BST_BINS)",
         b"    upl = dict((bn, sum(1 for x in rep[bn] if x['ok'] and x['kmin'] is not None))"
         b" for bn in BST_BINS)")
J_ZF = A("        Zf = set(key(x) for x in lst if any(v['甲'] is False for v in x['v'].values()))",
         "        Zf = set(key(x) for x in lst if all(v['甲'] is False for v in x['v'].values()))")
J_DL = (b"        dl[bn] = (len(rows), len(v), sum(1 for x in v if not any('nu' in n for n in x['fl'])),",
        b"        dl[bn] = (len(rows), len(v), sum(1 for x in v if not any(n == 'nu^c'"
        b" for n in x['fl'])),")
J_MAXD = (b"    maxd = max((str(x['dmin']) for x in sum(rep.values(), []) if x['dmin'] is not None),",
          b"    maxd = min((str(x['dmin']) for x in sum(rep.values(), []) if x['dmin'] is not None),")
J_MECH = (b"and int(3 * x['scq']) % 2)", b"and int(3 * x['scq']) % 4)")
J_OK = (b"    key = lambda x: x['k']", b"    key = lambda x: x['k']  # inert: benign case")

# R16 侧：六个各钉住 §14.8 的一处算术语境，同样落在门禁条件上（不在 assert 上）。
# 甲路就是引擎共用的 cg_j0 ⇒ 从外面改它会把别的层一起拖红，测不到本节这张票（如实登记在 docstring）。
K_CG = (b"        return cg_j0(x['nu'] + kk) * cg_j0(x['nd'] + kk)",
        b"        return cg_j0(x['nu'] + kk) + cg_j0(x['nd'] + kk)")
K_BINC = (b"        return 0 if n % 2 else math.comb(n, n // 2) - math.comb(n, n // 2 + 1)",
          b"        return 0 if n % 2 else math.comb(n, n // 2) + math.comb(n, n // 2 + 1)")
K_HOOK = (b"        return math.factorial(2 * m) // (math.factorial(m + 1) * math.factorial(m))",
          b"        return math.factorial(2 * m) // (math.factorial(m) * math.factorial(m))")
# 这条是**复现伤**：对角余乘是沿位求和，写成覆写就等于把 $\sum_iX^{(i)}T=0$ 换成逐位单独归零
K_SL2 = (b"                            row[t ^ (bit << i) ^ (b << i)] += F(xv)",
         b"                            row[t ^ (bit << i) ^ (b << i)] = F(xv)")
K_EPS = (b"        eps = {(0, 1): F(1), (1, 0): F(-1)}",
         b"        eps = {(0, 1): F(1), (1, 0): F(1)}")
K_D6 = (b"sum(1 for x in hi if F(str(x['dmin'])) <= 6),",
        b"sum(1 for x in hi if F(str(x['dmin'])) < 6),")
K_OK = (b"    okc = [x for bn in BST_BINS for x in rep[bn] if x['ok']]",
        b"    okc = [x for bn in BST_BINS for x in rep[bn] if x['ok']]  # inert: benign case")

# R17 侧：五个各钉住 §14.9 的一处算术语境，同样落在门禁条件上（不在 assert 上）。
# 乙、丁两张票各自独立（甲路 = 引擎共用的零空间/阶梯秩，从外面改它会连别层一起拖红，见 docstring）。
L_SIGN = (b"                acc[key] = acc.get(key, F(0)) + (c if inv % 2 == 0 else -c)",
          b"                acc[key] = acc.get(key, F(0)) + c")
L_LAM = (b"            if m >= 3:", b"            if m >= 4:")
L_SPIN = (b"            js.append(0 if m == 2 else 1)", b"            js.append(1 if m == 2 else 1)")
L_SIZE = (b"        return tuple(sorted((v for v in c.values() if v >= 2), reverse=True))",
          b"        return tuple(sorted((v for v in c.values() if v >= 3), reverse=True))")
L_PROD = (b"            a = ju[0] * jd[0]", b"            a = ju[0]")
L_OK = (b"    ftab = [(n, s) + fermi_dim(n, s) for n in range(NEXP + 1) for s in fermi_parts(n)]",
        b"    ftab = [(n, s) + fermi_dim(n, s) for n in range(NEXP + 1) for s in fermi_parts(n)]"
        b"  # inert: benign case")

CASES = [
    ('ctl', '基线：不植入', 'baseline', None, 'both'),
    ('m1', '甲：同余式右移一位，把 N|3Q 写成 N|Q（只动三条路径里的整除那条）', 'mutant', A_JIA, 'R11'),
    ('m2', '丙：浮点那条把 2pi 周期写成 pi 半周期（只动三条路径里的浮点那条）', 'mutant', A_BING, 'R11'),
    ('m3', '荷账丢掉求和号：sum_k 3(B-L)_k 写成只取第一条场', 'mutant', A_T3Q, 'R11'),
    ('m4', '枚举改用 R11.1 那个错 projector 的零权当筛选条件', 'mutant', A_HIT, 'R11'),
    ('b1', '良性：给 f_tri 补一条尾部注释（语义不动）', 'benign', A_OK, 'both'),
    ('g1', 'R12：换掉色 Z_3 生成元的甲侧 triality（p+2q 写成 p+q）⇒ 两支不再互化',
     'mutant', G_TRI, 'R12'),
    ('g2', 'R12：阿贝尔群的元素阶多重集把单位元读成最大阶（定名那一步失去唯一命中）',
     'mutant', G_OO, 'R12'),
    ('g3', 'R12：格指数把不变因子取和而不是取积（三条出处不再同数）',
     'mutant', G_IDX, 'R12'),
    ('g4', 'R12："在不在根格里"的第二条判法把坐标和的奇偶改成模 3（两条判法不再同判）',
     'mutant', G_ZB, 'R12'),
    ('b2', '良性：给 cen_law 的 U(1) 分量补一条尾部注释（语义不动）', 'benign', G_OK, 'both'),
    ('h1', 'R13：路丙的标准 triality 号把 3b 写成 2b（丙与格读数不再成 q_lat = 3 q_std）',
     'mutant', H_QSTD, 'R13'),
    ('h2', 'R13：色类阶的枚举把类元读成对角粘合元（(ci,0,0) 写成 (ci,1,1) ⇒ 类表"阶"列漂移）',
     'mutant', H_K, 'R13'),
    ('h3', 'R13：正向对照把两半"交集"写成"并集"（半群读数退化 ⇒ 集合相等不再成立）',
     'mutant', H_CLO, 'R13'),
    ('h4', 'R13：物质字称的实现者把相位判据取反（只数逐场都 ≠ 目标相位的元 ⇒ 个数偏离恰 2）',
     'mutant', H_MP, 'R13'),
    ('b3', '良性：给 Kset 那行补一条尾部注释（语义不动）', 'benign', H_OK, 'both'),
    ('i1', 'R14：乙账"甲账没有"的条件把差集写成交集（304 掉到 61 ⇒ 乙账不再严格更细）',
     'mutant', I_NOV, 'R14'),
    ('i2', 'R14：子多重态内的标签差向量循环错位一位（"在不在根格里"那条判法读到错的分量 '
           '⇒ 三条恒等事的违例三元组从 0/0/0 变成 0/非零/0，另两条判法照旧干净）',
     'mutant', I_ROOT, 'R14'),
    ('i3', 'R14：冗余度里"单条最好的一条"把 min 写成 max（核从 12 读成整格 432）',
     'mutant', I_ONE, 'R14'),
    ('i4', 'R14：形变的逐点加法封闭性把 not in 写成 in（158 对例外与 418 对命中整批互换）',
     'mutant', I_ADD, 'R14'),
    ('i5', 'R14：$t$ 网格每档的周期去掉 CEN_U_PER 因子（候选元数 216/432/864/2160 整体缩 3 倍）',
     'mutant', I_GRID, 'R14'),
    ('b4', '良性：给 FULL 那行补一条尾部注释（语义不动）', 'benign', I_OK, 'both'),
    ('j1', 'R15：逐类单态结构总数去掉排列权重（$\sum$ 单态数 而不乘 perm_weight ⇒ §14 那两张'
           '结构表的整列漂移）', 'mutant', J_PERM, 'R15'),
    ('j2', 'R15：把"只取非点号字母"读成"至多含一个点号字母"（$x[\'nd\'] == 0$ 写成 $<= 1$ ⇒'
           ' "扩基是超集、不是替换"那条集合相等不再成立）', 'mutant', J_UND, 'R15'),
    ('j3', 'R15：把"上移"读成"洛伦兹可行"（真值判成 `is not None` ⇒ §14.3 的上移列读到别的数）',
     'mutant', J_UPL, 'R15'),
    ('j4', 'R15：群禁集合把"任一道判禁"读成"全部道判禁"（any 写成 all ⇒ §14.5 的群禁列与'
           '"指标禁 $=$ 群禁"那条巧合整批改判）', 'mutant', J_ZF, 'R15'),
    ('j5', 'R15.5："不碰 $\\nu^c$（含其共轭）"读成名字恰等于 $\\nu^c$（共轭半边漏掉 ⇒ §14.6'
           ' 那条"不碰"的计数改变）', 'mutant', J_DL, 'R15'),
    ('j6', 'R15：覆盖面把 $d_{\\min}$ 的上端读成下端（max 写成 min ⇒ "六档实际探到 $d=8$" 被读成'
           '"只到 $d=3$"）', 'mutant', J_MAXD, 'R15'),
    ('j7', 'R15：机理等式的"标量半边为奇"把 mod 2 写成 mod 4（⇒ §14.5 那条集合等式判成"不等"）',
     'mutant', J_MECH, 'R15'),
    ('b5', '良性：给 §14 的 key 那行补一条尾部注释（语义不动）', 'benign', J_OK, 'both'),
    ('k1', 'R16：把"一类的缩法重数 $=$ 两侧重数之**积**"写成**和**（$*$ 改成 $+$ ⇒ "只有 1 条缩法 '
           '当且仅当两侧指标数都不超过 2"不再成立，逐档表与 2261/668 整列漂移）', 'mutant', K_CG, 'R16'),
    ('k2', 'R16：乙路二项式差把减号写成加号（一张票自己错、别张票照旧 ⇒ 动的只有"四路逐项相等、'
           '违例 N 条"里那违例的一半）', 'mutant', K_BINC, 'R16'),
    ('k3', 'R16：丙路钩长公式把 $(m+1)!\\,m!$ 写成 $m!\\,m!$（即把 Catalan 读成中心二项式 ⇒ 同上，'
           '钉的是第二张票）', 'mutant', K_HOOK, 'R16'),
    ('k4', 'R16：丁路把对角余乘的沿位**累加**写成**覆写**（$\\sum_iX^{(i)}T=0$ 变成逐位单独归零 '
           '⇒ 显式零空间的维数读错；这一条复现本层写作时真踩过的伤）', 'mutant', K_SL2, 'R16'),
    ('k5', 'R16：画线法的 $\\varepsilon_{10}$ 把 $-1$ 写成 $+1$（配对张量不再反对称 ⇒ 秩与 Plücker '
           '关系数一起动、$(n-1)!!$ 那一列不动：钉住"三个画线法只撑出两个独立缩法"）',
     'mutant', K_EPS, 'R16'),
    ('k6', 'R16：覆盖面把 $d\\le6$ 读成 $d<6$（⇒ "多缩法的类恰有 16 条 $=$ 8 条加其点号孪生 8 条" '
           '整批归零，"谁多重是边界清楚的一批"从此没有主体）', 'mutant', K_D6, 'R16'),
    ('b6', '良性：给 §14.8 的 okc 那行补一条尾部注释（语义不动）', 'benign', K_OK, 'both'),
    ('l1', 'R17：丁路 Grassmann 求值丢掉排序符号（$+(-1)^{\\#inv}c$ 写成 $+c$ ⇒ 同名槽的反对易不再'
           '现形，$\\varepsilon^{\\alpha\\beta}\\psi_\\alpha\\psi_\\beta$ 那类读数被读歪：这是本层'
           '写作时真踩过的伤）', 'mutant', L_SIGN, 'R17'),
    ('l2', 'R17：乙路 $\\Lambda^m(\\mathbb C^2)=0$ 的门槛从 $m\\ge3$ 挪到 $m\\ge4$（三元组不再自动'
           '归零 ⇒ 票二与票三在一整批用例上分手）', 'mutant', L_LAM, 'R17'),
    ('l3', 'R17：乙路把"$m$ 个同名槽给 $2j=0$"读成 $2j=1$（$m=2$ 那一步的自旋记错 ⇒ 四槽两两同名'
           '这类锚点漂掉，甲/丁照旧）', 'mutant', L_SPIN, 'R17'),
    ('l4', 'R17：名字分组的阈值把"占 $\\ge2$ 槽"写成"占 $\\ge3$ 槽"（成对全同从登记里消失 ⇒ '
           '判据对一半的全同类瞎掉，§10 接缝的 16 条结构数读回 16）', 'mutant', L_SIZE, 'R17'),
    ('l5', 'R17：一类的存活数写成只算无点号侧（$j_u\\times j_d$ 写成 $j_u$ ⇒ "两侧各自算秩再相乘"'
           '这句话没有内容，无重复名字那一批不再被"看不见"）', 'mutant', L_PROD, 'R17'),
    ('b7', '良性：给 §14.9 的 ftab 那行补一条尾部注释（语义不动）', 'benign', L_OK, 'both'),
]


def read_source():
    with open(TARGET, 'rb') as fh:
        return fh.read()


def engine_json_tests():
    """磁盘上那份报告 JSON 的 tests 条数：基线打印的门禁数必须与它相等，否则夹具塌陷。"""
    p = os.path.join(ENGINE, 'SO10表示论报告.json')
    if not os.path.exists(p):
        return None
    with io.open(p, encoding='utf-8') as fh:
        return len(json.load(fh).get('tests') or [])


def build(tag, patch):
    """临时目录 = 整台引擎的一份可跑副本；patch 为 None 时是基线。"""
    d = os.path.join(tempfile.mkdtemp(prefix='am_r11_%s_' % tag), 'engine')
    os.makedirs(d)
    hits = 0
    for f in DEPS:
        src = os.path.join(ENGINE, f)
        with open(src, 'rb') as fh:
            b = fh.read()
        if f == 'so10_reps.py' and patch:
            hits = b.count(patch[0])
            b = b.replace(patch[0], patch[1])
        with open(os.path.join(d, f), 'wb') as fh:
            fh.write(b)
    return d, hits


def run(d):
    r = subprocess.run([sys.executable, os.path.join(d, 'so10_reps.py')], cwd=d,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = r.stdout.decode('utf-8', 'replace')
    rep = ''
    rp = os.path.join(d, 'SO10表示论报告.md')
    if os.path.exists(rp):
        with io.open(rp, encoding='utf-8') as fh:
            rep = fh.read()
    a, bnd = rep.find(SEC12_A), rep.find(SEC12_B)
    sec12 = rep[a:bnd] if (a >= 0 and bnd > a) else ''
    a, bnd = rep.find(SEC13_A), rep.find(SEC13_B)
    sec13 = rep[a:bnd] if (a >= 0 and bnd > a) else ''
    a, bnd = rep.find(SEC14_A), rep.find(SEC14_B)
    sec14 = rep[a:bnd] if (a >= 0 and bnd > a) else ''
    a, bnd = rep.find(SEC148_A), rep.find(SEC148_B)
    sec148 = rep[a:bnd] if (a >= 0 and bnd > a) else ''
    a, bnd = rep.find(SEC149_A), rep.find(SEC149_B)
    sec149 = rep[a:bnd] if (a >= 0 and bnd > a) else ''
    lrows = sorted(l for l in sec149.split('\n') if l.startswith('|'))
    trows = sorted(l for l in sec14.split('\n') if l.startswith('|'))
    m = TOTAL_RE.search(out)
    fails = FAIL_RE.findall(out)
    return {'exit': r.returncode,
            'gates': int(m.group(1)) if m else None,
            'pass': int(m.group(2)) if m else None,
            'fail_ids': fails,
            'r11_fail_ids': [x for x in fails if x.startswith('R11')],
            'layer_fail_ids': dict((k, [x for x in fails if x.startswith(k)])
                                   for k in ('R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17')),
            'printed_r11_block': BLOCK in out,
            'printed_r12_block': BLOCK2 in out,
            'printed_r13_block': BLOCK3 in out,
            'printed_r14_block': BLOCK4 in out,
            'printed_r15_block': BLOCK5 in out,
            'printed_r16_block': BLOCK6 in out,
            'printed_r17_block': BLOCK7 in out,
            'report_pairs': sorted(set(tuple(int(x) for x in t) for t in PAIR_RE.findall(rep))),
            'report_global': {
                'g_size': sorted(set(int(x) for x in G_SIZE_RE.findall(rep))),
                'g_flag': len(G_FLAG_RE.findall(rep)),
                'g_idx': sorted(set(int(x) for x in G_IDX_RE.findall(rep))),
                'g_root': sorted(set(G_ROOT_RE.findall(rep)))},
            'report_r13': {
                'h_size': sorted(set(H_SIZE_RE.findall(sec12))),
                'h_k': sorted(set(H_K_RE.findall(sec12))),
                'h_kord': sorted(set(H_KORD_RE.findall(sec12))),
                'h_by': sorted(set(H_BY_RE.findall(sec12))),
                'h_int': sorted(set(tuple(x) for x in H_INT_RE.findall(sec12))),
                'h_exc': sorted(set(H_EXC_RE.findall(sec12))),
                'h_mp': sorted(set(H_MP_RE.findall(sec12))),
                'h_tord': sorted(set(m[2] for m in H_TORD_RE.findall(sec12)))},
            'report_r14': {
                'i_nov': sorted(set(I_NOV_RE.findall(sec13))),
                'i_hom': sorted(set(zip(I_HOMG_RE.findall(sec13),
                                        I_HOMB_RE.findall(sec13)))),
                'i_add': sorted(set(I_ADD_RE.findall(sec13))),
                'i_mis': sorted(set(I_MIS_RE.findall(sec13))),
                'i_kern': sorted(set(I_KERN_RE.findall(sec13))),
                'i_sets': sorted(set(I_ALLK_RE.findall(sec13))),
                'i_one': sorted(set(I_ONEK_RE.findall(sec13))),
                'i_core': sorted(set(I_CORE_RE.findall(sec13))),
                'i_half': sorted(set(I_HALF_RE.findall(sec13))),
                'i_gu': sorted(set(I_GU_RE.findall(sec13))),
                'i_int': sorted(set(I_INT_RE.findall(sec13))),
                'i_pairs': sorted(set(I_PAIR_RE.findall(sec13))),
                'i_grid': sorted(set(I_GRID_RE.findall(sec13)))},
            'report_r15': {
                'j_rows': (len(trows), hashlib.sha1('\n'.join(trows).encode('utf-8')).hexdigest()[:12]),
                'j_zero': sorted(set(J_ZERO_RE.findall(sec14))),
                'j_par': sorted(set(J_PAR_RE.findall(sec14))),
                'j_mech': sorted(set(J_MECH_RE.findall(sec14))),
                'j_cover': sorted(set(J_COVER_RE.findall(sec14))),
                'j_eq': sorted(set(J_EQ_RE.findall(sec14))),
                'j_dln': sorted(set(J_DLN_RE.findall(sec14)))},
            'report_r16': {
                'k_tri': sorted(set(K_TRI_RE.findall(sec148))),
                'k_t4': sorted(set(K_T4_RE.findall(sec148))),
                'k_bin': sorted(set(K_BIN_RE.findall(sec148))),
                'k_sum': sorted(set(K_SUM_RE.findall(sec148))),
                'k_seam': sorted(set(K_SEAM_RE.findall(sec148))),
                'k_d6': sorted(set(K_D6_RE.findall(sec148))),
                'k_tower': sorted(set(K_TOWER_RE.findall(sec148)))},
            'report_r17': {
                'l_dis': sorted(set(L_DIS_RE.findall(sec149))),
                'l_unu': sorted(set(L_UNU_RE.findall(sec149))),
                'l_tab': sorted(set(L_TAB_RE.findall(sec149))),
                'l_rows': (len(lrows), hashlib.sha1('\n'.join(lrows).encode('utf-8')).hexdigest()[:12]),
                # 四条锚点是一个**有序序列**（两槽／四槽／两两／三对），其读数里 (1, 1, 1) 合法地出现三次
                # ⇒ 去重会把"哪一格动了"抹掉（且本轮实测：去重后恒为 2 条，`== 4` 永不可满足 ⇒ 基线被判不干净、
                #   七条良性例跟着全部误报）。故这里保留出现次序，不去重。
                'l_anch': L_ANCH_RE.findall(sec149),
                'l_price': sorted(set(L_PRICE_RE.findall(sec149))),
                'l_part': sorted(set(L_PART_RE.findall(sec149))),
                'l_seam': sorted(set(L_SEAM_RE.findall(sec149))),
                'l_scope': sorted(set(L_SCOPE_RE.findall(sec149)))},
            'traceback': 'Traceback' in out}


def judge(case, res, base):
    _tag, _name, kind, _patch, layer = case
    r14_live = (bool(res['report_r14']['i_nov']) and bool(res['report_r14']['i_kern'])
                and bool(res['report_r14']['i_grid']) and bool(res['report_r14']['i_mis']))
    r15_live = (res['report_r15']['j_rows'][0] > 0 and bool(res['report_r15']['j_zero'])
                and bool(res['report_r15']['j_par']) and bool(res['report_r15']['j_cover'])
                and bool(res['report_r15']['j_eq'])
                and bool(res['report_r15']['j_dln']))
    r16_live = (len(res['report_r16']['k_t4']) == 7 and len(res['report_r16']['k_bin']) == 6
                and bool(res['report_r16']['k_tri']) and bool(res['report_r16']['k_sum'])
                and bool(res['report_r16']['k_seam']) and bool(res['report_r16']['k_d6'])
                and bool(res['report_r16']['k_tower']))
    r17_live = (len(res['report_r17']['l_tab']) == 30 and res['report_r17']['l_rows'][0] > 0
                and len(res['report_r17']['l_anch']) == 4
                and bool(res['report_r17']['l_dis']) and bool(res['report_r17']['l_unu'])
                and bool(res['report_r17']['l_price']) and bool(res['report_r17']['l_part'])
                and bool(res['report_r17']['l_seam']) and bool(res['report_r17']['l_scope']))
    clean = (res['exit'] == 0 and res['pass'] == res['gates'] and not res['fail_ids']
             and not res['traceback']
             and res['printed_r11_block'] and res['printed_r12_block']
             and res['printed_r13_block'] and res['printed_r14_block']
             and res['printed_r15_block'] and res['printed_r16_block']
             and res['printed_r17_block']
             and bool(res['report_pairs']) and bool(res['report_global']['g_size'])
             and bool(res['report_r13']['h_size']) and bool(res['report_r13']['h_k'])
             and r14_live and r15_live and r16_live and r17_live)
    if kind in ('baseline', 'benign'):
        return clean and (kind == 'baseline'
                          or (res['report_pairs'] == base['report_pairs']
                              and res['report_global'] == base['report_global']
                              and res['report_r13'] == base['report_r13']
                              and res['report_r14'] == base['report_r14']
                              and res['report_r15'] == base['report_r15']
                              and res['report_r16'] == base['report_r16']
                              and res['report_r17'] == base['report_r17']
                              and res['pass'] == base['pass']))
    moved = [k for k, v in (('report_pairs', res['report_pairs'] != base['report_pairs']),
                            ('report_global', res['report_global'] != base['report_global']),
                            ('report_r13', res['report_r13'] != base['report_r13']),
                            ('report_r14', res['report_r14'] != base['report_r14']),
                            ('report_r15', res['report_r15'] != base['report_r15']),
                            ('report_r16', res['report_r16'] != base['report_r16']),
                            ('report_r17', res['report_r17'] != base['report_r17']),
                            ('gates_pass', res['pass'] != base['pass'])) if v]
    res['moved'] = moved
    return (res['exit'] != 0 and bool(res['layer_fail_ids'].get(layer))
            and not res['traceback'] and bool(moved))


def main():
    src = read_source()
    anchors = {}
    for _, _, _, patch, _layer in CASES:
        if patch:
            anchors[patch[0].decode()] = src.count(patch[0])
    tests_on_disk = engine_json_tests()

    res = {}
    for tag, name, kind, patch, layer in CASES:
        d, hits = build(tag, patch)
        try:
            r = run(d)
        finally:
            shutil.rmtree(os.path.dirname(d), ignore_errors=True)
        r.update({'id': tag, 'claim': name, 'kind': kind, 'layer': layer,
                  'anchor_hits': hits if patch else 0})
        r['expect_caught'] = kind == 'mutant'
        res[tag] = r
        print('[case] %s %-14s layer=%-5s exit=%s gates=%s/%s fail=%s pairs=%s glob=%s h12=%s '
              'r14=%s r15=%s r16=%s r17=%s' %
              (tag, kind, layer, r['exit'], r['pass'], r['gates'],
               r['layer_fail_ids'].get(layer) or r['fail_ids'], r['report_pairs'],
               r['report_global']['g_size'], r['report_r13']['h_k'] and
               (r['report_r13']['h_size'], r['report_r13']['h_int'], r['report_r13']['h_mp']),
               r['report_r14']['i_nov'] and
               (r['report_r14']['i_mis'], r['report_r14']['i_one'], r['report_r14']['i_add'],
                r['report_r14']['i_grid'] and len(r['report_r14']['i_grid'])),
               r['report_r15']['j_cover'] and
               (r['report_r15']['j_rows'], r['report_r15']['j_zero'], r['report_r15']['j_eq'],
                r['report_r15']['j_cover'], r['report_r15']['j_dln'], r['report_r15']['j_mech']),
               r['report_r16']['k_tri'] and
               (r['report_r16']['k_tri'], len(r['report_r16']['k_t4']), r['report_r16']['k_sum'],
                r['report_r16']['k_seam'], r['report_r16']['k_d6'], r['report_r16']['k_tower'],
                len(r['report_r16']['k_bin'])),
               r['report_r17']['l_dis'] and
               (r['report_r17']['l_dis'], len(r['report_r17']['l_tab']),
                r['report_r17']['l_anch'], r['report_r17']['l_price'], r['report_r17']['l_part'],
                r['report_r17']['l_seam'], r['report_r17']['l_scope'])))

    anchor_bad = [k for k, v in anchors.items() if v != 1]
    fixture_bad = (res['ctl']['gates'] is None or (tests_on_disk is not None
                   and res['ctl']['gates'] != tests_on_disk))
    for tag, r in res.items():
        r['ok'] = (not anchor_bad and not fixture_bad) and judge(
            next(c for c in CASES if c[0] == tag), r, res['ctl'])
        if r['expect_caught']:
            print('[moved] %s %s' % (tag, r.get('moved')))
    missed = [t for t, r in res.items() if r['expect_caught'] and not r['ok']]
    false_alarm = [t for t, r in res.items() if not r['expect_caught'] and not r['ok']]
    payload_layers = sorted(set(c[4] for c in CASES if c[4] != 'both'))
    # 覆盖面自己也要判：某一层的变异体被整批删掉时，例数的账照样自洽（baseline 1 + 变异体 + 良性），
    # 但这台仪器已经悄悄退回单层 ⇒ "七层都看守"这句话就没有仪器背书了。
    uncovered = [k for k in payload_layers
                 if not any(c[2] == 'mutant' and c[4] == k for c in CASES)]
    verdict = 'CAUGHT' if not missed and not false_alarm and not anchor_bad \
        and not fixture_bad and not uncovered else 'INVALID'
    payload = {'script': 'check_r11_mutation.py', 'target': '验证脚本/so10_reps.py',
               'layers': sorted(set(c[4] for c in CASES if c[4] != 'both')),
               'target_bytes': len(src), 'engine_json_tests': tests_on_disk,
               'anchor_counts': anchors, 'fixture_ok': not fixture_bad,
               'cases_total': len(CASES), 'mutants': sum(1 for c in CASES if c[2] == 'mutant'),
               'benign': sum(1 for c in CASES if c[2] == 'benign'),
               'caught': sum(1 for t, r in res.items() if r['expect_caught'] and r['ok']),
               'missed': missed, 'false_alarm': false_alarm,
               'uncovered_layers': uncovered,
               'baseline_pairs': res['ctl']['report_pairs'],
               'baseline_global': res['ctl']['report_global'],
               'baseline_r13': res['ctl']['report_r13'],
               'baseline_r14': res['ctl']['report_r14'],
               'baseline_r15': res['ctl']['report_r15'],
               'baseline_r16': res['ctl']['report_r16'],
               'baseline_r17': res['ctl']['report_r17'],
               'layer_mutants': dict((k, sum(1 for c in CASES if c[2] == 'mutant' and c[4] == k))
                                     for k in payload_layers),
               'verdict': verdict,
               'cases': [res[t] for t, _, _, _, _ in CASES]}
    with io.open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    print('结论：%s ｜ %d 例（变异体 %d、良性 %d）｜ 基线报告读数 %s ｜ 台账 %s' %
          (verdict, len(CASES), payload['mutants'], payload['benign'],
           res['ctl']['report_pairs'], os.path.basename(OUT)))
    print('自检：%s（%d 例，PASS %d）' %
          ('全部通过' if verdict == 'CAUGHT' else '存在未捕获或误报', len(CASES),
           sum(1 for r in res.values() if r['ok'])))
    return 0 if verdict == 'CAUGHT' else 1


if __name__ == '__main__':
    sys.exit(main())
