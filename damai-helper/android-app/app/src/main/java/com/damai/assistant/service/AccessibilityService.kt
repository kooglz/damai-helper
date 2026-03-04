package com.damai.assistant.service

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.AccessibilityServiceInfo
import android.content.Intent
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import com.damai.assistant.MainActivity

/**
 * 大麦无障碍抢票服务
 * 
 * 功能：
 * - 自动点击"立即购买"按钮
 * - 自动选择票价
 * - 自动选择张数
 * - 自动勾选观演人
 * - 自动提交订单
 */
class AccessibilityService : AccessibilityService() {

    companion object {
        const val TAG = "DamaiAccessibility"
        
        // 大麦 APP 包名
        const val DAMAI_PACKAGE_NAME = "cn.damai"
        
        // 关键按钮文本
        const val BTN_BUY_NOW = "立即购买"
        const val BTN_CONFIRM = "确认"
        const val BTN_SUBMIT = "提交订单"
        const val BTN_PAY = "立即支付"
        
        // 操作状态
        var isGrabbing = false
        var currentStep = GrabStep.IDLE
    }

    enum class GrabStep {
        IDLE,           // 空闲
        WAIT_SALE,      // 等待开售
        SELECT_PRICE,   // 选择票价
        SELECT_COUNT,   // 选择张数
        SELECT_ATTENDEE,// 选择观演人
        SUBMIT_ORDER,   // 提交订单
        COMPLETE        // 完成
    }

    private val handler = Handler(Looper.getMainLooper())
    private var saleTimeMillis: Long = 0

    override fun onServiceConnected() {
        super.onServiceConnected()
        Log.d(TAG, "无障碍服务已连接")
        
        val info = AccessibilityServiceInfo().apply {
            eventTypes = AccessibilityEvent.TYPES_ALL_MASK
            feedbackType = AccessibilityServiceInfo.FEEDBACK_GENERIC
            flags = AccessibilityServiceInfo.FLAG_INCLUDE_NOT_IMPORTANT_VIEWS or
                    AccessibilityServiceInfo.FLAG_REPORT_VIEW_IDS or
                    AccessibilityServiceInfo.FLAG_REQUEST_ENHANCED_WEB_ACCESSIBILITY
            notificationTimeout = 100
        }
        serviceInfo = info
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        if (event == null || !isGrabbing) return

        val packageName = event.packageName?.toString() ?: return
        if (packageName != DAMAI_PACKAGE_NAME) return

        when (event.eventType) {
            AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED -> {
                handleWindowStateChanged(event)
            }
            AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED -> {
                handleContentChanged(event)
            }
        }
    }

    private fun handleWindowStateChanged(event: AccessibilityEvent) {
        val source = event.source ?: return
        Log.d(TAG, "窗口状态变化：${event.className}")

        when (currentStep) {
            GrabStep.WAIT_SALE -> {
                // 检查是否已开售
                if (isSaleStarted(source)) {
                    currentStep = GrabStep.SELECT_PRICE
                    Log.d(TAG, "已开售，开始选择票价")
                }
            }
            GrabStep.SELECT_PRICE -> {
                // 自动选择票价
                selectPriceLevel(source)
            }
            GrabStep.SELECT_COUNT -> {
                // 自动选择张数
                selectTicketCount(source)
            }
            GrabStep.SELECT_ATTENDEE -> {
                // 自动选择观演人
                selectAttendees(source)
            }
            GrabStep.SUBMIT_ORDER -> {
                // 自动提交订单
                submitOrder(source)
            }
            else -> {}
        }
    }

    private fun handleContentChanged(event: AccessibilityEvent) {
        if (currentStep == GrabStep.WAIT_SALE && System.currentTimeMillis() >= saleTimeMillis) {
            currentStep = GrabStep.SELECT_PRICE
        }
    }

    private fun isSaleStarted(root: AccessibilityNodeInfo): Boolean {
        // 检查"立即购买"按钮是否可点击
        val buyButtons = findNodesByText(root, BTN_BUY_NOW)
        for (btn in buyButtons) {
            if (btn.isEnabled && btn.isClickable) {
                Log.d(TAG, "发现可点击的购买按钮")
                return true
            }
        }
        return false
    }

