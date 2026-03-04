#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多位置水印去除脚本 - 处理视频中动态位置的水印
"""

import argparse
import subprocess
import os
import sys
import tempfile
import shutil
from pathlib import Path

def extract_frames(video_path, output_dir, fps=1):
    """提取视频帧"""
    cmd = [
        'ffmpeg', '-i', video_path,
        '-vf', f'fps={fps}',
        '-q:v', '2',
        os.path.join(output_dir, 'frame_%04d.png')
    ]
    subprocess.run(cmd, check=True, capture_output=True)

def get_frame_count(video_path):
    """获取视频总帧数"""
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-count_packets',
        '-show_entries', 'stream=nb_read_packets',
        '-of', 'csv=p=0',
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return int(result.stdout.strip())

def process_frame_with_inpaint(frame_path, output_path, mask_areas):
    """
    使用 ffmpeg 处理单帧的水印
    mask_areas: [(x, y, w, h), ...] 水印区域列表
    """
    # 构建滤镜链 - 对每个水印区域使用模糊覆盖
    filters = []
    for x, y, w, h in mask_areas:
        # 使用高斯模糊覆盖水印区域
        filters.append(f'delogo=x={x}:y={y}:w={w}:h={h}')
    
    filter_complex = ','.join(filters)
    
    cmd = [
        'ffmpeg', '-i', frame_path,
        '-vf', filter_complex,
        '-y', output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)

def create_mask_image(width, height, mask_areas, output_path):
    """创建掩码图片用于 removelogo"""
    # 创建黑色背景
    cmd = [
        'ffmpeg', '-f', 'lavfi',
        '-i', f'color=c=black:s={width}x{height}',
        '-y', output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    
    # 在掩码上绘制白色矩形（水印区域）
    draw_expr = '+'.join([f'drawbox=x={x}:y={y}:w={w}:h={h}:color=white@1:t=fill' for x, y, w, h in mask_areas])
    cmd = [
        'ffmpeg', '-i', output_path,
        '-vf', draw_expr,
        '-y', output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)

def main():
    parser = argparse.ArgumentParser(description='去除视频中多位置的水印')
    parser.add_argument('input', help='输入视频文件')
    parser.add_argument('-o', '--output', help='输出视频文件')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细输出')
    args = parser.parse_args()
    
    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"错误：文件不存在 {input_path}")
        sys.exit(1)
    
    output_path = Path(args.output).resolve() if args.output else input_path.parent / f"{input_path.stem}_cleaned.mp4"
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp(prefix='watermark_remove_')
    frames_dir = os.path.join(temp_dir, 'frames')
    processed_dir = os.path.join(temp_dir, 'processed')
    os.makedirs(frames_dir)
    os.makedirs(processed_dir)
    
    try:
        # 获取视频信息
        print(f"处理视频：{input_path}")
        print(f"输出文件：{output_path}")
        
        # 获取视频尺寸
        probe_cmd = [
            'ffprobe', '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'csv=p=0',
            str(input_path)
        ]
        result = subprocess.run(probe_cmd, capture_output=True, text=True)
        width, height = map(int, result.stdout.strip().split(','))
        print(f"视频尺寸：{width}x{height}")
        
        # 定义所有可能的水印区域（根据视频尺寸调整）
        # 左上角：AI 生成
        # 右下角/左侧/右上角：即梦 LOGO + @Wave&V5 夫妇日常
        mask_areas = [
            (10, 10, 90, 35),           # 左上角 AI 生成
            (520, 1100, 200, 80),       # 右下角
            (10, 600, 200, 80),         # 左侧中部
            (520, 10, 200, 80),         # 右上角
        ]
        
        # 提取所有帧
        print("提取视频帧...")
        total_frames = get_frame_count(str(input_path))
        print(f"总帧数：{total_frames}")
        
        extract_frames(str(input_path), frames_dir, fps=0)  # 提取所有帧
        
        # 处理每一帧
        print("处理帧...")
        frame_files = sorted(Path(frames_dir).glob('frame_*.png'))
        processed_count = 0
        
        for frame_path in frame_files:
            output_frame = os.path.join(processed_dir, frame_path.name)
            
            # 使用 delogo 滤镜处理所有水印区域
            filter_parts = []
            for x, y, w, h in mask_areas:
                filter_parts.append(f'delogo=x={x}:y={y}:w={w}:h={h}')
            
            filter_complex = ','.join(filter_parts)
            
            cmd = [
                'ffmpeg', '-i', str(frame_path),
                '-vf', filter_complex,
                '-y', output_frame
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            processed_count += 1
            
            if args.verbose and processed_count % 50 == 0:
                print(f"已处理 {processed_count}/{len(frame_files)} 帧")
        
        print(f"完成 {processed_count} 帧处理")
        
        # 重新合成视频
        print("重新合成视频...")
        cmd = [
            'ffmpeg', '-framerate', '24',
            '-i', os.path.join(processed_dir, 'frame_%04d.png'),
            '-i', str(input_path),
            '-map', '0:v', '-map', '1:a',
            '-c:v', 'libx265', '-crf', '18',
            '-c:a', 'copy',
            '-y', str(output_path)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        
        print(f"✅ 完成！输出文件：{output_path}")
        
    finally:
        # 清理临时文件
        print("清理临时文件...")
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    main()
