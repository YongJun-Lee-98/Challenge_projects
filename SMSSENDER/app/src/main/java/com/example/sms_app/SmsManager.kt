package com.example.sms_app
import android.telephony.SmsManager

object SmsManager {
    fun sendSms(phoneNumber: String, message: String) {
        val smsManager = SmsManager.getDefault()
        smsManager.sendTextMessage(phoneNumber, null, message, null, null)
    }
}

