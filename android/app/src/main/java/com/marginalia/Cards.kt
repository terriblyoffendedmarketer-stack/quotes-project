package com.marginalia

import android.content.Context
import org.json.JSONArray
import java.io.File
import java.time.LocalDate

data class Card(
    val id: String,
    val job: String,
    val quote: String,
    val author: String,
    val work: String,
    val year: Int,
    val translator: String?,
    val highlights: List<String>,
    val lookCloser: String,
    val aroundIt: String,
    val stealIt: String,
)

/**
 * The slides of a card, in reading order. The hook is just the job, set as large as it will go,
 * so the first thing you see is something to do. "Around it" is the optional extra at the end.
 * Each slide has its own colour, which changes every day (see [Palette]).
 */
enum class Slide(val label: String) {
    HOOK("How to"),
    LINE("The line"),
    LOOK("Look closer"),
    STEAL("Steal it"),
    AROUND("Around it");

    fun body(context: Context, card: Card): CharSequence = when (this) {
        HOOK -> hookTitle(card)
        LINE -> "“${card.quote}”"
        LOOK -> Markup.note(context, card.lookCloser)
        STEAL -> Markup.note(context, card.stealIt)
        AROUND -> Markup.note(context, card.aroundIt)
    }

    companion object {
        /** “How to make the impossible believable” → “make the impossible believable”; the “How to” sits above it. */
        fun hookTitle(card: Card): String = card.job.removePrefix(HOW_TO).trim()

        /** Whether the job starts with “How to”, so the hook can show it in its pill. */
        fun hasHowTo(card: Card) = card.job.startsWith(HOW_TO)

        private const val HOW_TO = "How to "
    }
}

object Cards {
    @Volatile private var cache: List<Card>? = null

    fun all(context: Context): List<Card> =
        cache ?: synchronized(this) { cache ?: load(context).also { cache = it } }

    /** The downloaded copy of cards.json, if the app has fetched one. */
    fun cacheFile(context: Context) = File(context.filesDir, "cards.json")

    /** Drop the in-memory copy so the next read picks up a fresh download. */
    fun invalidate() = synchronized(this) { cache = null }

    /** Parses a cards.json string, throwing if it isn't usable. */
    fun parse(text: String): List<Card> {
        val array = JSONArray(text)
        val cards = List(array.length()) { i ->
            val o = array.getJSONObject(i)
            val highlights = o.getJSONArray("highlights")
            Card(
                id = o.getString("id"),
                job = o.getString("job"),
                quote = o.getString("quote"),
                author = o.getString("author"),
                work = o.getString("work"),
                year = o.optInt("year"),
                translator = if (o.isNull("translator")) null else o.getString("translator"),
                highlights = List(highlights.length()) { highlights.getString(it) },
                lookCloser = o.getString("lookCloser"),
                aroundIt = o.getString("aroundIt"),
                stealIt = o.getString("stealIt"),
            )
        }
        require(cards.isNotEmpty())
        return cards
    }

    /**
     * The same card all day, a new one each day, cycling through the whole set. If you left the
     * app on a different card, that card is today's and the days carry on from it.
     */
    fun todayIndex(context: Context): Int {
        val cards = all(context)
        val today = LocalDate.now().toEpochDay()
        val start = Prefs.startCard(context)?.let { (id, day) ->
            cards.indexOfFirst { it.id == id }.takeIf { it >= 0 }?.let { it - day }
        } ?: 0L
        return Math.floorMod(start + today, cards.size.toLong()).toInt()
    }

    /** Makes [index] today's card, so the widget shows it now and moves on from it each day. */
    fun startFrom(context: Context, index: Int) {
        Prefs.setStartCard(context, all(context)[index].id, LocalDate.now().toEpochDay())
    }

    fun slides(context: Context): List<Slide> =
        if (Prefs.showSteal(context)) Slide.entries else Slide.entries - Slide.STEAL

    /** Prefer the latest download; fall back to the copy built into the app. */
    private fun load(context: Context): List<Card> {
        val assetCards = runCatching {
            parse(context.assets.open("cards.json").bufferedReader().use { it.readText() })
        }.getOrNull() ?: emptyList()

        val file = cacheFile(context)
        if (!file.exists()) return assetCards

        val cachedCards = runCatching { parse(file.readText()) }.getOrNull()
        if (cachedCards == null || cachedCards.isEmpty()) return assetCards

        return if (assetCards.size >= cachedCards.size && assetCards.isNotEmpty()) {
            runCatching { file.delete() }
            assetCards
        } else {
            cachedCards
        }
    }
}

