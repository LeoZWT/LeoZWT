# GitHub 动态语言统计更新脚本
# PowerShell 版本

Write-Host "🚀 正在更新GitHub语言统计..." -ForegroundColor Cyan
Write-Host ""

# 检查Python是否安装
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✅ Python已安装: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 错误: 未找到Python，请先安装Python" -ForegroundColor Red
    Write-Host "下载地址: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "按任意键退出"
    exit 1
}

# 检查.env文件是否存在
if (-not (Test-Path ".env")) {
    Write-Host "❌ 错误: 未找到.env文件" -ForegroundColor Red
    Write-Host "请复制.env.example为.env并填入你的GitHub token" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "获取GitHub token: https://github.com/settings/tokens" -ForegroundColor Blue
    Write-Host "需要权限: repo (访问私有仓库)" -ForegroundColor Blue
    Read-Host "按任意键退出"
    exit 1
}

# 安装依赖
Write-Host "📦 检查并安装依赖..." -ForegroundColor Yellow
try {
    pip install requests python-dotenv --quiet
    Write-Host "✅ 依赖安装完成" -ForegroundColor Green
} catch {
    Write-Host "⚠️  依赖安装可能有问题，继续尝试运行..." -ForegroundColor Yellow
}

Write-Host ""

# 运行生成器
Write-Host "🎨 正在生成语言统计SVG..." -ForegroundColor Magenta
try {
    python generate_lang_stats.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ 语言统计已更新！" -ForegroundColor Green
        Write-Host "📁 文件位置: assets\lang-stats-dynamic.svg" -ForegroundColor Cyan
        
        # 检查文件是否存在
        if (Test-Path "assets\lang-stats-dynamic.svg") {
            $fileSize = (Get-Item "assets\lang-stats-dynamic.svg").Length
            Write-Host "📊 文件大小: $([math]::Round($fileSize/1KB, 2)) KB" -ForegroundColor Gray
        }
    } else {
        Write-Host ""
        Write-Host "❌ 生成失败，请检查错误信息" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ 运行出错: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "💡 提示: 你也可以设置GitHub Actions来自动更新" -ForegroundColor Blue
Read-Host "按任意键退出"