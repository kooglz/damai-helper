#!/usr/bin/env python3
import markdown

# 读取 Markdown 文件
with open('/Users/konglingzheng/.openclaw/workspace/AI插画商单报价指南.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# 转换为 HTML
html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

# 添加样式
styled_html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>AI插画商单报价指南 - KOOG</title>
<style>
    @media print {{
        @page {{
            size: A4;
            margin: 2cm;
            @bottom-center {{
                content: "第 " counter(page) " 页";
                font-size: 9pt;
                color: #666;
            }}
        }}
        .no-print {{ display: none; }}
    }}
    body {{
        font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
        font-size: 11pt;
        line-height: 1.8;
        color: #333;
        max-width: 210mm;
        margin: 0 auto;
        padding: 20px;
    }}
    h1 {{
        font-size: 26pt;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 30px;
        padding-bottom: 20px;
        border-bottom: 4px solid #ff6b6b;
    }}
    h1:after {{
        content: "by KOOG";
        display: block;
        font-size: 12pt;
        color: #666;
        margin-top: 10px;
        font-weight: normal;
    }}
    h2 {{
        font-size: 16pt;
        color: #2c2c2c;
        margin-top: 30px;
        margin-bottom: 15px;
        padding: 10px 15px;
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
        color: white;
        border-radius: 5px;
    }}
    h3 {{
        font-size: 14pt;
        color: #444;
        margin-top: 25px;
        margin-bottom: 12px;
        padding-left: 15px;
        border-left: 4px solid #ff6b6b;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 10pt;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    th, td {{
        border: 1px solid #ddd;
        padding: 10px;
        text-align: left;
    }}
    th {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
    }}
    tr:nth-child(even) {{
        background-color: #f8f9fa;
    }}
    tr:hover {{
        background-color: #e9ecef;
    }}
    code {{
        background-color: #f4f4f4;
        padding: 3px 8px;
        border-radius: 4px;
        font-family: "Consolas", "Monaco", monospace;
        font-size: 10pt;
        color: #e83e8c;
    }}
    blockquote {{
        border-left: 4px solid #ff6b6b;
        margin: 20px 0;
        padding: 15px 25px;
        background: linear-gradient(135deg, #fff5f5 0%, #ffe0e0 100%);
        border-radius: 0 8px 8px 0;
        font-style: italic;
    }}
    ul, ol {{
        margin: 15px 0;
        padding-left: 30px;
    }}
    li {{
        margin: 8px 0;
    }}
    li:before {{
        content: "✓ ";
        color: #28a745;
        font-weight: bold;
    }}
    hr {{
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #ff6b6b, #667eea);
        margin: 30px 0;
    }}
    strong {{
        color: #ff6b6b;
        font-weight: bold;
    }}
    .highlight {{
        background: linear-gradient(120deg, #ffeaa7 0%, #ffeaa7 100%);
        background-repeat: no-repeat;
        background-size: 100% 40%;
        background-position: 0 88%;
        padding: 0 4px;
    }}
    .tip-box {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }}
    .warning-box {{
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }}
    pre {{
        background-color: #2d2d2d;
        color: #f8f8f2;
        padding: 20px;
        border-radius: 8px;
        overflow-x: auto;
        font-family: "Consolas", "Monaco", monospace;
        font-size: 10pt;
        line-height: 1.5;
    }}
    .print-btn {{
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 30px;
        font-size: 14pt;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }}
    .print-btn:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }}
    @media print {{
        .print-btn {{ display: none !important; }}
        body {{
            padding: 0;
            max-width: 100%;
        }}
    }}
</style>
</head>
<body>
<button class="print-btn no-print" onclick="window.print()">🖨️ 点击保存为 PDF</button>
{html_content}
<script>
    // 打印完成后可以执行的操作
    window.onafterprint = function() {{
        console.log('打印完成！');
    }};
</script>
</body>
</html>'''

# 保存 HTML
with open('/Users/konglingzheng/.openclaw/workspace/AI插画商单报价指南.html', 'w', encoding='utf-8') as f:
    f.write(styled_html)

print("✅ HTML 文件生成成功！")
print("📄 文件位置：/Users/konglingzheng/.openclaw/workspace/AI插画商单报价指南.html")
print("")
print("💡 使用说明：")
print("1. 用浏览器打开 HTML 文件")
print("2. 点击右上角的 '🖨️ 点击保存为 PDF' 按钮")
print("3. 或按 Ctrl+P / Cmd+P 选择'另存为 PDF'")
print("")
print("🎯 提示：在打印设置中，选择：")
print("   - 纸张：A4")
print("   - 边距：默认")
print("   - 勾选'背景图形'（可显示彩色背景）")
