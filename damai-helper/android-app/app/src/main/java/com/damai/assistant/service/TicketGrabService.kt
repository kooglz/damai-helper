package com.damai.assistant.service

import android.app.*
import android.content.Intent
import android.os.Build
import android.os.CountDownTimer
import android.os.IBinder
import android.util.Log
import androidx.core.app.NotificationCompat
import com.damai.assistant.MainActivity
import com.damai.assistant.R
import java.text.SimpleDateFormat
import java.util.*

class TicketGrabService : Service() {

    companion object {
        const val TAG = "TicketGrabService"
        const val CHANNEL_ID = "ticket_grab_channel"
        const val NOTIFICATION_ID = 1001
        const val ACTION_TEST_NOTIFICATION = "com.damai.assistant.TEST_NOTIFICATION"
        const val ACTION_STOP_SERVICE = "com.damai.assistant.STOP_SERVICE"
        const val ACTION_UPDATE_COUNTDOWN = "com.damai.assistant.UPDATE_COUNTDOWN"
    }

    private var countdownTimer: CountDownTimer? = null
    private var saleTimeMillis: Long = 0
    private var isCountingDown = false

    override fun onCreate() {
        super.onCreate()
        Log.d(TAG, "Service created")
        createNotificationChannel()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        Log.d(TAG, "Service started with action: ${intent?.action}")

        when (intent?.action) {
            ACTION_TEST_NOTIFICATION -> {
                showTestNotification()
                return START_NOT_STICKY
            }
            ACTION_STOP_SERVICE -> {
                stopSelf()
                return START_NOT_STICKY
            }
        }

        // 获取配置
        val prefs = getSharedPreferences("damai_config", MODE_PRIVATE)
        val saleTimeStr = prefs.getString(
            MainActivity.CONFIG_KEY_SALE_TIME,
            MainActivity.DEFAULT_SALE_TIME
        ) ?: MainActivity.DEFAULT_SALE_TIME

        // 解析开票时间
        saleTimeMillis = parseTime(saleTimeStr)
        Log.d(TAG, "Sale time: $saleTimeStr -> $saleTimeMillis")

        // 启动前台服务
        startForeground(NOTIFICATION_ID, createNotification("准备中..."))

        // 开始倒计时
        startCountdown()

        return START_STICKY
    }

    private fun parseTime(timeStr: String): Long {
        return try {
            val formats = listOf(
                SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.CHINA),
                SimpleDateFormat("yyyy/MM/dd HH:mm:ss", Locale.CHINA),
                SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.CHINA)
            )
            
            for (format in formats) {
                try {
                    return format.parse(timeStr)?.time ?: 0
                } catch (e: Exception) {
                    continue
                }
            }
            System.currentTimeMillis() + 3600000 // 默认 1 小时后
        } catch (e: Exception) {
            Log.e(TAG, "Parse time error", e)
            System.currentTimeMillis() + 3600000
        }
    }

    private fun startCountdown() {
        countdownTimer?.cancel()

        val millisUntilFinished = saleTimeMillis - System.currentTimeMillis()
        Log.d(TAG, "Millis until sale: $millisUntilFinished")

        if (millisUntilFinished <= 0) {
            // 已经开售
            updateNotification("演出已开售！立即抢票！", true)
            return
        }

        isCountingDown = true
        countdownTimer = object : CountDownTimer(millisUntilFinished, 1000) {
            override fun onTick(millisUntilFinished: Long) {
                val hours = millisUntilFinished / 3600000
                val minutes = (millisUntilFinished % 3600000) / 60000
                val seconds = (millisUntilFinished % 60000) / 1000

                val tickText = String.format("%02d:%02d:%02d", hours, minutes, seconds)
                updateNotification("距离开售：$tickText", false)

                // 关键时间点提醒
                checkImportantTimePoints(millisUntilFinished)
            }

            override fun onFinish() {
                isCountingDown = false
                updateNotification("🔥 开售了！立即抢票！", true)
                playAlarm()
            }
        }.start()

        Log.d(TAG, "Countdown started")
    }

    private fun checkImportantTimePoints(millisUntilFinished: Long) {
        val minutesUntil = millisUntilFinished / 60000
        
        when (minutesUntil) {
            60L -> sendTimePointNotification("距离开售还有 1 小时")
            30L -> sendTimePointNotification("距离开售还有 30 分钟")
            15L -> sendTimePointNotification("距离开售还有 15 分钟")
            10L -> sendTimePointNotification("距离开售还有 10 分钟")
            5L -> sendTimePointNotification("距离开售还有 5 分钟")
            3L -> sendTimePointNotification("距离开售还有 3 分钟")
            1L -> sendTimePointNotification("距离开售还有 1 分钟！准备！")
            0L -> sendTimePointNotification("最后 30 秒！准备好！")
        }
    }

    private fun sendTimePointNotification(message: String) {
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle("⏰ 抢票提醒")
            .setContentText(message)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setCategory(NotificationCompat.CATEGORY_REMINDER)
            .setAutoCancel(true)
            .build()

        val notificationManager = getSystemService(NotificationManager::class.java)
        notificationManager.notify(System.currentTimeMillis().toInt(), notification)
    }

    private fun createNotification(contentText: String): Notification {
        val pendingIntent = PendingIntent.getActivity(
            this,
            0,
            Intent(this, MainActivity::class.java),
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )

        val stopIntent = Intent(this, TicketGrabService::class.java).apply {
            action = ACTION_STOP_SERVICE
        }
        val stopPendingIntent = PendingIntent.getService(
            this,
            1,
            stopIntent,
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )

        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle("🎫 大麦抢票助手")
            .setContentText(contentText)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setCategory(NotificationCompat.CATEGORY_SERVICE)
            .setContentIntent(pendingIntent)
            .addAction(R.drawable.ic_stop, "停止", stopPendingIntent)
            .setOngoing(true)
            .build()
    }

    private fun updateNotification(contentText: String, isUrgent: Boolean) {
        val notification = createNotification(contentText).apply {
            if (isUrgent) {
                priority = NotificationCompat.PRIORITY_MAX
                category = NotificationCompat.CATEGORY_ALARM
            }
        }

        val notificationManager = getSystemService(NotificationManager::class.java)
        notificationManager.notify(NOTIFICATION_ID, notification)
    }

    private fun showTestNotification() {
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle("🎫 抢票助手测试")
            .setContentText("通知功能正常！抢票时会收到此类提醒。")
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .build()

        val notificationManager = getSystemService(NotificationManager::class.java)
        notificationManager.notify(System.currentTimeMillis().toInt(), notification)
    }

    private fun playAlarm() {
        // 播放提示音
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle("🔥🔥🔥 开抢了！")
            .setContentText("立即打开大麦 APP 抢票！")
            .setPriority(NotificationCompat.PRIORITY_MAX)
            .setCategory(NotificationCompat.CATEGORY_ALARM)
            .setAutoCancel(true)
            .setVibrate(longArrayOf(0, 500, 200, 500, 200, 500))
            .build()

        val notificationManager = getSystemService(NotificationManager::class.java)
        notificationManager.notify(NOTIFICATION_ID + 1, notification)
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "抢票服务",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "用于抢票倒计时和提醒"
                enableVibration(true)
                vibrationPattern = longArrayOf(0, 500, 200, 500)
            }

            val notificationManager = getSystemService(NotificationManager::class.java)
            notificationManager.createNotificationChannel(channel)
        }
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, "Service destroyed")
        countdownTimer?.cancel()
        countdownTimer = null
    }
}
