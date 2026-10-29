package com.marginalia

import android.content.Context
import org.json.JSONArray
import java.io.File
import java.time.LocalDate

data class BankQuote(
    val quote: String,
    val author: String,
    val work: String,
    val year: Int?,
    val explanation: String,
    val tags: List<String>
)

object QuoteBank {
    @Volatile private var cache: List<BankQuote>? = null

    fun all(context: Context): List<BankQuote> =
        cache ?: synchronized(this) { cache ?: load(context).also { cache = it } }

    fun cacheFile(context: Context) = File(context.filesDir, "quote-bank.json")

    fun invalidate() = synchronized(this) { cache = null }

    fun parse(text: String): List<BankQuote> {
        val array = JSONArray(text)
        val quotes = ArrayList<BankQuote>(array.length())
        for (i in 0 until array.length()) {
            val o = array.getJSONObject(i)
            val quote = o.optString("quote", "").trim()
            if (quote.isEmpty()) continue
            val author = o.optString("author", "Unknown").trim()
            val work = o.optString("work", "Unknown").trim()
            val year = if (o.has("year") && !o.isNull("year")) o.optInt("year") else null
            val explanation = o.optString("explanation", "").trim()
            val tagsArray = o.optJSONArray("tags")
            val tags = if (tagsArray != null) {
                List(tagsArray.length()) { tagsArray.getString(it) }
            } else emptyList()

            quotes.add(BankQuote(
                quote = quote,
                author = author,
                work = work,
                year = year,
                explanation = explanation,
                tags = tags
            ))
        }
        require(quotes.isNotEmpty())
        return quotes
    }

    private fun load(context: Context): List<BankQuote> {
        val file = cacheFile(context)
        if (file.exists()) {
            runCatching { return parse(file.readText()) }
        }
        return runCatching {
            parse(context.assets.open("quote-bank.json").bufferedReader().use { it.readText() })
        }.getOrElse { emptyList() }
    }

    /**
     * Today's shelf quote, rotating every day deterministically through the entire library.
     */
    fun todayIndex(context: Context): Int {
        val quotes = all(context)
        if (quotes.isEmpty()) return 0
        val today = LocalDate.now().toEpochDay()
        return Math.floorMod(today, quotes.size.toLong()).toInt()
    }
}
