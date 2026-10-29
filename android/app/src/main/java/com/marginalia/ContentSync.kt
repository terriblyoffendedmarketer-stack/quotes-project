package com.marginalia

import android.content.Context
import com.marginalia.widget.CardWidgetProvider
import java.net.HttpURLConnection
import java.net.URL
import kotlin.concurrent.thread

/**
 * Keeps cards and quote bank up to date without reinstalling the app. It downloads from the
 * project's GitHub repository at most every few hours, validates JSON, and updates cache files.
 */
object ContentSync {
    const val CARDS_URL =
        "https://raw.githubusercontent.com/terriblyoffendedmarketer-stack/quotes-project/main/content/cards.json"
    const val QUOTE_BANK_URL =
        "https://raw.githubusercontent.com/terriblyoffendedmarketer-stack/quotes-project/main/content/quote-bank.json"

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
        thread(name = "content-sync") {
            try {
                var changed = false
                
                // 1. Sync Cards
                val cardsText = download(CARDS_URL)
                if (cardsText != null) {
                    Cards.parse(cardsText)
                    val file = Cards.cacheFile(app)
                    if (!file.exists() || file.readText() != cardsText) {
                        val tmp = java.io.File(file.path + ".tmp")
                        tmp.writeText(cardsText)
                        tmp.renameTo(file)
                        Cards.invalidate()
                        changed = true
                    }
                }

                // 2. Sync Quote Bank
                val bankText = download(QUOTE_BANK_URL)
                if (bankText != null) {
                    QuoteBank.parse(bankText)
                    val bFile = QuoteBank.cacheFile(app)
                    if (!bFile.exists() || bFile.readText() != bankText) {
                        val tmp = java.io.File(bFile.path + ".tmp")
                        tmp.writeText(bankText)
                        tmp.renameTo(bFile)
                        QuoteBank.invalidate()
                        changed = true
                    }
                }

                if (changed) {
                    CardWidgetProvider.refreshAll(app)
                }
            } catch (_: Exception) {
                // Offline or bad file: keep existing files
            } finally {
                done?.invoke()
            }
        }
    }

    private fun download(urlStr: String): String? {
        val connection = URL(urlStr).openConnection() as HttpURLConnection
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
