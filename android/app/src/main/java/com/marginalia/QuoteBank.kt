package com.marginalia

import android.content.Context
import org.json.JSONArray
import java.io.File
import java.time.LocalDate

data class HorizonInfo(val code: String, val title: String, val keywords: Set<String>)

object Horizons {
    val ALL = listOf(
        HorizonInfo("all", "All", emptySet()),
        HorizonInfo("dread", "Atmospheric Dread", setOf("dread", "horror", "fear", "death", "dark", "eerie", "uncanny", "haunting", "tension", "macabre", "grotesque")),
        HorizonInfo("folly", "Human Folly", setOf("folly", "vanity", "satire", "hypocrisy", "manners", "social", "pretension", "awkwardness", "family", "prejudice", "pride")),
        HorizonInfo("solitude", "Solitude & Finitude", setOf("solitude", "stillness", "time", "silence", "memory", "grief", "mortality", "loss", "longing", "reflection", "quiet", "finitude", "loneliness")),
        HorizonInfo("stakes", "High Stakes", setOf("stakes", "high-stakes", "choice", "sacrifice", "survival", "courage", "crisis", "danger", "pressure", "willpower", "duty", "moral")),
        HorizonInfo("irony", "Sharp Irony", setOf("irony", "dark-humor", "humor", "wit", "cynicism", "absurdity", "paradox", "comedy", "dry", "understatement", "wry")),
        HorizonInfo("power", "Power & History", setOf("power", "history", "politics", "empire", "systems", "bureaucracy", "control", "civilization", "war", "ideology", "propaganda")),
        HorizonInfo("prose", "Prose & Voice", setOf("observation", "prose", "rhythm", "sensory-detail", "detail", "voice"))
    )

    fun horizonFor(quote: String, explanation: String, tags: List<String>): String {
        val tagSet = tags.map { it.lowercase() }.toSet()
        val text = "$quote $explanation".lowercase()
        for (h in ALL) {
            if (h.code == "all" || h.code == "prose") continue
            if (tagSet.any { h.keywords.contains(it) }) return h.code
        }
        for (h in ALL) {
            if (h.code == "all" || h.code == "prose") continue
            if (h.keywords.any { text.contains(it) }) return h.code
        }
        return "prose"
    }

    fun titleFor(code: String): String =
        ALL.firstOrNull { it.code == code }?.title ?: code.replaceFirstChar { it.uppercase() }
}

data class ShelfSlide(
    val label: String,
    val text: String,
    val isLine: Boolean
)

data class BankQuote(
    val quote: String,
    val author: String,
    val work: String,
    val year: Int?,
    val explanation: String,
    val tags: List<String>,
    val horizon: String = Horizons.horizonFor(quote, explanation, tags)
)

object QuoteBank {
    @Volatile private var cache: List<BankQuote>? = null

    fun slidesFor(quote: BankQuote): List<ShelfSlide> {
        val paragraphs = quote.explanation.split("\n\n").map { it.trim() }.filter { it.isNotEmpty() }
        val slides = mutableListOf<ShelfSlide>()
        slides.add(ShelfSlide(label = "The Line", text = quote.quote, isLine = true))
        if (paragraphs.size >= 2) {
            slides.add(ShelfSlide(label = "The Scene", text = paragraphs[0], isLine = false))
            slides.add(ShelfSlide(label = "The Truth", text = paragraphs[1], isLine = false))
            for (i in 2 until paragraphs.size) {
                slides.add(ShelfSlide(label = "Context", text = paragraphs[i], isLine = false))
            }
        } else if (paragraphs.isNotEmpty()) {
            slides.add(ShelfSlide(label = "Scene Context", text = paragraphs[0], isLine = false))
        }
        return slides
    }

    fun all(context: Context): List<BankQuote> =
        cache ?: synchronized(this) { cache ?: load(context).also { cache = it } }

    fun forHorizon(context: Context, horizonCode: String): List<BankQuote> {
        val list = all(context)
        return if (horizonCode == "all") list else list.filter { it.horizon == horizonCode }
    }

    fun countForHorizon(context: Context, horizonCode: String): Int =
        forHorizon(context, horizonCode).size

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
