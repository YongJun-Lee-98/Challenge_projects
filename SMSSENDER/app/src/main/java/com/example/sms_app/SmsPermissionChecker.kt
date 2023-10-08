package com.example.sms_app

import android.Manifest
import android.app.Activity
import android.content.pm.PackageManager
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class SmsPermissionChecker(private val activity: Activity) {
    private val smsPermissionCode = 123
    var permissionResultListener: ((Boolean) -> Unit)? = null

    fun checkSmsPermission(): Boolean {
        val permissionStatus = ContextCompat.checkSelfPermission(activity, Manifest.permission.SEND_SMS)
        return if (permissionStatus != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(activity, arrayOf(Manifest.permission.SEND_SMS), smsPermissionCode)
            false
        } else {
            true
        }
    }

    fun onRequestPermissionsResult(requestCode: Int, grantResults: IntArray) {
        if (requestCode == smsPermissionCode) {
            val granted = grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED
            permissionResultListener?.invoke(granted)
        }
    }
}
