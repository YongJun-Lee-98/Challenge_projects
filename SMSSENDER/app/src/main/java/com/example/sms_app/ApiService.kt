package com.example.sms_app

import com.github.kittinunf.fuel.Fuel
import com.github.kittinunf.fuel.core.Response
import com.github.kittinunf.result.Result
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import android.util.Log
import org.json.JSONObject



class ApiService {
    suspend fun fetchDataFromApi(): List<Message> {
        Log.d("api service", "fetchDataFromApi front called")
        val (_, _, result) = Fuel.get("your api address/get_messages")
            .responseString()


        return when (result) {
            is Result.Success -> {
                val jsonObject = JSONObject(result.value)
                val messagesJsonArray = jsonObject.getJSONArray("messages")
                val gson = Gson()
                val type = object : TypeToken<List<Message>>() {}.type
                val messages = gson.fromJson<List<Message>>(messagesJsonArray.toString(), type)
                // Log the received messages
                Log.d("ApiService", "Received messages: $messages")

                messages
            }
            is Result.Failure -> {
                Log.d("api service", "fetchDataFromApi failed with: ${result.error}")
                emptyList()
            }
        }
    }
    suspend fun deleteItemFromDatabase(id: Int): Response {
        val (_, response, _) = Fuel.delete("your api address//delete_message/$id")
            .response()

        return response
    }

}







