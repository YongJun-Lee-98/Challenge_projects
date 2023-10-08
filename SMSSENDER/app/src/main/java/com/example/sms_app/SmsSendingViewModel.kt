package com.example.sms_app

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import android.util.Log
import android.telephony.SmsManager

class SmsSendingViewModel : ViewModel() {
    private val apiService = ApiService()

    fun sendAllMessages() {
        viewModelScope.launch(Dispatchers.IO) {
            val messages = apiService.fetchDataFromApi()
            messages.forEach { message ->
                val result = sendSms(message.phoneNumber, message.message)

                Log.d("SmsSendingViewModel", "sendAllMessages() called")
                    // Rest of the code ...

                if (result) {
                    apiService.deleteItemFromDatabase(message.id)
                }
            }
        }
    }

    private fun sendSms(phoneNumber: String, messageText: String): Boolean {
        return try {
            val smsManager = SmsManager.getDefault()
            smsManager.sendTextMessage(phoneNumber, null, messageText, null, null)
            true
        } catch (e: Exception) {
            e.printStackTrace()
            false
        }
    }
}
