#!/bin/bash

# 娱乐新闻视频生成脚本（简化版）

AUDIO_FILE="/tmp/openclaw/tts-qqXsQ4/voice-1772292529001.mp3"
OUTPUT_FILE="/Users/konglingzheng/.openclaw/workspace/entertainment_news_20260228.mp4"

# 获取音频时长
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$AUDIO_FILE")
echo "音频时长：$DURATION 秒"

# 创建简单视频背景 + 音频
ffmpeg -y \
    -f lavfi -i "smptebars=s=1920x1080:d=$DURATION" \
    -i "$AUDIO_FILE" \
    -c:v libx264 -preset medium -crf 23 \
    -c:a aac -b:a 192k \
    -shortest \
    "$OUTPUT_FILE"

echo "视频生成完成：$OUTPUT_FILE"
ls -lh "$OUTPUT_FILE"