    private fun selectPriceLevel(root: AccessibilityNodeInfo) {
        val prefs = getSharedPreferences("damai_config", MODE_PRIVATE)
        val targetPrice = prefs.getString(MainActivity.CONFIG_KEY_PRICE_LEVEL, "680") ?: "680"
        
        Log.d(TAG, "正在选择 $targetPrice 元价位")
        
        // 查找价格按钮
        val priceNodes = findNodesByText(root, "${targetPrice}元")
        if (priceNodes.isNotEmpty()) {
            clickNode(priceNodes[0])
            Log.d(TAG, "已点击 $targetPrice 元价位")
            currentStep = GrabStep.SELECT_COUNT
            
            // 延迟后选择张数
            handler.postDelayed({
                currentStep = GrabStep.SELECT_COUNT
            }, 500)
        }
    }

    private fun selectTicketCount(root: AccessibilityNodeInfo) {
        val prefs = getSharedPreferences("damai_config", MODE_PRIVATE)
        val ticketCount = prefs.getString(MainActivity.CONFIG_KEY_TICKET_COUNT, "2") ?: "2"
        
        Log.d(TAG, "正在选择 $ticketCount 张")
        
        // 查找张数按钮
        val countNodes = findNodesByText(root, "${ticketCount}张")
        if (countNodes.isNotEmpty()) {
            clickNode(countNodes[0])
            Log.d(TAG, "已选择 $ticketCount 张")
            currentStep = GrabStep.SELECT_ATTENDEE
            
            // 延迟后选择观演人
            handler.postDelayed({
                currentStep = GrabStep.SELECT_ATTENDEE
            }, 500)
        }
    }

    private fun selectAttendees(root: AccessibilityNodeInfo) {
        val prefs = getSharedPreferences("damai_config", MODE_PRIVATE)
        val ticketCount = (prefs.getString(MainActivity.CONFIG_KEY_TICKET_COUNT, "2") ?: "2").toInt()
        
        // 获取配置的观演人姓名
        val attendeeNames = listOf("孔令征", "叶波")
        
        Log.d(TAG, "正在选择 $ticketCount 位观演人：${attendeeNames.take(ticketCount)}")
        
        // 查找包含观演人姓名的复选框
        var selectedCount = 0
        
        for (i in 0 until minOf(ticketCount, attendeeNames.size)) {
            val targetName = attendeeNames[i]
            Log.d(TAG, "查找观演人：$targetName")
            
            // 查找包含姓名的节点
            val nameNodes = findNodesByText(root, targetName)
            for (node in nameNodes) {
                // 查找附近的复选框
                val checkbox = findNearbyCheckbox(node)
                if (checkbox != null && !checkbox.isChecked) {
                    clickNode(checkbox)
                    selectedCount++
                    Log.d(TAG, "已选择观演人：$targetName")
                    checkbox.recycle()
                    break
                }
                node.recycle()
            }
        }
        
        // 如果没找到姓名，尝试按顺序选择前 N 个复选框
        if (selectedCount < ticketCount) {
            Log.d(TAG, "未找到姓名匹配，尝试按顺序选择")
            val checkboxes = findNodesByClassName(root, "android.widget.CheckBox")
            for (checkbox in checkboxes) {
                if (selectedCount >= ticketCount) break
                if (!checkbox.isChecked) {
                    clickNode(checkbox)
                    selectedCount++
                }
                checkbox.recycle()
            }
        }
        
        if (selectedCount >= ticketCount) {
            Log.d(TAG, "观演人选择完成，共选择 $selectedCount 位")
            currentStep = GrabStep.SUBMIT_ORDER
            
            // 延迟后提交订单
            handler.postDelayed({
                currentStep = GrabStep.SUBMIT_ORDER
            }, 800)
        }
    }
    
    private fun findNearbyCheckbox(node: AccessibilityNodeInfo): AccessibilityNodeInfo? {
        // 尝试在父节点中查找复选框
        var parent = node.parent
        while (parent != null) {
            for (i in 0 until parent.childCount) {
                val child = parent.getChild(i)
                if (child != null) {
                    if (child.className?.toString() == "android.widget.CheckBox") {
                        return child
                    }
                    child.recycle()
                }
            }
            val grandParent = parent.parent
            parent.recycle()
            parent = grandParent
        }
        return null
    }

