#!/usr/bin/env python3
import markdown
from weasyprint import HTML, CSS
import sys

# 读取 Markdown 文件
with open('/Users/konglingzheng/.openclaw/workspace/AI插画商单报价指南.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# 转换为 HTML
html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

# 添加样式
styled_html = f'''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    @page {{
        size: A4;
        margin: 2cm;
        @bottom-center {{
            content: "第 " counter(page) " 页";
            font-size: 9pt;
            color: #666;
        }}
    }}
    body {{
        font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
        font-size: 11pt;
        line-height: 1.8;
        color: #333;
    }}
    h1 {{
        font-size: 24pt;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 30px;
        padding-bottom: 15px;
        border-bottom: 3px solid #333;
    }}
    h2 {{
        font-size: 16pt;
        color: #2c2c2c;
        margin-top: 25px;
        margin-bottom: 15px;
        padding-left: 10px;
        border-left: 4px solid #ff6b6b;
    }}
    h3 {{
        font-size: 13pt;
        color: #444;
        margin-top: 20px;
        margin-bottom: 10px;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        font-size: 10pt;
    }}
    th, td {{
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }}
    th {{
        background-color: #f5f5f5;
        font-weight: bold;
    }}
    tr:nth-child(even) {{
        background-color: #fafafa;
    }}
    code {{
        background-color: #f4f4f4;
        padding: 2px 6px;
        border-radius: 3px;
        font-family: monospace;
        font-size: 10pt;
    }}
    blockquote {{
        border-left: 4px solid #ff6b6b;
        margin: 15px 0;
        padding: 10px 20px;
        background-color: #f9f9f9;
        font-style: italic;
    }}
    ul, ol {{
        margin: 10px 0;
        padding-left: 25px;
    }}
    li {{
        margin: 5px 0;
    }}
    hr {{
        border: none;
        border-top: 2px solid #eee;
        margin: 25px 0;
    }}
    .page-break {{
        page-break-before: always;
    }}
</style>
</head>
<body>
{html_content}
</body>
</html>
'''

# 保存 HTML（可选）
with open('/Users/konglingzheng/.openclaw/workspace/AI插画商单报价指南.html', 'w', encoding='utf-8') as f:
    f.write(styled_html)

# 转换为 PDF
HTML(string=styled_html).write_pdf('/Users/konglingzheng/.openclaw/workspace/AI插画商单报价指南.pdf')

print("✅ PDF 生成成功！")
print("📄 文件位置：/Users/konglingzheng/.openclaw/workspace/AI插画商单报价指南.pdf")
