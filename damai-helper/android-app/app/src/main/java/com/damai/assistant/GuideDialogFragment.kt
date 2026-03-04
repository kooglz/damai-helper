package com.damai.assistant

import android.app.AlertDialog
import android.app.Dialog
import android.os.Bundle
import android.view.LayoutInflater
import android.widget.TextView
import androidx.fragment.app.DialogFragment

class GuideDialogFragment : DialogFragment() {

    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        val view = LayoutInflater.from(requireContext())
            .inflate(R.layout.dialog_guide, null)

        val tvGuide = view.findViewById<TextView>(R.id.tvGuide)
        tvGuide.text = buildGuideText()

        return AlertDialog.Builder(requireContext())
            .setTitle("📖 抢票攻略")
            .setView(view)
            .setPositiveButton("知道了", null)
            .setNeutralButton("复制攻略") { _, _ ->
                copyGuideToClipboard()
            }
            .create()
    }

    private fun buildGuideText(): String {
        return """
🎯 孙燕姿苏州站抢票攻略

⏰ 关键时间
• 开票时间：2026-03-06 14:00
• 演出日期：2026-04-10 / 04-12
• 地点：苏州奥林匹克体育中心

📱 战前准备
□ 提前登录大麦账号
□ 添加观演人信息
□ 设置默认支付方式
□ 测试指纹/面容支付
□ 清理手机内存
□ 关闭后台应用
□ 连接稳定 WiFi 或 5G

🎫 抢票流程
1. 开售前 10 分钟：打开倒计时
2. 开售前 1 分钟：停止刷新
3. 开售前 10 秒：手指悬停按钮
4. 开售瞬间：立即购买→选价位→选张数→提交
5. 提交后：立即支付（不要犹豫）

💡 关键技巧
• 680 元价位性价比最高
• 建议抢 2 张（成功率更高）
• 如果失败，15 分钟内持续刷新
• 回流票在 5/10/15 分钟时出现
• 多平台同时抢（大麦 + 猫眼）

⚠️ 注意事项
• 不要频繁刷新（可能被封）
• 不要相信代抢（99% 骗子）
• 订单 15 分钟后释放
• 保持好心态

🍀 祝你好运！
        """.trimIndent()
    }

    private fun copyGuideToClipboard() {
        val clipboard = requireContext().getSystemService(android.content.ClipboardManager::class.java)
        val clip = android.content.ClipData.newPlainText("抢票攻略", buildGuideText())
        clipboard.setPrimaryClip(clip)
        android.widget.Toast.makeText(requireContext(), "攻略已复制", android.widget.Toast.LENGTH_SHORT).show()
    }
}
