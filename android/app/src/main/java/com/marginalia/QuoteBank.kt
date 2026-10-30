package com.marginalia

import android.content.Context
import org.json.JSONArray
import java.io.File
import java.time.LocalDate

data class HorizonInfo(val code: String, val title: String, val keywords: Set<String>)

object Horizons {
    val ALL = listOf(
        HorizonInfo("all", "All", emptySet()),
        HorizonInfo("craft", "✨ How-To", setOf("how-to", "craft", "daily", "prose-craft")),
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
            if (h.code == "all" || h.code == "craft" || h.code == "prose") continue
            if (tagSet.any { h.keywords.contains(it) }) return h.code
        }
        for (h in ALL) {
            if (h.code == "all" || h.code == "craft" || h.code == "prose") continue
            if (h.keywords.any { text.contains(it) }) return h.code
        }
        return "prose"
    }

    fun titleFor(code: String): String =
        ALL.firstOrNull { it.code == code }?.title ?: code.replaceFirstChar { it.uppercase() }
}

data class ShelfSlide(
    val label: String,
    val pill: String,
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
    val horizon: String = Horizons.horizonFor(quote, explanation, tags),
    val isCard: Boolean = false,
    val cardJob: String? = null,
    val cardIndex: Int? = null,
    val lookCloser: String? = null,
    val stealIt: String? = null,
    val aroundIt: String? = null
)

object QuoteBank {
    @Volatile private var cache: List<BankQuote>? = null

    fun slidesFor(quote: BankQuote, maxWords: Int = 85): List<ShelfSlide> {
        val slides = mutableListOf<ShelfSlide>()
        slides.add(ShelfSlide(label = "The Line", pill = "THE LINE", text = quote.quote, isLine = true))

        val paragraphs = quote.explanation.split("\n\n").map { it.trim() }.filter { it.isNotEmpty() }
        paragraphs.forEachIndexed { pIdx, paragraph ->
            val (baseLabel, basePill) = when (pIdx) {
                0 -> "The Predicament" to "THE PREDICAMENT"
                1 -> "The Mirror" to "THE MIRROR"
                else -> "The Insight" to "THE INSIGHT"
            }
            val words = paragraph.split(Regex("\\s+"))
            if (words.size <= maxWords) {
                slides.add(ShelfSlide(label = baseLabel, pill = basePill, text = paragraph, isLine = false))
            } else {
                val sentences = paragraph.split(Regex("(?<=[.!?])\\s+"))
                val chunks = mutableListOf<String>()
                var currentChunk = StringBuilder()
                var currentWordCount = 0

                for (sentence in sentences) {
                    val sWords = sentence.split(Regex("\\s+")).size
                    if (currentWordCount + sWords > maxWords && currentChunk.isNotEmpty()) {
                        chunks.add(currentChunk.toString().trim())
                        currentChunk = StringBuilder(sentence)
                        currentWordCount = sWords
                    } else {
                        if (currentChunk.isNotEmpty()) currentChunk.append(" ")
                        currentChunk.append(sentence)
                        currentWordCount += sWords
                    }
                }
                if (currentChunk.isNotEmpty()) {
                    chunks.add(currentChunk.toString().trim())
                }

                chunks.forEachIndexed { cIdx, chunk ->
                    val chunkLabel = if (chunks.size > 1) "$baseLabel (${cIdx + 1}/${chunks.size})" else baseLabel
                    val chunkPill = if (chunks.size > 1) "$basePill (${cIdx + 1}/${chunks.size})" else basePill
                    slides.add(ShelfSlide(label = chunkLabel, pill = chunkPill, text = chunk, isLine = false))
                }
            }
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
        val assetQuotes = runCatching {
            parse(context.assets.open("quote-bank.json").bufferedReader().use { it.readText() })
        }.getOrNull() ?: emptyList()

        val file = cacheFile(context)
        if (!file.exists()) return assetQuotes

        val cachedQuotes = runCatching { parse(file.readText()) }.getOrNull()
        if (cachedQuotes == null || cachedQuotes.isEmpty()) return assetQuotes

        val assetExpChars = assetQuotes.sumOf { it.explanation.length.toLong() }
        val cachedExpChars = cachedQuotes.sumOf { it.explanation.length.toLong() }

        return if (assetExpChars >= cachedExpChars && assetQuotes.isNotEmpty()) {
            runCatching { file.delete() }
            assetQuotes
        } else {
            cachedQuotes
        }
    }

    /**
     * Today's shelf quote, rotating every day deterministically through the entire library.
     * If you left the app on a different quote, that quote becomes today's and subsequent days carry on from it.
     */
    fun todayIndex(context: Context): Int {
        val quotes = all(context)
        if (quotes.isEmpty()) return 0
        val today = LocalDate.now().toEpochDay()
        val start = Prefs.startShelf(context)?.let { (idx, day) ->
            idx.toLong() - day
        } ?: 0L
        return Math.floorMod(start + today, quotes.size.toLong()).toInt()
    }

    /** Makes [index] today's shelf quote, so the widget and app show it now and advance each day. */
    fun startFrom(context: Context, index: Int) {
        val quotes = all(context)
        if (quotes.isNotEmpty()) {
            val safeIndex = index.coerceIn(0, quotes.lastIndex)
            Prefs.setStartShelf(context, safeIndex, LocalDate.now().toEpochDay())
        }
    }
}
