package com.marginalia

import android.content.Context
import androidx.annotation.ColorRes
import androidx.annotation.DrawableRes
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
 * Each slide has its own colour, in the app and the widget.
 */
enum class Slide(val label: String, @ColorRes val color: Int, @DrawableRes val widgetBg: Int) {
    HOOK("How to", R.color.slide_hook, R.drawable.widget_bg_hook),
    LINE("The line", R.color.slide_line, R.drawable.widget_bg_line),
    LOOK("Look closer", R.color.slide_look, R.drawable.widget_bg_look),
    STEAL("Steal it", R.color.slide_steal, R.drawable.widget_bg_steal),
    AROUND("Around it", R.color.slide_around, R.drawable.widget_bg_around);

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

    /** The same card all day, a new one each day, cycling through the whole set. */
    fun todayIndex(context: Context): Int {
        val n = all(context).size
        return Math.floorMod(LocalDate.now().toEpochDay(), n.toLong()).toInt()
    }

    fun slides(context: Context): List<Slide> =
        if (Prefs.showSteal(context)) Slide.entries else Slide.entries - Slide.STEAL

    /** Prefer the latest download; fall back to the copy built into the app. */
    private fun load(context: Context): List<Card> {
        val file = cacheFile(context)
        if (file.exists()) {
            runCatching { return parse(file.readText()) }
        }
        return parse(context.assets.open("cards.json").bufferedReader().use { it.readText() })
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
}
