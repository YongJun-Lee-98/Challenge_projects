package com.example.sms_app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Surface
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.sms_app.ui.theme.SmsAppTheme


class MainActivity : ComponentActivity() {
    private lateinit var smsPermissionChecker: SmsPermissionChecker

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        smsPermissionChecker = SmsPermissionChecker(this)
        smsPermissionChecker.checkSmsPermission()

        setContent {
            SmsAppTheme {
                Surface(color = MaterialTheme.colors.background) {
                    val smsSendingViewModel: SmsSendingViewModel = viewModel()
                    val smsPermissionGranted = remember { mutableStateOf(smsPermissionChecker.checkSmsPermission()) }

                    smsPermissionChecker.permissionResultListener = { granted ->
                        smsPermissionGranted.value = granted
                    }
                    smsSendingViewModel.sendAllMessages()

                    if (smsPermissionGranted.value) {
                        SmsSendingScreen(onSendAllMessagesClick = {
                            smsSendingViewModel.sendAllMessages()
                        })
                        // 앱 시작시 자동으로 메시지 전송 시작
                    }

                }
            }
        }
    }

}
