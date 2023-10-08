package com.example.sms_app
import com.google.gson.annotations.SerializedName

data class Message(
    val id: Int,
    val message: String,
    @SerializedName("phone_number") val phoneNumber: String,
    val user: String
)



