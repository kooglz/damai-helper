---
name: remove-watermark
description: "视频水印处理工具箱。用于去除视频静态水印（如即梦AI生成视频的水印）、添加Logo水印、视频/图片高清化放大。Use when: 用户需要处理视频水印（去除或添加）、视频超分辨率放大、图片放大。"
metadata: { "openclaw": { "emoji": "🎬" } }
---

# Remove Watermark - 视频水印处理工具箱

基于 GitHub 开源项目 [remove_watermark](https://github.com/johnson7788/remove_watermark) 的视频处理工具集合。

## 功能

- **去除视频水印** - 自动检测并去除视频中的静态水印（适用于即梦等AI生成视频）
- **添加Logo水印** - 为视频添加Logo，支持多种位置、大小和透明度调节
- **视频高清化** - 使用 AI 超分辨率技术将视频放大 2x/3x/4x
- **图片高清化** - 单张图片超分辨率放大

## 依赖安装

### macOS

```bash
# 安装 FFmpeg
brew install ffmpeg

# 安装 Python 依赖
pip install numpy scipy imageio

# 安装 upscayl-cli（用于视频/图片高清化）
# 参考: https://github.com/upscayl/upscayl-ncnn
```

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install ffmpeg python3-pip
pip3 install numpy scipy imageio
```

## 使用方法

### 1. 去除视频水印

自动检测并去除视频中的静态水印：

```bash
# 基本用法（输出自动命名为 input_cleaned.mp4）
python scripts/remove_video_watermark.py input.mp4

# 指定输出文件
python scripts/remove_video_watermark.py input.mp4 output.mp4

# 增加关键帧数量以提高检测精度
python scripts/remove_video_watermark.py input.mp4 -k 100

# 显示详细处理过程
python scripts/remove_video_watermark.py input.mp4 -v
```

**工作原理：**
1. 提取多个关键帧
2. 通过分析多帧图像的梯度差异定位水印区域
3. 使用 FFmpeg 的 `removelogo` 滤镜修复水印区域

### 2. 添加 Logo 水印

为视频添加 Logo 水印：

```bash
# 基本用法（Logo 默认添加在右下角）
python scripts/add_logo.py input.mp4 logo.png

# 指定位置和输出
python scripts/add_logo.py input.mp4 logo.png -p top-right -o output.mp4

# 完整参数示例
python scripts/add_logo.py input.mp4 logo.png -p bottom-right -s 0.2 -o 0.8 -m 20
```

**参数说明：**
- `-p, --position`: Logo 位置 (`top-left`, `top-right`, `bottom-left`, `bottom-right`, `center`)
- `-s, --scale`: Logo 缩放比例（默认 0.15，即视频宽度的 15%）
- `-o, --opacity`: 透明度 0.0~1.0（默认 1.0，完全不透明）
- `-m, --margin`: 距边缘像素间距（默认 10px）

**推荐：** 使用 PNG 透明背景图片效果最佳。

### 3. 视频高清化

使用 upscayl 对视频逐帧超分辨率放大：

```bash
# 默认 4x 放大
python scripts/upscale_video.py input.mp4

# 2x 放大
python scripts/upscale_video.py input.mp4 -s 2

# 指定输出路径
python scripts/upscale_video.py input.mp4 -s 4 -o output_hd.mp4

# 4 线程并发加速
python scripts/upscale_video.py input.mp4 -w 4 -v
```

**可用模型：**
- `upscayl-standard-2x/3x/4x` - 通用图片
- `upscayl-photo-4x` - 照片优化
- `upscayl-anime-4x` - 动漫/插画

### 4. 图片高清化

```bash
# 默认 4x 放大
python scripts/upscale_image.py -i input.png -o output.png

# 2x 放大
python scripts/upscale_image.py -i input.jpg -o output.png -s 2

# 使用照片优化模型
python scripts/upscale_image.py -i input.jpg -o output.png -n upscayl-photo-4x
```

## 完整工作流示例

去除水印 → 高清化 → 添加自己的 Logo：

```bash
# 1. 去除原视频水印
python scripts/remove_video_watermark.py test_video.mp4 -v

# 2. 高清化（4x放大）
python scripts/upscale_video.py test_video_cleaned.mp4 -s 4 -w 4

# 3. 添加自己的 Logo
python scripts/add_logo.py test_video_cleaned_upscaled.mp4 mylogo.png -p top-right -s 0.1
```

## 注意事项

- 水印去除仅适用于**静态水印**（位置和内容不随时间变化）
- 视频高清化需要较长时间，建议使用多线程 (`-w` 参数)
- 输出视频使用 H.265 编码，兼容性较好
- 处理前请确保有足够的磁盘空间（临时帧文件可能很大）

## 故障排除

**水印检测不准确：**
- 增加关键帧数量 `-k 100` 或更多
- 确保水印在视频中是静态的
- 确保水印有足够的梯度差异

**处理速度太慢：**
- 使用 `-w` 参数增加并发线程数
- 降低放大倍数（使用 `-s 2` 代替 `-s 4`）

**upscayl 未找到：**
- 确保已安装 upscayl-cli
- 检查模型文件是否已下载到 `~/.upscayl-cli/resources/models`
