# -*- coding utf-8 -*-
"""Clean garbled tokens + 2 logic bugs in r215 engine (line-precise patch)."""
import io

ENG = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码\TUFT-r215_四力统一方程_定义恒等式零判别力覆盖缺与修复定价_精算_2026-10-26.py"

lines = io.open(ENG, encoding="utf-8").read().split("\n")

# 1) A4 entry block (lines 512..517 in 1-based -> idx 511..516)
i0 = next(i for i, l in enumerate(lines) if l.strip().startswith('add("A4"'))
new_block = [
    '    add("A4", "L1 定义恒等式",',
    '        "推论：该统一式本身不产出任何耦合数值——四个通道的 (s, Q, \u03bb) 每一个成分都取自"',
    '        "外部（详见 L2 账目），故「把四力写进一个方程」在信息意义上等价于「同一个符号"',
    '        "取四个互不相干的外部值」。",',
    '        "INFO",',
    '        "自由度核算：外部输入数不下降，自由度削减为 0")',
]
assert 'add("A4"' in lines[i0], lines[i0]
end = i0
while not lines[end].strip().startswith('"自由度核算') and end < i0 + 8:
    end += 1
lines[i0:end + 1] = new_block

t = "\n".join(lines)

# 2) remaining garbled tokens
subs = [
    ("无一处形状 beteiligt。", "无一处形状与数据的 confrontation。"),
    ("- 力度tomcat：", "- 统一式为静态标量势梯度："),
    ("≡ G*m1*m2 的单项式精确归约", "的单项式精确归约"),
    ('("1.602176634e-19") ** 2 / (Decimal(4) * Decimal(',
     '("1.602176634e-19") ** 2 / (Decimal(4) * Decimal('),
]
# fix 2 legit bugs separately below; here only tokens
t = t.replace("无一处形状 beteiligt。", "无一处形状与数据的 confrontation。")
t = t.replace("- 力度tomcat：", "- 统一式为静态标量势梯度：")

# 3) BUG-A: numeric_e identity must compare alpha*hbar*c with e^2/(4pi*eps0) [no extra c]
old_a = '''        (Decimal("1.602176634e-19") ** 2 / (Decimal(4) * Decimal(
            "3.14159265358979323846") * Decimal("8.8541878128e-12") * C0)),'''
new_a = '''        (Decimal("1.602176634e-19") ** 2 / (Decimal(4) * Decimal(
            "3.14159265358979323846") * Decimal("8.8541878128e-12"))),'''
assert old_a in t, "BUG-A anchor"
t = t.replace(old_a, new_a)

# 4) BUG-B: exact rational power in Mon.__pow__ (Fraction**Fraction silently yields float)
old_b = '''    def __pow__(self, e):
        e = Fraction(e)
        return Mon(self.c ** e, {k: v * e for k, v in self.p.items()})'''
new_b = '''    def __pow__(self, e):
        e = Fraction(e)
        if self.c == 1:
            coef = Fraction(1)
        elif e.denominator == 1:
            coef = self.c ** int(e)
        else:
            # 非整数幂且系数非 1 会落入浮点 ⇒ 精确性破产，必须显式报错而非静默降级
            raise ValueError("inexact coefficient power: c=%s e=%s" % (self.c, e))
        return Mon(coef, {k: v * e for k, v in self.p.items()})'''
assert old_b in t, "BUG-B anchor"
t = t.replace(old_b, new_b)

# 5) drop the garbage table line in render_verdict_md
old_c = '''    L.append("| PDG 提及 / 「实验输入」表述 | %d / %d |"
             % (kn["coverage"].get("pdg_mentions", 0) if False else 3, 2)
             if False else "| PDG / 实验输入标注 | 见 §18 §0 表③ 明言 g_w/g_s 为实验输入 |")'''
new_c = '''    L.append("| PDG / 实验输入标注 | §18 §0 表③ 明言 g_w/g_s 为实验输入 |")'''
if old_c in t:
    t = t.replace(old_c, new_c)
else:
    print("WARN: garbage table line not found (already clean?)")

io.open(ENG, "w", encoding="utf-8").write(t)
print("patched ok")
