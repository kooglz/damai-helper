#!/bin/bash
# 大麦抢票助手 - 一键启动脚本
# 功能：启动桌面提醒 + 打开大麦页面

echo "🎫 大麦抢票助手 - 孙燕姿苏州站"
echo "================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python3"
    exit 1
fi

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "✅ 配置文件位置：$SCRIPT_DIR"
echo ""
echo "📋 已配置的观演人信息："
echo "   1. 叶波 (320105198701191427)"
echo "   2. 孔令征 (320104198504011216)"
echo ""
echo "🎯 目标：¥680 × 2 张 (4 月 12 日)"
echo ""

# 询问是否测试通知
read -p "🔔 是否先测试通知功能？(y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "测试通知中..."
    python3 "$SCRIPT_DIR/remind.py" --test
    echo ""
fi

# 询问是否打开大麦页面
read -p "🌐 是否打开大麦演出页面？(y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "打开大麦页面..."
    # 孙燕姿苏州站大麦页面（请确认实际 URL）
    open "https://detail.damai.cn/item.htm" 2>/dev/null || echo "请手动打开大麦 APP 或网站"
    echo ""
fi

# 启动倒计时提醒
echo "🚀 启动倒计时提醒..."
echo "   按 Ctrl+C 退出提醒"
echo ""
echo "================================"
echo ""

python3 "$SCRIPT_DIR/remind.py"
