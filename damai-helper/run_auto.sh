#!/bin/bash
# 大麦自动抢票程序 - 启动脚本

echo "🎫 大麦自动抢票程序"
echo "================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3"
    exit 1
fi

# 检查 Playwright
if ! python3 -c "import playwright" 2>/dev/null; then
    echo "❌ Playwright 未安装，运行：pip3 install playwright"
    echo "   然后运行：python3 -m playwright install chromium"
    exit 1
fi

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "📋 抢票配置："
echo "   演出：孙燕姿《就在日落以后》巡回演唱会 - 苏州"
echo "   日期：2026-04-12"
echo "   价位：¥680 × 2 张"
echo "   观演人：孔令征、叶波"
echo "   开票：2026-03-13 10:00:00"
echo ""

# 提醒用户确认配置
echo "⚠️  使用前请确认："
echo "   1. 已在 auto_buy.py 中填写正确的 item_id（从大麦 URL 获取）"
echo "   2. 已登录大麦账号（浏览器会打开，需手动登录）"
echo "   3. 已提前填写好观演人信息（在大麦 APP 或网站）"
echo ""

read -p "是否继续？(y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "👋 已取消"
    exit 0
fi

echo ""
echo "🚀 启动抢票程序..."
echo "   浏览器将自动打开，请在开售前保持页面登录状态"
echo "   按 Ctrl+C 可随时退出"
echo ""
echo "================================"
echo ""

python3 "$SCRIPT_DIR/auto_buy.py"
