#!/usr/bin/env python3
import markdown

# 读取2026版Markdown文件
with open('/Users/konglingzheng/.openclaw/workspace/AI插画商单报价指南2026.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# 转换为 HTML
html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

# 添加2026年专属样式
styled_html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>AI插画商单报价指南 2026修订版 - KOOG</title>
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
        font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
        font-size: 11pt;
        line-height: 1.8;
        color: #333;
        max-width: 210mm;
        margin: 0 auto;
        padding: 20px;
        background: #f5f5f5;
    }}
    .container {{
        background: white;
        padding: 40px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }}
    h1 {{
        font-size: 28pt;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 20px;
        padding-bottom: 20px;
        border-bottom: 4px solid #ff6b6b;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    .subtitle {{
        text-align: center;
        color: #666;
        font-size: 12pt;
        margin-bottom: 30px;
    }}
    .badge {{
        display: inline-block;
        background: #ff6b6b;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 10pt;
        margin: 0 5px;
    }}
    h2 {{
        font-size: 16pt;
        color: white;
        margin-top: 35px;
        margin-bottom: 20px;
        padding: 12px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }}
    h3 {{
        font-size: 14pt;
        color: #444;
        margin-top: 25px;
        margin-bottom: 15px;
        padding-left: 15px;
        border-left: 4px solid #ff6b6b;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 10pt;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-radius: 8px;
        overflow: hidden;
    }}
    th, td {{
        border: 1px solid #e0e0e0;
        padding: 12px;
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
        background-color: #e3f2fd;
    }}
    code {{
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
        color: white;
        padding: 3px 10px;
        border-radius: 15px;
        font-family: "Consolas", "Monaco", monospace;
        font-size: 10pt;
    }}
    blockquote {{
        border-left: 4px solid #ff6b6b;
        margin: 20px 0;
        padding: 20px 25px;
        background: linear-gradient(135deg, #fff5f5 0%, #ffe0e0 100%);
        border-radius: 0 10px 10px 0;
        font-style: italic;
        position: relative;
    }}
    blockquote:before {{
        content: """;
        font-size: 40pt;
        color: #ff6b6b;
        position: absolute;
        top: -10px;
        left: 10px;
        opacity: 0.3;
    }}
    ul, ol {{
        margin: 15px 0;
        padding-left: 30px;
    }}
    li {{
        margin: 10px 0;
        position: relative;
    }}
    li:before {{
        content: "▸";
        color: #667eea;
        font-weight: bold;
        position: absolute;
        left: -20px;
    }}
    hr {{
        border: none;
        height: 3px;
        background: linear-gradient(90deg, #ff6b6b, #667eea, #764ba2);
        margin: 35px 0;
        border-radius: 2px;
    }}
    strong {{
        color: #ff6b6b;
        font-weight: bold;
        background: linear-gradient(120deg, transparent 0%, #fff3cd 0%, #fff3cd 100%, transparent 100%);
        background-size: 100% 40%;
        background-position: 0 90%;
        background-repeat: no-repeat;
    }}
    .highlight-box {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        margin: 25px 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }}
    .warning-box {{
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        margin: 25px 0;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }}
    .success-box {{
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        margin: 25px 0;
        box-shadow: 0 4px 15px rgba(0, 184, 148, 0.3);
    }}
    pre {{
        background: linear-gradient(135deg, #2d3436 0%, #000000 100%);
        color: #00cec9;
        padding: 20px;
        border-radius: 10px;
        overflow-x: auto;
        font-family: "Consolas", "Monaco", monospace;
        font-size: 10pt;
        line-height: 1.6;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}
    .print-btn {{
        position: fixed;
        top: 30px;
        right: 30px;
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        border: none;
        padding: 18px 35px;
        border-radius: 30px;
        font-size: 14pt;
        cursor: pointer;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
        transition: all 0.3s ease;
        font-weight: bold;
        z-index: 1000;
    }}
    .print-btn:hover {{
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.6);
    }}
    .year-badge {{
        display: inline-block;
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        font-size: 11pt;
        font-weight: bold;
        margin: 10px 0;
    }}
    @media print {{
        .print-btn {{ display: none !important; }}
        body {{
            padding: 0;
            max-width: 100%;
            background: white;
        }}
        .container {{
            box-shadow: none;
            padding: 20px;
        }}
    }}
</style>
</head>
<body>
<button class="print-btn no-print" onclick="window.print()">🖨️ 点击保存为 PDF</button>
<div class="container">
<div style="text-align: center; margin-bottom: 30px;">
<span class="year-badge">🚀 2026年AI浪潮特辑</span>
<span class="year-badge">📉 市场下行应对版</span>
</div>
{html_content}
</div>
<script>
    window.onafterprint = function() {{
        console.log('打印完成！');
    }};
</script>
</body>
</html>'''

# 保存 HTML
with open('/Users/konglingzheng/.openclaw/workspace/AI插画商单报价指南2026.html', 'w', encoding='utf-8') as f:
    f.write(styled_html)

print("✅ 2026修订版 HTML 文件生成成功！")
print("📄 文件位置：/Users/konglingzheng/.openclaw/workspace/AI插画商单报价指南2026.html")
print("")
print("🎯 2026年版本特色：")
print("   • 基于AI浪潮冲击的市场下行现状")
print("   • 新增'从卖图到卖服务'的转型策略")
print("   • 增加AI培训、企业顾问等高价值业务")
print("   • 包含2026-2027年趋势预判")
print("")
print("💡 使用说明：")
print("1. 用浏览器打开 HTML 文件")
print("2. 点击右上角的 '🖨️ 点击保存为 PDF' 按钮")
print("3. 打印设置选择 A4，勾选'背景图形'")