    private fun submitOrder(root: AccessibilityNodeInfo) {
        Log.d(TAG, "正在提交订单")
        
        // 优先查找"提交订单"按钮
        var submitNodes = findNodesByText(root, BTN_SUBMIT)
        if (submitNodes.isEmpty()) {
            // 查找"确认"按钮
            submitNodes = findNodesByText(root, BTN_CONFIRM)
        }
        if (submitNodes.isEmpty()) {
            // 查找"立即购买"按钮
            submitNodes = findNodesByText(root, BTN_BUY_NOW)
        }
        
        if (submitNodes.isNotEmpty()) {
            clickNode(submitNodes[0])
            Log.d(TAG, "订单已提交！")
            currentStep = GrabStep.COMPLETE
            
            // 发送完成通知
            sendCompletionNotification()
        }
    }

    private fun findNodesByText(root: AccessibilityNodeInfo, text: String): List<AccessibilityNodeInfo> {
        val result = mutableListOf<AccessibilityNodeInfo>()
        findNodesByTextRecursive(root, text, result)
        return result
    }

    private fun findNodesByTextRecursive(
        node: AccessibilityNodeInfo,
        text: String,
        result: MutableList<AccessibilityNodeInfo>
    ) {
        val nodeText = node.text?.toString() ?: ""
        if (nodeText.contains(text, ignoreCase = true)) {
            result.add(node)
        }

        for (i in 0 until node.childCount) {
            val child = node.getChild(i)
            if (child != null) {
                findNodesByTextRecursive(child, text, result)
                child.recycle()
            }
        }
    }

    private fun findNodesByClassName(root: AccessibilityNodeInfo, className: String): List<AccessibilityNodeInfo> {
        val result = mutableListOf<AccessibilityNodeInfo>()
        findNodesByClassNameRecursive(root, className, result)
        return result
    }

    private fun findNodesByClassNameRecursive(
        node: AccessibilityNodeInfo,
        className: String,
        result: MutableList<AccessibilityNodeInfo>
    ) {
        if (node.className?.toString() == className) {
            result.add(node)
        }

        for (i in 0 until node.childCount) {
            val child = node.getChild(i)
            if (child != null) {
                findNodesByClassNameRecursive(child, className, result)
                child.recycle()
            }
        }
    }

    private fun clickNode(node: AccessibilityNodeInfo) {
        if (node.isEnabled && node.isClickable) {
            node.performAction(AccessibilityNodeInfo.ACTION_CLICK)
        } else {
            // 尝试父节点
            var parent = node.parent
            while (parent != null) {
                if (parent.isEnabled && parent.isClickable) {
                    parent.performAction(AccessibilityNodeInfo.ACTION_CLICK)
                    parent.recycle()
                    break
                }
                val grandParent = parent.parent
                parent.recycle()
                parent = grandParent
            }
        }
    }

    private fun sendCompletionNotification() {
        val notification = android.app.NotificationCompat.Builder(this, TicketGrabService.CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle("✅ 订单已提交！")
            .setContentText("请在 15 分钟内完成支付")
            .setPriority(android.app.NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .build()

        val notificationManager = getSystemService(android.app.NotificationManager::class.java)
        notificationManager.notify(System.currentTimeMillis().toInt(), notification)
    }

    override fun onInterrupt() {
        Log.d(TAG, "服务被中断")
        isGrabbing = false
        currentStep = GrabStep.IDLE
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, "服务已销毁")
        handler.removeCallbacksAndMessages(null)
        isGrabbing = false
        currentStep = GrabStep.IDLE
    }

    /**
     * 开始抢票
     */
    fun startGrabbing(saleTime: Long) {
        isGrabbing = true
        currentStep = GrabStep.WAIT_SALE
        saleTimeMillis = saleTime
        Log.d(TAG, "开始抢票，开售时间：$saleTimeMillis")
    }

    /**
     * 停止抢票
     */
    fun stopGrabbing() {
        isGrabbing = false
        currentStep = GrabStep.IDLE
        handler.removeCallbacksAndMessages(null)
        Log.d(TAG, "停止抢票")
    }
}
