package com.damai.assistant

import android.Manifest
import android.app.AlertDialog
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import com.damai.assistant.databinding.ActivityMainBinding
import com.damai.assistant.service.TicketGrabService
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private var isServiceRunning = false

    companion object {
        const val NOTIFICATION_PERMISSION_CODE = 1001
        const val CONFIG_KEY_SALE_TIME = "sale_time"
        const val CONFIG_KEY_PRICE_LEVEL = "price_level"
        const val CONFIG_KEY_TICKET_COUNT = "ticket_count"
        const val CONFIG_KEY_ATTENDEE_INFO = "attendee_info"
        
        // 孙燕姿苏州站默认配置
        const val DEFAULT_SALE_TIME = "2026-03-06 14:00:00"
        const val DEFAULT_PRICE_LEVEL = "680"
        const val DEFAULT_TICKET_COUNT = "2"
        
        // 默认观演人信息
        val DEFAULT_ATTENDEES = listOf(
            AttendeeInfo("孔令征", "320104198504011216"),
            AttendeeInfo("叶波", "320105198701191427")
        )
        
        data class AttendeeInfo(val name: String, val idCard: String)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupUI()
        checkPermissions()
        loadConfig()
    }

    private fun setupUI() {
        // 开始抢票按钮
        binding.btnStartGrab.setOnClickListener {
            if (isServiceRunning) {
                stopGrabService()
            } else {
                startGrabService()
            }
        }

        // 配置按钮
        binding.btnConfig.setOnClickListener {
            showConfigDialog()
        }

        // 攻略按钮
        binding.btnGuide.setOnClickListener {
            showGuide()
        }

        // 测试通知
        binding.btnTestNotification.setOnClickListener {
            testNotification()
        }
    }

    private fun checkPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(
                    this,
                    Manifest.permission.POST_NOTIFICATIONS
                ) != PackageManager.PERMISSION_GRANTED
            ) {
                ActivityCompat.requestPermissions(
                    this,
                    arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                    NOTIFICATION_PERMISSION_CODE
                )
            }
        }
    }

    private fun loadConfig() {
        val prefs = getSharedPreferences("damai_config", MODE_PRIVATE)
        val saleTime = prefs.getString(CONFIG_KEY_SALE_TIME, DEFAULT_SALE_TIME) ?: DEFAULT_SALE_TIME
        val priceLevel = prefs.getString(CONFIG_KEY_PRICE_LEVEL, DEFAULT_PRICE_LEVEL) ?: DEFAULT_PRICE_LEVEL
        val ticketCount = prefs.getString(CONFIG_KEY_TICKET_COUNT, DEFAULT_TICKET_COUNT) ?: DEFAULT_TICKET_COUNT

        binding.tvSaleTime.text = "开票时间：$saleTime"
        binding.tvPriceLevel.text = "目标价位：¥$priceLevel"
        binding.tvTicketCount.text = "张数：$ticketCount 张"
    }

    private fun startGrabService() {
        // 检查无障碍权限
        if (!isAccessibilityServiceEnabled()) {
            showAccessibilityEnableDialog()
            return
        }
        
        val intent = Intent(this, TicketGrabService::class.java)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
        
        isServiceRunning = true
        updateUIState()
        Toast.makeText(this, "抢票服务已启动", Toast.LENGTH_SHORT).show()
    }

    private fun stopGrabService() {
        val intent = Intent(this, TicketGrabService::class.java)
        stopService(intent)
        
        isServiceRunning = false
        updateUIState()
        Toast.makeText(this, "抢票服务已停止", Toast.LENGTH_SHORT).show()
    }

    private fun updateUIState() {
        if (isServiceRunning) {
            binding.btnStartGrab.text = "停止抢票"
            binding.btnStartGrab.setBackgroundResource(R.drawable.btn_stop_background)
            binding.tvStatus.text = "状态：运行中"
            binding.tvStatus.setTextColor(ContextCompat.getColor(this, R.color.success))
        } else {
            binding.btnStartGrab.text = "开始抢票"
            binding.btnStartGrab.setBackgroundResource(R.drawable.btn_start_background)
            binding.tvStatus.text = "状态：未启动"
            binding.tvStatus.setTextColor(ContextCompat.getColor(this, R.color.warning))
        }
    }

    private fun showConfigDialog() {
        val configDialog = ConfigDialogFragment()
        configDialog.show(supportFragmentManager, "ConfigDialog")
    }

    private fun showGuide() {
        val guideDialog = GuideDialogFragment()
        guideDialog.show(supportFragmentManager, "GuideDialog")
    }

    private fun testNotification() {
        val intent = Intent(this, TicketGrabService::class.java)
        intent.action = TicketGrabService.ACTION_TEST_NOTIFICATION
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
        Toast.makeText(this, "测试通知已发送", Toast.LENGTH_SHORT).show()
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == NOTIFICATION_PERMISSION_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "通知权限已授予", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "需要通知权限才能发送提醒", Toast.LENGTH_LONG).show()
            }
        }
    }

    override fun onResume() {
        super.onResume()
        // 检查服务状态
        checkServiceStatus()
    }

    private fun checkServiceStatus() {
        // 简单实现，实际应该检查服务是否真的在运行
        updateUIState()
    }

    private fun isAccessibilityServiceEnabled(): Boolean {
        val serviceName = "$packageName/.service.AccessibilityService"
        val enabledServices = android.provider.Settings.Secure.getString(
            contentResolver,
            android.provider.Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES
        ) ?: ""
        
        return enabledServices.contains(serviceName)
    }

    private fun showAccessibilityEnableDialog() {
        AlertDialog.Builder(this)
            .setTitle("需要开启无障碍权限")
            .setMessage("抢票功能需要无障碍权限来自动点击按钮。\n\n请在设置中找到「大麦抢票助手」并开启权限。")
            .setPositiveButton("去设置") { _, _ ->
                val intent = android.content.Intent(android.provider.Settings.ACTION_ACCESSIBILITY_SETTINGS)
                startActivity(intent)
            }
            .setNegativeButton("取消", null)
            .show()
    }
}
