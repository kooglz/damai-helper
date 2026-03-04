package com.damai.assistant

import android.app.AlertDialog
import android.app.Dialog
import android.os.Bundle
import android.view.LayoutInflater
import android.widget.EditText
import androidx.fragment.app.DialogFragment

class ConfigDialogFragment : DialogFragment() {

    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        val prefs = requireContext().getSharedPreferences("damai_config", requireContext().MODE_PRIVATE)
        
        val currentSaleTime = prefs.getString(
            MainActivity.CONFIG_KEY_SALE_TIME,
            MainActivity.DEFAULT_SALE_TIME
        ) ?: MainActivity.DEFAULT_SALE_TIME
        
        val currentPriceLevel = prefs.getString(
            MainActivity.CONFIG_KEY_PRICE_LEVEL,
            MainActivity.DEFAULT_PRICE_LEVEL
        ) ?: MainActivity.DEFAULT_PRICE_LEVEL
        
        val currentTicketCount = prefs.getString(
            MainActivity.CONFIG_KEY_TICKET_COUNT,
            MainActivity.DEFAULT_TICKET_COUNT
        ) ?: MainActivity.DEFAULT_TICKET_COUNT

        val view = LayoutInflater.from(requireContext())
            .inflate(R.layout.dialog_config, null)

        val etSaleTime = view.findViewById<EditText>(R.id.etSaleTime)
        val etPriceLevel = view.findViewById<EditText>(R.id.etPriceLevel)
        val etTicketCount = view.findViewById<EditText>(R.id.etTicketCount)

        etSaleTime.setText(currentSaleTime)
        etPriceLevel.setText(currentPriceLevel)
        etTicketCount.setText(currentTicketCount)

        return AlertDialog.Builder(requireContext())
            .setTitle("⚙️ 抢票配置")
            .setView(view)
            .setPositiveButton("保存") { _, _ ->
                with(prefs.edit()) {
                    putString(MainActivity.CONFIG_KEY_SALE_TIME, etSaleTime.text.toString())
                    putString(MainActivity.CONFIG_KEY_PRICE_LEVEL, etPriceLevel.text.toString())
                    putString(MainActivity.CONFIG_KEY_TICKET_COUNT, etTicketCount.text.toString())
                    apply()
                }
                
                // 通知 MainActivity 更新 UI
                (activity as? MainActivity)?.loadConfig()
            }
            .setNegativeButton("取消", null)
            .create()
    }
}