object Prefs {
    private const val FILE = "marginalia"
    private const val SHOW_STEAL = "show_steal"

    fun showSteal(context: Context) =
        context.getSharedPreferences(FILE, Context.MODE_PRIVATE).getBoolean(SHOW_STEAL, true)

    fun setShowSteal(context: Context, value: Boolean) {
        context.getSharedPreferences(FILE, Context.MODE_PRIVATE).edit().putBoolean(SHOW_STEAL, value).apply()
    }

    private const val START_CARD = "start_card"
    private const val START_DAY = "start_day"

    /** The card you last left the app on, by id, and the day you left it there. */
    fun startCard(context: Context): Pair<String, Long>? {
        val prefs = context.getSharedPreferences(FILE, Context.MODE_PRIVATE)
        val id = prefs.getString(START_CARD, null) ?: return null
        return id to prefs.getLong(START_DAY, 0)
    }

    fun setStartCard(context: Context, id: String, day: Long) {
        context.getSharedPreferences(FILE, Context.MODE_PRIVATE).edit()
            .putString(START_CARD, id).putLong(START_DAY, day).apply()
    }

    private const val START_SHELF_INDEX = "start_shelf_index"
    private const val START_SHELF_DAY = "start_shelf_day"

    /** The shelf quote index you last left the app on, and the day you left it there. */
    fun startShelf(context: Context): Pair<Int, Long>? {
        val prefs = context.getSharedPreferences(FILE, Context.MODE_PRIVATE)
        if (!prefs.contains(START_SHELF_INDEX)) return null
        return prefs.getInt(START_SHELF_INDEX, 0) to prefs.getLong(START_SHELF_DAY, 0L)
    }

    fun setStartShelf(context: Context, index: Int, day: Long) {
        context.getSharedPreferences(FILE, Context.MODE_PRIVATE).edit()
            .putInt(START_SHELF_INDEX, index).putLong(START_SHELF_DAY, day).apply()
    }

    private const val BASE_MODE = "base_mode"
    private const val BASE_MODE_DAY = "base_mode_day"

    const val MODE_CARDS = 0
    const val MODE_SHELF = 1

    /**
     * Determines today's mode, alternating each day between Daily Craft Cards (MODE_CARDS)
     * and Shelf Quotes (MODE_SHELF). If the user manually flips modes, that choice becomes
     * the base for today, and the daily alternation continues from there.
     */
    fun todayMode(context: Context): Int {
        val prefs = context.getSharedPreferences(FILE, Context.MODE_PRIVATE)
        val today = LocalDate.now().toEpochDay()
        val baseMode = prefs.getInt(BASE_MODE, MODE_CARDS)
        val baseDay = prefs.getLong(BASE_MODE_DAY, today)
        val offset = Math.floorMod(today - baseDay, 2L)
        return if (offset == 0L) baseMode else (1 - baseMode)
    }

    fun setMode(context: Context, mode: Int) {
        val today = LocalDate.now().toEpochDay()
        context.getSharedPreferences(FILE, Context.MODE_PRIVATE).edit()
            .putInt(BASE_MODE, mode)
            .putLong(BASE_MODE_DAY, today)
            .apply()
    }

    private const val SPARK_QUEUE = "spark_queue"

    fun sparkQueue(context: Context): Set<String> {
        val prefs = context.getSharedPreferences(FILE, Context.MODE_PRIVATE)
        return prefs.getStringSet(SPARK_QUEUE, emptySet()) ?: emptySet()
    }

    fun toggleSpark(context: Context, work: String): Boolean {
        val prefs = context.getSharedPreferences(FILE, Context.MODE_PRIVATE)
        val current = prefs.getStringSet(SPARK_QUEUE, emptySet())?.toMutableSet() ?: mutableSetOf()
        val added = if (current.contains(work)) {
            current.remove(work)
            false
        } else {
            current.add(work)
            true
        }
        prefs.edit().putStringSet(SPARK_QUEUE, current).apply()
        return added
    }
}
