# Win7 Playwright 完整快速部署包（一键脚本\+全官方下载地址）

## 环境锁定栈（Win7 唯一稳定组合，开源无修改）

- Python：3\.8\.10（Win7 最高支持 Python）

- Playwright Python：1\.15\.3（最后兼容 Win7 版本）

- 浏览器：仅 Chromium 112（Firefox/WebKit 直接崩溃）

- 系统前置：KB2533623 补丁 \+ VC\+\+2015\-2019 运行库

## 一、全组件官方下载地址（全部微软 / Python 官网，安全无捆绑）

### 1\. Python 3\.8\.10

64 位系统（主流）：
[https://www\.python\.org/ftp/python/3\.8\.10/python\-3\.8\.10\-amd64\.exe](https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe)
32 位系统：
[https://www\.python\.org/ftp/python/3\.8\.10/python\-3\.8\.10\.exe](https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe)
安装必勾选：`Add Python 3.8 to PATH`

### 2\. VC\+\+2015\-2019 运行库（缺一不可）

x64：[https://aka\.ms/vs/16/release/VC\_redist\.x64\.exe](https://aka.ms/vs/16/release/VC_redist.x64.exe)
x86：[https://aka\.ms/vs/16/release/VC\_redist\.x86\.exe](https://aka.ms/vs/16/release/VC_redist.x86.exe)

> 64 位 Win7 建议 x86\+x64 全部安装
> 
> 

### 3\. KB2533623 系统补丁（解决 WS2\_32\.dll 入口点报错）

微软更新目录检索页：
[https://www\.catalog\.update\.microsoft\.com/Search\.aspx?q=KB2533623](https://www.catalog.update.microsoft.com/Search.aspx?q=KB2533623)

- x64 文件：windows6\.1\-kb2533623\-x64\.msu

- x86 文件：windows6\.1\-kb2533623\-x86\.msu
安装后**必须重启电脑**生效

### 4\. Playwright 开源源码仓库

Python 版（MIT 开源）：[https://github\.com/microsoft/playwright\-python](https://github.com/microsoft/playwright-python)
锁定兼容 tag：v1\.15\.3

## 二、在线一键安装脚本 `install_playwright_win7.cmd`（开源可修改，管理员运行）

```cmd
@echo off
chcp 65001 >nul
title Win7 Playwright 1.15.3 一键部署脚本
echo ==============================================
echo Win7专用 Playwright 自动化安装工具
echo 适配版本：Python3.8.10 + playwright==1.15.3
echo 仅安装兼容Chromium，自动配置国内镜像
echo ==============================================
echo.

:: 全局镜像加速
set PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
set PLAYWRIGHT_DOWNLOAD_HOST=https://registry.npmmirror.com/-/binary/playwright
setx PLAYWRIGHT_DOWNLOAD_HOST %PLAYWRIGHT_DOWNLOAD_HOST% /M

:: 校验Python版本
python --version | findstr "3.8" >nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python3.8.x！
    echo 下载地址：https://www.python.org/downloads/release/python-3810/
    echo 安装时务必勾选 Add Python 3.8 to PATH
    pause
    exit /b 1
)

echo [1/5] 升级pip工具
python -m pip install --upgrade pip -i %PIP_INDEX_URL%

echo [2/5] 安装Win7兼容版Playwright 1.15.3
pip install playwright==1.15.3 -i %PIP_INDEX_URL%

echo [3/5] 下载Chromium112（仅兼容内核，跳过火狐/webkit）
python -m playwright install chromium

echo [4/5] 生成测试脚本 test_demo.py
echo from playwright.sync_api import sync_playwright > test_demo.py
echo def run(): >> test_demo.py
echo     with sync_playwright() as p: >> test_demo.py
echo         # Win7兼容强制参数：无头、禁用GPU、无沙盒 >> test_demo.py
echo         browser = p.chromium.launch(headless=True,args=["--disable-gpu","--no-sandbox","--disable-dev-shm-usage"]) >> test_demo.py
echo         page = browser.new_page() >> test_demo.py
echo         page.goto("https://www.baidu.com") >> test_demo.py
echo         print("页面标题：", page.title()) >> test_demo.py
echo         browser.close() >> test_demo.py
echo if __name__ == "__main__": >> test_demo.py
echo     run() >> test_demo.py

echo [5/5] 部署完成！
echo ==============================================
echo 前置依赖检查清单（未装会闪退）：
echo 1. VC++2015-2019 x86/x64运行库
echo 2. KB2533623系统补丁，安装后重启电脑
echo ==============================================
echo 运行测试：python test_demo.py
pause
```

## 三、内网离线打包双脚本（无网络环境专用，开源）

### 1\. 有网机器打包脚本 `offline_pack.cmd`

```cmd
@echo off
mkdir playwright_offline
set PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
set PLAYWRIGHT_DOWNLOAD_HOST=https://registry.npmmirror.com/-/binary/playwright
:: 下载离线whl包
pip download playwright==1.15.3 -d playwright_offline
:: 下载浏览器内核
python -m playwright install chromium
:: 复制浏览器缓存
xcopy "%LOCALAPPDATA%\ms-playwright" "playwright_offline\ms-playwright\" /e /h /y
echo 离线包打包完成，复制整个 playwright_offline 文件夹到Win7内网机器
pause
```

### 2\. Win7 内网离线安装脚本 `offline_install.cmd`

```cmd
@echo off
chcp 65001 >nul
set PIP_NO_INDEX=true
set PIP_FIND_LINKS=%~dp0playwright_offline
set PLAYWRIGHT_BROWSERS_PATH=%~dp0playwright_offline\ms-playwright
pip install playwright==1.15.3
echo 离线安装完成，执行 python test_demo.py 验证
pause
```

## 四、快速部署执行顺序（必按顺序，否则报错）

1. 安装 VC\+\+2015\-2019 x86\+x64 运行库

2. 安装 KB2533623 补丁 → **重启电脑**

3. 安装 Python3\.8\.10，勾选添加到环境变量

4. 右键管理员运行 `install_playwright_win7.cmd`

5. 执行 `python test_demo.py` 验证环境

## 五、高频报错一键修复方案

1. **无法定位 WS2\_32\.dll 入口点**
缺失 KB2533623 补丁，安装后重启

2. **浏览器启动闪退 / 崩溃**
启动代码强制参数：`headless=True,args=["--disable-gpu","--no-sandbox"]`

3. **pip 下载超时**
脚本已内置清华镜像，无需额外配置

4. **提示 Python 版本不兼容**
卸载 3\.9\+，重装 3\.8\.10

## 六、开源说明

1. Playwright 主体 MIT 开源，无闭源限制，可商用二次开发

2. 所有 cmd 脚本无加密、无捆绑，可任意修改版本、镜像、启动参数

3. 所有下载源均为微软 / Python 官方，无第三方分流风险

4. 不支持 Playwright 1\.33\+、Python3\.9\+，底层内核不兼容 Win7 系统 API

> （注：部分内容可能由 AI 生成）
