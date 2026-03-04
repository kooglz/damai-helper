// ==UserScript==
// @name         大麦抢票助手 - 孙燕姿苏州站
// @namespace    https://github.com/koogaiclaw
// @version      1.0.0
// @description  大麦抢票辅助工具 - 倒计时、预填信息、快速提交（孙燕姿苏州 4.12）
// @author       Koogaiclaw
// @match        https://detail.damai.cn/*
// @match        https://m.damai.cn/*
// @match        https://www.damai.cn/*
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_notification
// @grant        GM_addStyle
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';

    // ==================== 配置区 ====================
    const CONFIG = {
        // 演出信息
        concertName: '孙燕姿《就在日落以后》巡回演唱会 - 苏州',
        concertDate: '2026-04-12',  // 目标日期
        targetPrice: 680,            // 目标价位
        ticketCount: 2,              // 张数

        // 抢票时间（孙燕姿苏州站）
        saleTime: '2026-03-06T14:00:00+08:00',  // 开票时间

        // 观演人信息（已配置）
        attendees: [
            { name: '叶波', idType: '身份证', idCard: '320105198701191427' },
            { name: '孔令征', idType: '身份证', idCard: '320104198504011216' }
        ],

        // 自动刷新设置
        autoRefresh: true,
        refreshInterval: 500,  // 刷新间隔（毫秒）
        startRefreshBefore: 60,  // 开售前多少秒开始刷新
    };

    // ==================== 工具函数 ====================

    // 获取服务器时间（模拟）
    function getServerTime() {
        return new Date().getTime();
    }

    // 倒计时计算
    function getCountdown() {
        const saleTime = new Date(CONFIG.saleTime).getTime();
        const now = getServerTime();
        const diff = saleTime - now;

        if (diff <= 0) {
            return { started: true, seconds: 0 };
        }

        return {
            started: false,
            seconds: Math.floor(diff / 1000),
            minutes: Math.floor(diff / 60000),
            hours: Math.floor(diff / 3600000)
        };
    }

    // 发送通知
    function sendNotification(title, message) {
        if (typeof GM_notification !== 'undefined') {
            GM_notification({ title, text: message });
        } else {
            console.log(`[通知] ${title}: ${message}`);
        }
    }

    // ==================== UI 组件 ====================

    // 添加倒计时浮窗
    function createCountdownOverlay() {
        const overlay = document.createElement('div');
        overlay.id = 'damai-countdown';
        overlay.innerHTML = `
            <div class="countdown-box">
                <div class="countdown-title">🎫 孙燕姿苏州站抢票倒计时</div>
                <div class="countdown-time" id="countdown-display">--:--:--</div>
                <div class="countdown-info">
                    <div>目标：${CONFIG.targetPrice}元 × ${CONFIG.ticketCount}张</div>
                    <div>日期：${CONFIG.concertDate}</div>
                </div>
                <div class="countdown-status" id="countdown-status">等待开票</div>
            </div>
        `;

        GM_addStyle(`
            #damai-countdown {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 99999;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            .countdown-box {
                background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 100%);
                color: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(255,107,53,0.4);
                min-width: 280px;
                text-align: center;
            }
            .countdown-title {
                font-size: 14px;
                font-weight: 600;
                margin-bottom: 10px;
            }
            .countdown-time {
                font-size: 36px;
                font-weight: 700;
                font-family: 'Courier New', monospace;
                margin: 10px 0;
            }
            .countdown-info {
                font-size: 12px;
                opacity: 0.9;
                margin: 10px 0;
            }
            .countdown-status {
                font-size: 12px;
                padding: 4px 12px;
                background: rgba(255,255,255,0.2);
                border-radius: 20px;
                display: inline-block;
            }
            .countdown-status.ready {
                background: #4CAF50;
            }
            .countdown-status.go {
                background: #f44336;
                animation: pulse 0.5s infinite;
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
        `);

        document.body.appendChild(overlay);
        return overlay;
    }

    // 更新倒计时显示
    function updateCountdown() {
        const display = document.getElementById('countdown-display');
        const status = document.getElementById('countdown-status');
        if (!display || !status) return;

        const countdown = getCountdown();

        if (countdown.started) {
            display.textContent = '开售中!';
            status.textContent = '🔥 立即抢票!';
            status.className = 'countdown-status go';
        } else {
            const hours = String(countdown.hours || 0).padStart(2, '0');
            const minutes = String(countdown.minutes % 60).padStart(2, '0');
            const seconds = String(countdown.seconds % 60).padStart(2, '0');
            display.textContent = `${hours}:${minutes}:${seconds}`;

            if (countdown.seconds <= 10) {
                status.textContent = '⚡ 准备!';
                status.className = 'countdown-status go';
            } else if (countdown.seconds <= 60) {
                status.textContent = '🎯 即将开始';
                status.className = 'countdown-status ready';
            } else {
                status.textContent = '⏰ 等待开票';
                status.className = 'countdown-status';
            }
        }
    }

    // 添加快速选择按钮
    function createQuickSelectButtons() {
        const container = document.createElement('div');
        container.id = 'damai-quick-select';
        container.innerHTML = `
            <button class="quick-btn" data-price="${CONFIG.targetPrice}">
                💨 一键选择${CONFIG.targetPrice}元
            </button>
            <button class="quick-btn count-btn" data-count="${CONFIG.ticketCount}">
                 选择${CONFIG.ticketCount}张
            </button>
        `;

        GM_addStyle(`
            #damai-quick-select {
                position: fixed;
                bottom: 100px;
                right: 20px;
                z-index: 99999;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .quick-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(102,126,234,0.4);
                transition: transform 0.1s;
            }
            .quick-btn:active {
                transform: scale(0.95);
            }
            .quick-btn:hover {
                box-shadow: 0 6px 20px rgba(102,126,234,0.6);
            }
        `);

        document.body.appendChild(container);

        // 绑定事件
        container.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                if (this.classList.contains('count-btn')) {
                    selectTicketCount(CONFIG.ticketCount);
                } else {
                    selectPrice(CONFIG.targetPrice);
                }
            });
        });
    }

    // 选择票价
    function selectPrice(price) {
        const priceButtons = document.querySelectorAll(`[data-price="${price}"], .price-btn`);
        priceButtons.forEach(btn => {
            if (btn.textContent.includes(price) || btn.dataset.price == price) {
                btn.click();
                sendNotification('已选择价位', `${price}元`);
            }
        });
    }

    // 选择张数
    function selectTicketCount(count) {
        const countButtons = document.querySelectorAll('.ticket-count button');
        countButtons.forEach(btn => {
            if (btn.textContent.includes(count) || btn.dataset.count == count) {
                btn.click();
                sendNotification('已选择张数', `${count}张`);
            }
        });
    }

    // 预填观演人信息
    function fillAttendeeInfo() {
        // 查找观演人选择区域并自动选择
        const attendeeCheckboxes = document.querySelectorAll('.attendee-checkbox input[type="checkbox"]');
        if (attendeeCheckboxes.length >= CONFIG.ticketCount) {
            for (let i = 0; i < CONFIG.ticketCount; i++) {
                attendeeCheckboxes[i].click();
            }
            sendNotification('已选择观演人', `${CONFIG.ticketCount}位`);
        }
    }

    // ==================== 主程序 ====================

    function init() {
        console.log('[大麦助手] 初始化完成');

        // 创建倒计时
        createCountdownOverlay();

        // 创建快捷按钮
        createQuickSelectButtons();

        // 启动倒计时更新
        setInterval(updateCountdown, 500);

        // 监听页面变化
        const observer = new MutationObserver(() => {
            // 页面元素变化时检查是否需要自动操作
            const countdown = getCountdown();
            if (countdown.started && countdown.seconds < 5) {
                // 刚开售几秒内，可以尝试自动选择
                console.log('[大麦助手] 开售中，准备抢票');
            }
        });

        observer.observe(document.body, { childList: true, subtree: true });

        // 开售提醒
        const checkSaleTime = setInterval(() => {
            const countdown = getCountdown();
            if (countdown.seconds === 10) {
                sendNotification('⚡ 准备!', '还有 10 秒开售!');
            }
            if (countdown.seconds === 0 && !countdown.started) {
                sendNotification('🔥 开售了!', '立即抢票!');
            }
        }, 1000);
    }

    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
