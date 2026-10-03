# 复制章节文件到最终出版版目录的脚本

$sourceDir = "d:\a10\aikjx\code\my_lib\utf\12-书籍\人人都能理解统一场论\V6"
$destDir = "d:\a10\aikjx\code\my_lib\utf\12-书籍\人人都能理解统一场论\最终出版版"

# 章节映射表
$chapterMap = @{
    "第三章：时空同一化原理.md" = "03-第三章：时空同一化原理.md"
    "第四章：观察者中心论.md" = "04-第四章：观察者中心论.md"
    "第五章：质量的几何定义.md" = "05-第五章：质量的几何定义.md"
    "第六章：电荷的几何定义.md" = "06-第六章：电荷的几何定义.md"
    "第七章：引力场的几何定义.md" = "07-第七章：引力场的几何定义.md"
    "第八章：电磁场的几何起源.md" = "08-第八章：电磁场的几何起源.md"
    "第九章：核心耦合常数.md" = "09-第九章：核心耦合常数.md"
    "第十章：统一动量方程.md" = "10-第十章：统一动量方程.md"
    "第十一章：统一力方程.md" = "11-第十一章：统一力方程.md"
    "第十二章：引力-电磁统一机制.md" = "12-第十二章：引力-电磁统一机制.md"
    "第十三章：时间势差效应.md" = "13-第十三章：时间势差效应.md"
    "第十四章：光速不变原理的几何解释.md" = "14-第十四章：光速不变原理的几何解释.md"
    "第十五章：量子现象的几何化尝试.md" = "15-第十五章：量子现象的几何化尝试.md"
    "第十六章：宇称不守恒的几何起源.md" = "16-第十六章：宇称不守恒的几何起源.md"
    "第十七章：人工场的本质.md" = "17-第十七章：人工场的本质.md"
    "第十八章：光速飞行与飞碟原理.md" = "18-第十八章：光速飞行与飞碟原理.md"
    "第十九章：能量革命.md" = "19-第十九章：能量革命.md"
    "第二十章：意识与生命.md" = "20-第二十章：意识与生命.md"
    "第二十一章：医疗与制造.md" = "21-第二十一章：医疗与制造.md"
    "第二十二章：反引力场.md" = "22-第二十二章：反引力场.md"
    "第二十三章：数学自洽验证.md" = "23-第二十三章：数学自洽验证.md"
    "第二十四章：实验证据引用.md" = "24-第二十四章：实验证据引用.md"
    "第二十五章：与主流理论的差异与冲突.md" = "25-第二十五章：与主流理论的差异与冲突.md"
    "第二十六章：理论的现状与未来.md" = "26-第二十六章：理论的现状与未来.md"
}

# 复制章节文件
foreach ($sourceName in $chapterMap.Keys) {
    $destName = $chapterMap[$sourceName]
    $sourcePath = Join-Path -Path $sourceDir -ChildPath $sourceName
    $destPath = Join-Path -Path $destDir -ChildPath $destName
    
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination $destPath -Force
        Write-Host "复制成功: $sourceName -> $destName"
    } else {
        Write-Host "文件不存在: $sourceName"
    }
}

# 复制附录文件
$appendices = @(
    "附录一：核心内容速查表.md",
    "附录二：数学附录.md",
    "附录三：实验设计指南.md",
    "附录四：技术应用展望.md",
    "附录五：常见问题解答.md",
    "附录六：进一步阅读推荐.md",
    "附录七：术语表.md",
    "附录八：作者的故事.md"
)

foreach ($appendix in $appendices) {
    $sourcePath = Join-Path -Path $sourceDir -ChildPath $appendix
    $destPath = Join-Path -Path $destDir -ChildPath $appendix
    
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination $destPath -Force
        Write-Host "复制成功: $appendix"
    } else {
        Write-Host "文件不存在: $appendix"
    }
}

Write-Host "所有文件复制完成！"
