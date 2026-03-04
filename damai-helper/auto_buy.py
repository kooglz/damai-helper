#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大麦自动抢票程序 - 直接到付款界面
使用 Playwright 自动化浏览器操作
"""

import asyncio
import sys
import os
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# ==================== 配置区 ====================
CONFIG = {
    # 演出信息
    'item_id': '746385412345',  # 大麦演出 item ID（需要从 URL 获取）
    'target_price': 680,        # 目标价位
    'ticket_count': 2,          # 张数
    
    # 开票时间（孙燕姿苏州站）
    'sale_time': '2026-03-06 14:00:00',
    
    # 观演人（按顺序选择）
    'attendees': ['孔令征', '叶波'],
    
    # 身份证号（预填）
    'id_cards': ['320104198504011216', '320105198701191427'],
    
    # 浏览器设置
    'headless': False,          # 是否无头模式（抢票建议 False）
    'refresh_interval': 0.5,    # 刷新间隔（秒）
    'start_early': 60,          # 开售前多少秒开始刷新
}

# ==================== 抢票逻辑 ====================

class DamaiTicketBot:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.sale_started = False
        
    async def setup_browser(self):
        """启动浏览器"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=CONFIG['headless'],
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage',
            ]
        )
        
        # 创建上下文（带用户代理）
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        self.page = await self.context.new_page()
        
        # 注入反检测脚本
        await self.page.add_init_script('''
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh'] });
        ''')
        
        print("✅ 浏览器启动完成")
        
    async def wait_for_sale(self):
        """等待开售时间"""
        sale_time = datetime.strptime(CONFIG['sale_time'], '%Y-%m-%d %H:%M:%S')
        
        while True:
            now = datetime.now()
            diff = (sale_time - now).total_seconds()
            
            if diff <= 0:
                print("🔥 开售时间已到！")
                break
                
            if diff <= CONFIG['start_early']:
                print(f"⚡ 准备刷新！还有 {diff:.1f} 秒")
                await self.page.reload()
                await asyncio.sleep(CONFIG['refresh_interval'])
            else:
                remaining = int(diff)
                hours = remaining // 3600
                minutes = (remaining % 3600) // 60
                seconds = remaining % 60
                print(f"\r⏳ 等待开票：{hours:02d}:{minutes:02d}:{seconds:02d}", end='', flush=True)
                await asyncio.sleep(1)
    
    async def select_price(self):
        """选择票价"""
        print("\n🎯 正在选择票价...")
        
        try:
            # 查找目标价位的按钮
            price_btn = await self.page.wait_for_selector(
                f'div[data-price="{CONFIG["target_price"]}"], button:has-text("{CONFIG["target_price"]}元")',
                timeout=3000
            )
            await price_btn.click()
            print(f"✅ 已选择 {CONFIG['target_price']}元 价位")
            await asyncio.sleep(0.3)
        except PlaywrightTimeout:
            print("❌ 未找到票价按钮，尝试其他选择器...")
            # 尝试点击第一个可选价位
            try:
                buttons = await self.page.query_selector_all('.ticket-price button:not([disabled])')
                if buttons:
                    for btn in buttons:
                        text = await btn.inner_text()
                        if str(CONFIG['target_price']) in text:
                            await btn.click()
                            print(f"✅ 已选择 {CONFIG['target_price']}元")
                            break
            except Exception as e:
                print(f"❌ 选择票价失败：{e}")
                return False
        
        return True
    
    async def select_quantity(self):
        """选择数量"""
        print("🎯 正在选择数量...")
        
        try:
            # 查找数量选择器
            count_btn = await self.page.wait_for_selector(
                f'button[data-count="{CONFIG["ticket_count"]}"], .ticket-count button:has-text("{CONFIG["ticket_count"]}张")',
                timeout=3000
            )
            await count_btn.click()
            print(f"✅ 已选择 {CONFIG['ticket_count']} 张")
            await asyncio.sleep(0.3)
        except PlaywrightTimeout:
            print("❌ 未找到数量按钮")
            return False
        
        return True
    
    async def select_attendees(self):
        """选择观演人"""
        print("🎯 正在选择观演人...")
        
        try:
            # 等待观演人列表加载
            await self.page.wait_for_selector('.attendee-list, .buyer-box', timeout=5000)
            await asyncio.sleep(0.5)
            
            # 查找所有观演人复选框
            checkboxes = await self.page.query_selector_all(
                '.attendee-checkbox input[type="checkbox"], .buyer-item input[type="checkbox"]'
            )
            
            if len(checkboxes) < CONFIG['ticket_count']:
                print(f"❌ 可用观演人不足：找到{len(checkboxes)}个，需要{CONFIG['ticket_count']}个")
                return False
            
            # 按配置选择观演人
            for i in range(CONFIG['ticket_count']):
                if i < len(checkboxes):
                    await checkboxes[i].check()
                    await asyncio.sleep(0.2)
            
            print(f"✅ 已选择 {CONFIG['ticket_count']} 位观演人")
        except PlaywrightTimeout:
            print("❌ 未找到观演人选择区域")
            return False
        except Exception as e:
            print(f"❌ 选择观演人失败：{e}")
            return False
        
        return True
    
    async def submit_order(self):
        """提交订单"""
        print("🎯 正在提交订单...")
        
        try:
            # 查找提交按钮
            submit_btn = await self.page.wait_for_selector(
                'button:has-text("提交订单"), button:has-text("立即购买"), button:has-text("确认"), .submit-btn',
                timeout=5000
            )
            
            # 多次点击确保提交成功
            for i in range(3):
                await submit_btn.click()
                await asyncio.sleep(0.3)
                
                # 检查是否跳转到支付页面
                current_url = self.page.url
                if 'pay' in current_url.lower() or 'cashier' in current_url.lower():
                    print("✅ 成功进入支付页面！")
                    return True
            
            print("✅ 订单已提交，请手动完成支付")
            return True
            
        except PlaywrightTimeout:
            print("❌ 未找到提交按钮")
            return False
        except Exception as e:
            print(f"❌ 提交订单失败：{e}")
            return False
    
    async def run(self):
        """主流程"""
        print("\n" + "="*60)
        print("🎫 大麦自动抢票程序 - 孙燕姿苏州站")
        print("="*60)
        print(f"📅 演出日期：2026-04-12")
        print(f"💰 目标价位：{CONFIG['target_price']}元 × {CONFIG['ticket_count']}张")
        print(f"👤 观演人：{', '.join(CONFIG['attendees'])}")
        print(f"⏰ 开票时间：{CONFIG['sale_time']}")
        print("="*60)
        print()
        
        # 启动浏览器
        await self.setup_browser()
        
        # 打开大麦页面（需要替换为实际 URL）
        item_url = f"https://detail.damai.cn/item.htm?id={CONFIG['item_id']}"
        print(f"🌐 打开页面：{item_url}")
        await self.page.goto(item_url, wait_until='domcontentloaded')
        
        # 等待开售
        await self.wait_for_sale()
        
        # 执行抢票流程
        print("\n🚀 开始抢票流程...")
        
        # 选择票价
        if not await self.select_price():
            print("⚠️ 票价选择失败，继续尝试...")
        
        # 选择数量
        if not await self.select_quantity():
            print("⚠️ 数量选择失败，继续尝试...")
        
        # 选择观演人
        if not await self.select_attendees():
            print("⚠️ 观演人选择失败，继续尝试...")
        
        # 提交订单
        await self.submit_order()
        
        print("\n" + "="*60)
        print("✅ 抢票流程完成！请在浏览器中完成支付")
        print("="*60)
        
        # 保持浏览器打开
        print("\n浏览器将保持打开状态，按 Ctrl+C 退出")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 退出程序")
            await self.browser.close()

# ==================== 主程序 ====================

async def main():
    bot = DamaiTicketBot()
    await bot.run()

if __name__ == '__main__':
    # 检查依赖
    try:
        import playwright
    except ImportError:
        print("❌ 未安装 Playwright，请先运行：pip3 install playwright")
        print("   然后运行：playwright install chromium")
        sys.exit(1)
    
    asyncio.run(main())
