package com.legalai.desk

import android.annotation.SuppressLint
import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.net.URLEncoder
import java.util.concurrent.Executors

class MainActivity : AppCompatActivity() {
    private lateinit var webView: WebView
    private val io = Executors.newSingleThreadExecutor()

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        webView = WebView(this)
        setContentView(webView)
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.webChromeClient = WebChromeClient()
        webView.webViewClient = WebViewClient()
        webView.addJavascriptInterface(NativeBridge(), "LegalAINative")
        webView.loadUrl("file:///android_asset/www/index.html")
    }

    override fun onDestroy() {
        io.shutdownNow()
        super.onDestroy()
    }

    inner class NativeBridge {
        @JavascriptInterface
        fun isNative(): Boolean = true

        @JavascriptInterface
        fun dial(phone: String) {
            runOnUiThread {
                val uri = Uri.parse("tel:${phone.filter { it.isDigit() || it == '+' }}")
                try {
                    startActivity(Intent(Intent.ACTION_DIAL, uri))
                } catch (ex: ActivityNotFoundException) {
                    toast("No Phone app found")
                }
            }
        }

        @JavascriptInterface
        fun whatsapp(phone: String, message: String) {
            runOnUiThread {
                val digits = phone.filter { it.isDigit() }
                val e164 = if (digits.length == 10) "91$digits" else digits
                val url = "https://wa.me/$e164?text=" + URLEncoder.encode(message, "UTF-8")
                try {
                    startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
                } catch (ex: ActivityNotFoundException) {
                    toast("Install WhatsApp from Play Store")
                    startActivity(
                        Intent(
                            Intent.ACTION_VIEW,
                            Uri.parse("https://play.google.com/store/apps/details?id=com.whatsapp"),
                        ),
                    )
                }
            }
        }

        @JavascriptInterface
        fun openTeleCrmApp() {
            runOnUiThread {
                val launch = packageManager.getLaunchIntentForPackage("app.telecrm.in")
                    ?: packageManager.getLaunchIntentForPackage("app.telecrm.enterprise3.in")
                if (launch != null) {
                    startActivity(launch)
                } else {
                    startActivity(
                        Intent(
                            Intent.ACTION_VIEW,
                            Uri.parse("https://play.google.com/store/apps/details?id=app.telecrm.in"),
                        ),
                    )
                }
            }
        }

        @JavascriptInterface
        fun saveTeleCrmSettings(pushUrl: String, pullUrl: String, token: String) {
            prefs().edit()
                .putString("pushUrl", pushUrl.trim())
                .putString("pullUrl", pullUrl.trim())
                .putString("token", token.trim())
                .apply()
            toast("TeleCRM settings saved on this phone")
        }

        @JavascriptInterface
        fun loadTeleCrmSettings(): String {
            val json = JSONObject()
            json.put("pushUrl", prefs().getString("pushUrl", "") ?: "")
            json.put("pullUrl", prefs().getString("pullUrl", "") ?: "")
            json.put("hasToken", !prefs().getString("token", "").isNullOrBlank())
            return json.toString()
        }

        @JavascriptInterface
        fun pullLeadsFromTeleCrm() {
            val pullUrl = prefs().getString("pullUrl", "") ?: ""
            val token = prefs().getString("token", "") ?: ""
            if (pullUrl.isBlank() || token.isBlank()) {
                toast("Paste TeleCRM Sync/search URL and token in TeleCRM setup")
                return
            }
            io.execute {
                try {
                    val conn = URL(pullUrl).openConnection() as HttpURLConnection
                    conn.requestMethod = "GET"
                    conn.setRequestProperty("Authorization", "Bearer $token")
                    conn.setRequestProperty("Accept", "application/json")
                    val text = (if (conn.responseCode in 200..299) conn.inputStream else conn.errorStream)
                        .bufferedReader().readText()
                    runOnUiThread {
                        if (conn.responseCode in 200..299) {
                            val escaped = JSONObject.quote(text)
                            webView.evaluateJavascript("window.onTeleCrmLeads && onTeleCrmLeads($escaped)", null)
                        } else {
                            toast("TeleCRM pull error ${conn.responseCode}")
                        }
                    }
                } catch (ex: Exception) {
                    runOnUiThread { toast("TeleCRM pull: ${ex.message}") }
                }
            }
        }

        @JavascriptInterface
        fun pushLeadToTeleCrm(leadJson: String) {
            val pushUrl = prefs().getString("pushUrl", "") ?: ""
            val token = prefs().getString("token", "") ?: ""
            if (pushUrl.isBlank() || token.isBlank()) {
                toast("Open TeleCRM setup and paste your API URL and token")
                return
            }
            io.execute {
                try {
                    val lead = JSONObject(leadJson)
                    val fields = JSONObject()
                    fields.put("Name", lead.optString("name"))
                    fields.put("Phone", lead.optString("phone"))
                    fields.put("Status", lead.optString("call_status"))
                    fields.put("Interested", lead.optString("interested"))
                    fields.put("Remaining amount", lead.optString("remaining_amount"))
                    fields.put("Settlement offered", lead.optString("settlement_amount"))
                    fields.put("Legal fee", lead.optString("legal_fee"))
                    fields.put("Notes", lead.optString("notes"))
                    val body = JSONObject()
                    body.put("fields", fields)
                    val conn = URL(pushUrl).openConnection() as HttpURLConnection
                    conn.requestMethod = "POST"
                    conn.setRequestProperty("Authorization", "Bearer $token")
                    conn.setRequestProperty("Content-Type", "application/json")
                    conn.doOutput = true
                    conn.outputStream.use { it.write(body.toString().toByteArray(Charsets.UTF_8)) }
                    val code = conn.responseCode
                    runOnUiThread {
                        if (code in 200..299) toast("TeleCRM updated")
                        else toast("TeleCRM error $code — check URL and token")
                    }
                } catch (ex: Exception) {
                    runOnUiThread { toast("TeleCRM: ${ex.message}") }
                }
            }
        }

        private fun prefs() = getSharedPreferences("legalai", Context.MODE_PRIVATE)

        private fun toast(message: String) {
            runOnUiThread { Toast.makeText(this@MainActivity, message, Toast.LENGTH_LONG).show() }
        }
    }
}
