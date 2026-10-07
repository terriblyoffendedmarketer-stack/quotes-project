package com.marginalia

import android.content.Context
import com.marginalia.widget.CardWidgetProvider
import java.net.HttpURLConnection
import java.net.URL
import kotlin.concurrent.thread

/**
 * Keeps the cards up to date without reinstalling the app. It downloads cards.json from the
 * project's GitHub repository at most every few hours, checks that it parses, and swaps it in.
 * If anything goes wrong it keeps whatever it already had.
 */
object ContentSync {
    const val CARDS_URL =
        "https://raw.githubusercontent.com/terriblyoffendedmarketer-stack/quotes-project/main/content/cards.json"

    private const val PREFS = "content_sync"
    private const val LAST_CHECK = "last_check"
    private const val MIN_INTERVAL_MS = 3 * 60 * 60 * 1000L

    /** Starts a background check if one is due. [done] runs on the background thread afterwards. */
    fun syncIfDue(context: Context, force: Boolean = false, done: (() -> Unit)? = null) {
        val app = context.applicationContext
        val prefs = app.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        val now = System.currentTimeMillis()
        if (!force && now - prefs.getLong(LAST_CHECK, 0) < MIN_INTERVAL_MS) {
            done?.invoke()
            return
        }
        prefs.edit().putLong(LAST_CHECK, now).apply()
        thread(name = "card-sync") {
            try {
                val text = download()
                if (text != null) {
                    Cards.parse(text)
                    val file = Cards.cacheFile(app)
                    if (!file.exists() || file.readText() != text) {
                        val tmp = java.io.File(file.path + ".tmp")
                        tmp.writeText(text)
                        tmp.renameTo(file)
                        Cards.invalidate()
                        CardWidgetProvider.refreshAll(app)
                    }
                }
            } catch (_: Exception) {
                // Offline or a bad file: keep the cards we already have.
            } finally {
                done?.invoke()
            }
        }
    }

    private fun download(): String? {
        val connection = URL(CARDS_URL).openConnection() as HttpURLConnection
        return try {
            connection.connectTimeout = 8000
            connection.readTimeout = 8000
            connection.useCaches = false
            if (connection.responseCode != 200) null
            else connection.inputStream.bufferedReader().use { it.readText() }
        } finally {
            connection.disconnect()
        }
    }
}
