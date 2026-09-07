# Bug Report · Bug 报告

> 请按以下结构提交 bug 报告。请确保每一个 `☑` 项目都有对应的回答。

---

## 〇、摘要（Summary）
一句话描述这个 bug。

**例**：R9 归纳闭合证明在 n=3 时 mpmath 验证失败

---

## 一、复现步骤（Steps to Reproduce）

```python
# 最小可复现代码
from mpmath import mp, mpf
mp.dps = 50
x = mpf('1.234')
# ...
```

---

## 二、预期行为（Expected Behavior）
正确情况下应该发生什么。

---

## 三、实际行为（Actual Behavior）
实际发生了什么。包括完整的错误信息 / traceback / 数值差。

---

## 四、环境（Environment）

| 项目 | 值 |
|---|---|
| Python 版本 | (如 3.13.12) |
| mpmath 版本 | (如 1.3.0) |
| sympy 版本 | (如 1.12) |
| OS | (如 Windows 11) |
| openuft 版本 | (如 v4.0.0) |

---

## 五、可能的影响范围

- [ ] 影响某个具体定理（如 TS3）
- [ ] 影响某条主轴（如 D 求导）
- [ ] 影响整体验证精度
- [ ] 仅限文档问题

---

## 六、其他上下文（Additional Context）

任何有助于问题定位的信息（截图、相关论文、相关 PR 等）。

---

## 七、修复建议（可选 · Optional）

如果你有修复想法，请附上。

---

**声明**：本仓库按 MIT License 开源，提交 Issue 表示您同意相关讨论可被公开引用。
