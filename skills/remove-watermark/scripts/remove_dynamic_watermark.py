#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态水印去除 - 使用 OpenCV inpaint 逐帧修复
"""

import cv2
import numpy as np
import subprocess
import os
import sys
import tempfile
import shutil
from pathlib import Path

def extract_frames(video_path, frames_dir):
    """提取所有视频帧"""
    cmd = [
        'ffmpeg', '-i', video_path,
        os.path.join(frames_dir, 'frame_%06d.png'),
        '-y'
    ]
    subprocess.run(cmd, check=True, capture_output=True)

def get_video_info(video_path):
    """获取视频信息"""
    # 获取尺寸
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
           '-show_entries', 'stream=width,height', '-of', 'csv=p=0', video_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    width, height = map(int, result.stdout.strip().split(','))
    
    # 获取帧率
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
           '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', video_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    fps = eval(result.stdout.strip())
    
    # 获取音频信息
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'a:0',
           '-show_entries', 'stream=codec_name', '-of', 'csv=p=0', video_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    has_audio = bool(result.stdout.strip())
    
    return width, height, fps, has_audio

def create_mask(height, width):
    """
    创建掩码 - 覆盖所有可能的水印区域
    返回一个黑白掩码图像，白色区域为需要修复的部分
    """
    mask = np.zeros((height, width), dtype=np.uint8)
    
    # 左上角：AI 生成 (固定位置)
    cv2.rectangle(mask, (5, 5), (100, 45), 255, -1)
    
    # 右下角区域：即梦 LOGO + @Wave&V5 夫妇日常
    cv2.rectangle(mask, (width-210, height-100), (width, height), 255, -1)
    
    # 左侧中部区域（可能出现在这里）
    cv2.rectangle(mask, (0, height//2-60), (210, height//2+60), 255, -1)
    
    # 右上角区域
    cv2.rectangle(mask, (width-210, 5), (width, 100), 255, -1)
    
    return mask

def process_frame(frame_path, output_path, mask):
    """使用 OpenCV inpaint 修复单帧"""
    frame = cv2.imread(str(frame_path))
    if frame is None:
        return False
    
    # 使用 Telea 算法进行 inpaint
    # 半径设为 3，算法为 INPAINT_TELEA 或 INPAINT_NS
    result = cv2.inpaint(frame, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    
    cv2.imwrite(str(output_path), result)
    return True

def main():
    if len(sys.argv) < 2:
        print("用法：python remove_dynamic_watermark.py <input_video> [output_video]")
        sys.exit(1)
    
    input_path = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else input_path.parent / f"{input_path.stem}_cleaned.mp4"
    
    if not input_path.exists():
        print(f"错误：文件不存在 {input_path}")
        sys.exit(1)
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp(prefix='watermark_remove_')
    frames_dir = os.path.join(temp_dir, 'frames')
    processed_dir = os.path.join(temp_dir, 'processed')
    os.makedirs(frames_dir)
    os.makedirs(processed_dir)
    
    try:
        print(f"📹 处理视频：{input_path}")
        print(f"📁 输出文件：{output_path}")
        
        # 获取视频信息
        width, height, fps, has_audio = get_video_info(str(input_path))
        print(f"📐 视频尺寸：{width}x{height}, 帧率：{fps:.2f}fps, 音频：{'有' if has_audio else '无'}")
        
        # 创建掩码
        print("🎭 创建水印掩码...")
        mask = create_mask(height, width)
        
        # 提取帧
        print("📸 提取视频帧...")
        extract_frames(str(input_path), frames_dir)
        
        # 处理每一帧
        print("🔧 逐帧修复水印...")
        frame_files = sorted(Path(frames_dir).glob('frame_*.png'))
        total = len(frame_files)
        
        for i, frame_path in enumerate(frame_files):
            output_frame = Path(processed_dir) / frame_path.name
            success = process_frame(frame_path, output_frame, mask)
            
            if not success:
                print(f"⚠️ 警告：处理失败 {frame_path.name}")
            
            if (i + 1) % 50 == 0:
                print(f"   进度：{i+1}/{total} ({(i+1)/total*100:.1f}%)")
        
        print(f"✅ 完成 {total} 帧处理")
        
        # 重新合成视频
        print("🎬 重新合成视频...")
        audio_map = ['-map', '0:a'] if has_audio else []
        audio_codec = ['-c:a', 'copy'] if has_audio else []
        
        cmd = [
            'ffmpeg', '-framerate', str(fps),
            '-i', os.path.join(processed_dir, 'frame_%06d.png'),
        ]
        
        if has_audio:
            cmd.extend(['-i', str(input_path)])
        
        cmd.extend([
            '-map', '0:v',
        ])
        
        if has_audio:
            cmd.extend(['-map', '1:a'])
        
        cmd.extend([
            '-c:v', 'libx265', '-crf', '18',
        ])
        
        if has_audio:
            cmd.extend(['-c:a', 'copy'])
        
        cmd.extend(['-y', str(output_path)])
        
        subprocess.run(cmd, check=True, capture_output=True)
        
        print(f"🎉 完成！输出文件：{output_path}")
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # 清理临时文件
        print("🧹 清理临时文件...")
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    main()
