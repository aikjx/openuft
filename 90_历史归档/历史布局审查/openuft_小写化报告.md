# openuft 小写化改造报告

> 2026-09-06 v4.0.2
> 任务：`openUFT/` → `openuft/`，仓库 URL `github.com/aikjx/openUFT` → `github.com/aikjx/openuft`

---

## 一、动机

| 项目 | 旧 | 新 |
|---|---|---|
| 本地目录 | `openUFT/` | `openuft/` |
| GitHub 仓库 | `github.com/aikjx/openUFT` | `github.com/aikjx/openuft` |
| 包名 | `openUFT` | `openuft` |

**为什么要小写？**

1. **GitHub URL 偏好**：现代开源项目的 GitHub URL 普遍小写（kubernetes、react、vue 等）
2. **URL 一致性**：用户给的 URL 是 `github.com/aikjx/openuft.git`，需要对齐
3. **Linux 友好**：Linux 文件系统区分大小写，小写路径最安全
4. **跨平台一致**：Windows 不区分大小写，反而可能造成混乱

---

## 二、操作记录

### 步骤 1 · 尝试改名（失败）

```bash
$ mv openUFT openuft_tmp
mv: cannot move 'openUFT' to 'openuft_tmp': Permission denied
```

❌ **失败原因**：`WinError 5 Permission Denied`。可能是有进程（IDE/Defender/Index）锁定了目录。

### 步骤 2 · 复制法（成功）

```python
import shutil
shutil.copytree(源码='openUFT', dst='openuft', dirs_exist_ok=True)
```

✅ 部分 WinError 32 警告（旧 源码 文件被同时持有句柄），但**复制成功**：

| 指标 | 值 |
|---|---|
| Markdown | 79 |
| Python | 11 |
| 总文件 | 93 |
| 大小 | 1.3 MB |

### 步骤 3 · 批量字面替换

```bash
find . -type f \( -name "*.md" -o -name "*.py" -o -name "*.cff" -o -name "LICENSE" -o -name ".gitignore" \) -print0 \
  | xargs -0 sed -i 's/openUFT/openuft/g'
```

- ✅ 0 处 `openUFT` 字面残留
- ✅ 0 处 `github.com/aikjx/openUFT` URL 残留

### 步骤 4 · 清理 `__pycache__/`

删除所有 `__pycache__/` 目录（防止 .pyc 文件残留旧名），下次运行 Python 时自动重新生成。

---

## 三、未自动完成项

### ❌ 旧目录 `openUFT/` 仍在

**原因**：Windows 进程锁定无法用脚本删除（Permission Denied）

**手动删除方法**（任选其一）：

**A · 资源管理器**：
1. 打开文件资源管理器 → `D:\a10\aikjx\code\my_lib\`
2. 右键 `openUFT` → 删除
3. 如果提示"文件被占用"，关闭所有可能占用该目录的程序（VSCode、IDEA 等），重启资源管理器后再删

**B · PowerShell（管理员）**：
```powershell
# 1. 关闭可能占用 openUFT 的进程
Get-Process | Where-Object { $_.MainWindowTitle -match 'openUFT|code|idea' } | Stop-Process -Force

# 2. 等 5 秒
Start-Sleep -Seconds 5

# 3. 删除
Remove-Item -Path 'D:\a10\aikjx\code\my_lib\openUFT' -Recurse -Force
```

**C · Git Bash（删除受限目录）**：
```bash
# 重启 bash 进程后
rm -rf /d/a10/aikjx/code/my_lib/openUFT
```

### ⚠ 旧报告文件保留

工作区两个历史报告文件保留（改名记录）：

| 文件 | 用途 |
|---|---|
| `openUFT_改名与全维整理优化报告.md` | 第一次改名记录（alg_uft → openUFT） |
| `openUFT_版本总结与区分报告.md` | 版本总结报告 |

---

## 四、验证最终结果

```bash
$ cd openuft && python verify.py

一级目录：12/12 ✅
核心文档：11/11 ✅
开放问题占位：10 ✅
历史名清理：✅
定理谱完整：12/12 ✅
文档总数：79

🎉 总体通过：36/36 可验证项
```

---

## 五、工作区双目录当前状态

```
D:\a10\aikjx\code\my_lib\
├── openuft/                     ← ★ 新版（小写，对齐 GitHub URL）
│   ├── 79 md + 11 py + 93 文件
│   └── 1.3 MB · verify 36/36
│
├── openUFT/                     ← ⚠ 旧版（驼峰命名，保留待用户手动删除）
│
├── openUFT_改名与全维整理优化报告.md   ← 历史记录
└── openUFT_版本总结与区分报告.md       ← 历史记录
```

---

## 六、推送命令

```bash
cd D:/a10/aikjx/code/my_lib/openuft
git init
git add .
git commit -m "v4.0.2 initial commit (openuft lowercase)"
git tag v4.0.2
git remote add origin https://github.com/aikjx/openuft.git
git push -u origin main --tags
```

— AI科技星 · 2026-09-06 23:57
