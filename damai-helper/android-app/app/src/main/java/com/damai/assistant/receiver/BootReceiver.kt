package com.damai.assistant.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Build
import android.util.Log
import com.damai.assistant.service.TicketGrabService

/**
 * 开机启动广播接收器
 * 设备启动后自动启动抢票服务（如果之前是运行状态）
 */
class BootReceiver : BroadcastReceiver() {
    
    companion object {
        const val TAG = "BootReceiver"
        const val PREF_SERVICE_RUNNING = "service_running"
    }
    
    override fun onReceive(context: Context?, intent: Intent?) {
        if (intent?.action == Intent.ACTION_BOOT_COMPLETED || 
            intent?.action == "android.intent.action.QUICKBOOT_POWERON") {
            
            Log.d(TAG, "Boot completed, checking service state")
            
            context?.let {
                val prefs = it.getSharedPreferences("damai_service_state", Context.MODE_PRIVATE)
                val wasRunning = prefs.getBoolean(PREF_SERVICE_RUNNING, false)
                
                if (wasRunning) {
                    Log.d(TAG, "Service was running, restarting...")
                    val serviceIntent = Intent(it, TicketGrabService::class.java)
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                        it.startForegroundService(serviceIntent)
                    } else {
                        it.startService(serviceIntent)
                    }
                }
            }
        }
    }
}
