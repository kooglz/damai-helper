package com.damai.assistant.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log
import com.damai.assistant.service.TicketGrabService

/**
 * 倒计时广播接收器
 * 用于接收系统时间变化广播，更新倒计时
 */
class CountdownReceiver : BroadcastReceiver() {
    
    companion object {
        const val TAG = "CountdownReceiver"
    }
    
    override fun onReceive(context: Context?, intent: Intent?) {
        Log.d(TAG, "Received broadcast: ${intent?.action}")
        
        // 可以发送广播通知服务更新时间
        context?.let {
            val updateIntent = Intent(it, TicketGrabService::class.java).apply {
                action = TicketGrabService.ACTION_UPDATE_COUNTDOWN
            }
            it.startService(updateIntent)
        }
    }
}
