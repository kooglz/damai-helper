#!/bin/bash

# 娱乐新闻视频生成脚本 - 纯色背景版

# 先生成中文语音（使用 say 命令）
TEXT="各位观众朋友们好，欢迎收看今日娱乐新闻！第一条，44 岁高云翔天津街边摊煎饼。第二条，26 岁林妙可逛庙会仍是娃娃脸。第三条，baby 聚会视频引关注。第四条，尹浩宇新 MV 上线。第五条，苏有朋演唱会合肥站落幕。感谢收看！"

# 使用 macOS 内置的中文语音
say -v Ting-Ting -o /tmp/news_audio.aiff "$TEXT"

# 转换格式
ffmpeg -y -i /tmp/news_audio.aiff -c:a libmp3lame -q:a 2 /tmp/news_audio.mp3

AUDIO_FILE="/tmp/news_audio.mp3"
OUTPUT_FILE="/Users/konglingzheng/.openclaw/workspace/entertainment_news_20260228_v2.mp4"

# 获取音频时长
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$AUDIO_FILE")
echo "音频时长：$DURATION 秒"

# 创建渐变背景视频
ffmpeg -y \
    -f lavfi -i "color=c=0x1a1a2e:s=1920x1080:d=$DURATION" \
    -i "$AUDIO_FILE" \
    -vf "format=yuv420p" \
    -c:v libx264 -preset medium -crf 18 \
    -c:a aac -b:a 192k \
    -shortest \
    "$OUTPUT_FILE"

echo "视频生成完成：$OUTPUT_FILE"
ls -lh "$OUTPUT_FILE"
