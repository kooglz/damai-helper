#!/bin/bash

# 大麦抢票助手 - APK 构建脚本

set -e

echo "🎫 大麦抢票助手 - APK 构建工具"
echo "================================"
echo ""

# 检查 Gradle
if ! command -v gradle &> /dev/null; then
    echo "⚠️  未检测到 Gradle，使用 Gradle Wrapper..."
    GRADLE_CMD="./gradlew"
else
    GRADLE_CMD="gradle"
fi

# 检查 Wrapper
if [ ! -f "./gradlew" ]; then
    echo "❌ 未找到 Gradle Wrapper"
    echo "请先在 Android Studio 中打开项目生成 Wrapper"
    exit 1
fi

# 构建
echo "🔨 开始构建 Debug 版本..."
$GRADLE_CMD assembleDebug

# 检查输出
APK_PATH="app/build/outputs/apk/debug/app-debug.apk"
if [ -f "$APK_PATH" ]; then
    echo ""
    echo "✅ 构建成功！"
    echo ""
    echo "📦 APK 位置：$APK_PATH"
    echo ""
    echo "📱 安装到设备:"
    echo "   adb install -r $APK_PATH"
    echo ""
    echo "📤 或通过文件传输到手机安装"
else
    echo ""
    echo "❌ 构建失败，未找到 APK 文件"
    exit 1
fi
