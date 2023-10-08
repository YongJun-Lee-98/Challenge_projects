package com.example.sms_app.ui.theme

import androidx.compose.material.MaterialTheme
import androidx.compose.material.Surface
import androidx.compose.material.darkColors
import androidx.compose.material.lightColors
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val LightThemeColors = lightColors(
    primary = Color(0xFF3F51B5), // Indigo
    primaryVariant = Color(0xFFFF00),// Your primary variant color,
    secondary = Color(0xFFFFFF)// Your secondary color
)

private val DarkThemeColors = darkColors(
    primary = Color(0xFF3F51B5), // Indigo
    primaryVariant = Color(0xFFFF00),// Your primary variant color,
    secondary = Color(0x000000)// Your secondary color
)

@Composable
fun SmsAppTheme(darkTheme: Boolean = false, content: @Composable () -> Unit) {
    val colors = if (darkTheme) {
        DarkThemeColors
    } else {
        LightThemeColors
    }

    MaterialTheme(
        colors = colors,
        content = content
    )
}

