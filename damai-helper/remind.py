#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大麦抢票桌面提醒助手
功能：开售倒计时、弹窗提醒、多平台同步
"""

import time
import datetime
import sys
import os
from datetime import datetime as dt

# ==================== 配置区 ====================
CONFIG = {
    'concert_name': '孙燕姿《就在日落以后》巡回演唱会 - 苏州',
    'concert_date': '2026-04-12',
    'sale_time': '2026-03-06 14:00:00',  # 孙燕姿苏州站开票时间
    'target_price': 680,
    'ticket_count': 2,
    'venue': '苏州奥林匹克体育中心体育场',
    'attendees': [
        {'name': '叶波', 'id': '320105198701191427'},
        {'name': '孔令征', 'id': '320104198504011216'}
    ],
}

# ==================== 提醒功能 ====================

def send_mac_notification(title, message):
    """发送 macOS 系统通知"""
    try:
        os.system(f'''osascript -e 'display notification "{message}" with title "{title}"' ''')
        print(f"📬 通知：{title} - {message}")
    except Exception as e:
        print(f"通知发送失败：{e}")

def send_sound_alert():
    """播放提示音"""
    try:
        os.system('afplay /System/Library/Sounds/Glass.aiff')
    except:
        pass

def get_countdown():
    """计算倒计时"""
    sale_time = dt.strptime(CONFIG['sale_time'], '%Y-%m-%d %H:%M:%S')
    now = dt.now()
    diff = sale_time - now

    if diff.total_seconds() <= 0:
        return {'started': True, 'seconds': 0}

    return {
        'started': False,
        'total_seconds': int(diff.total_seconds()),
        'hours': diff.seconds // 3600,
        'minutes': (diff.seconds % 3600) // 60,
        'seconds': diff.seconds % 60,
        'days': diff.days
    }

def format_countdown(countdown):
    """格式化倒计时显示"""
    if countdown['started']:
        return "🔥 开售中！"

    if countdown['days'] > 0:
        return f"{countdown['days']}天 {countdown['hours']:02d}:{countdown['minutes']:02d}:{countdown['seconds']:02d}"
    else:
        return f"{countdown['hours']:02d}:{countdown['minutes']:02d}:{countdown['seconds']:02d}"

def print_status():
    """打印当前状态"""
    print("\n" + "="*60)
    print(f"🎫 {CONFIG['concert_name']}")
    print("="*60)
    print(f"📅 演出日期：{CONFIG['concert_date']}")
    print(f"🏟️ 演出场馆：{CONFIG['venue']}")
    print(f"💰 目标价位：{CONFIG['target_price']}元 × {CONFIG['ticket_count']}张")
    print(f"⏰ 开票时间：{CONFIG['sale_time']}")
    print("="*60)

def countdown_display():
    """主倒计时循环"""
    print_status()
    print("\n🚀 抢票提醒助手已启动... (按 Ctrl+C 退出)\n")

    last_notification_minute = -1
    last_sound_minute = -1

    try:
        while True:
            countdown = get_countdown()
            time_str = format_countdown(countdown)

            # 清屏并显示倒计时
            os.system('clear' if os.name != 'nt' else 'cls')
            print_status()

            print(f"\n⏳ 倒计时：{time_str}")

            if countdown['started']:
                print("\n🔥🔥🔥 开售了！立即抢票！🔥🔥🔥")
                send_mac_notification("🔥 开售了！", "立即抢票！")
                send_sound_alert()
                break

            # 整分钟提醒
            current_minute = countdown['total_seconds'] // 60
            if current_minute != last_notification_minute and current_minute in [60, 30, 15, 10, 5, 3, 1]:
                send_mac_notification(f"⏰ 抢票提醒", f"还有{current_minute}分钟开售")
                last_notification_minute = current_minute

            # 最后 10 秒声音提醒
            if countdown['total_seconds'] <= 10 and countdown['total_seconds'] > 0:
                if last_sound_minute != current_minute:
                    send_sound_alert()
                    last_sound_minute = current_minute
                    print(f"\n⚡ 准备！{countdown['total_seconds']}秒后开售!")

            # 最后 1 分钟显示秒数
            if countdown['total_seconds'] <= 60:
                print(f"\n⚡ 最后冲刺！准备好！")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n\n👋 提醒助手已退出")
        sys.exit(0)

def test_notification():
    """测试通知功能"""
    print("🔔 测试通知...")
    send_mac_notification("测试通知", "如果你看到这条消息，说明通知功能正常！")
    send_sound_alert()
    print("✅ 通知测试完成")

# ==================== 主程序 ====================

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        test_notification()
    else:
        countdown_display()
