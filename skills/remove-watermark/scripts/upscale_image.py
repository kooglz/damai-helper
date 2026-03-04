#!/usr/bin/env python3
"""
图片高清化工具

使用 upscayl CLI 对图片进行超分辨率放大。
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def upscale_image(input_path: str, output_path: str, model_name: str,
                  scale: int, model_path: str, fmt: str = "png"):
    """使用 upscayl 放大单张图片"""
    cmd = [
        "upscayl", "run",
        "-i", input_path,
        "-o", output_path,
        "-m", model_path,
        "-n", model_name,
        "-s", str(scale),
        "-f", fmt,
    ]
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="图片高清化工具 - 使用 upscayl 超分辨率放大图片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python upscale_image.py -i input.png -o output.png              # 默认 4x 放大
  python upscale_image.py -i input.png -o output.png -s 2         # 2x 放大
  python upscale_image.py -i input.jpg -o output.png -n upscayl-photo-4x  # 使用照片优化模型

可用模型:
  upscayl-standard-2x    2x 通用图片
  upscayl-standard-3x    3x 通用图片
  upscayl-standard-4x    4x 通用图片（默认）
  upscayl-photo-4x       4x 照片优化
  upscayl-anime-4x       4x 动漫/插画
        """
    )
    parser.add_argument("-i", "--input", required=True, help="输入图片路径")
    parser.add_argument("-o", "--output", required=True, help="输出图片路径")
    parser.add_argument("-s", "--scale", type=int, default=4, choices=[2, 3, 4],
                        help="放大倍数（2/3/4，默认: 4）")
    parser.add_argument("-n", "--model", default="upscayl-standard-4x",
                        help="模型名称（默认: upscayl-standard-4x）")
    parser.add_argument("-m", "--model-path",
                        default=str(Path.home() / ".upscayl-cli/resources/models"),
                        help="模型文件夹路径")
    parser.add_argument("-f", "--format", default="png",
                        choices=["png", "jpg", "webp"],
                        help="输出格式（默认: png）")

    args = parser.parse_args()

    # 验证输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_path}")
        sys.exit(1)

    # 检查 upscayl 是否可用
    if not shutil.which("upscayl"):
        print("错误: 未找到 upscayl，请确认已安装 upscayl-cli")
        sys.exit(1)

    # 检查模型路径
    model_path = Path(args.model_path)
    if not model_path.exists():
        print(f"错误: 模型路径不存在: {model_path}")
        print("请先安装 upscayl-cli 并下载模型")
        sys.exit(1)

    try:
        print(f"处理: {input_path}")
        print(f"模型: {args.model}, 放大倍数: {args.scale}x")
        upscale_image(
            str(input_path),
            args.output,
            args.model,
            args.scale,
            str(model_path),
            args.format
        )
        print(f"完成: {args.output}")
    except subprocess.CalledProcessError as e:
        print(f"错误: upscayl 处理失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
