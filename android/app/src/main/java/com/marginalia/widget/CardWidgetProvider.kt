package com.marginalia.widget

import android.app.AlarmManager
import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.graphics.Typeface
import android.os.Build
import android.os.Bundle
import android.text.TextPaint
import android.view.View
import android.widget.RemoteViews
import androidx.annotation.ColorRes
import androidx.core.content.ContextCompat
import com.marginalia.BankQuote
import com.marginalia.Cards
import com.marginalia.ContentSync
import com.marginalia.MainActivity
import com.marginalia.Markup
import com.marginalia.Palette
import com.marginalia.Prefs
import com.marginalia.QuoteBank
import com.marginalia.R
import com.marginalia.Slide
import java.time.LocalDate
import java.time.ZoneId

/**
 * Adaptive dual-mode home-screen widget:
 * - Mode 1: Daily Craft Card (5 slides: Hook, Line, Look, Steal, Around)
 * - Mode 2: Shelf Spark (2 slides: The Line, Scene Context)
 *
 * Tap [ ⇄ ] in the footer to toggle modes in place without needing multiple widgets on the screen.
 * In Shelf Spark mode, tapping right reveals the complete Scene Context before advancing to the next book.
 */
class CardWidgetProvider : AppWidgetProvider() {

    override fun onUpdate(context: Context, manager: AppWidgetManager, ids: IntArray) {
        ids.forEach { manager.updateAppWidget(it, render(context, it)) }
        scheduleMidnight(context)
        val pending = goAsync()
        ContentSync.syncIfDue(context) { pending.finish() }
    }

    override fun onReceive(context: Context, intent: Intent) {
        when (intent.action) {
            ACTION_STEP -> {
                val id = intent.getIntExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, AppWidgetManager.INVALID_APPWIDGET_ID)
                if (id != AppWidgetManager.INVALID_APPWIDGET_ID) step(context, id, intent.getIntExtra(EXTRA_DIRECTION, 1))
            }
            ACTION_TOGGLE_MODE -> {
                val id = intent.getIntExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, AppWidgetManager.INVALID_APPWIDGET_ID)
                if (id != AppWidgetManager.INVALID_APPWIDGET_ID) toggleMode(context, id)
            }
            ACTION_MIDNIGHT, Intent.ACTION_TIME_CHANGED, Intent.ACTION_TIMEZONE_CHANGED -> refreshAll(context)
            else -> super.onReceive(context, intent)
        }
    }

    override fun onAppWidgetOptionsChanged(context: Context, manager: AppWidgetManager, id: Int, options: Bundle) {
        manager.updateAppWidget(id, render(context, id))
    }

    override fun onDeleted(context: Context, ids: IntArray) {
        val prefs = state(context).edit()
        ids.forEach {
            prefs.remove(slideKey(it))
                .remove(dayKey(it))
                .remove(cardKey(it))
                .remove(modeKey(it))
                .remove(shelfKey(it))
                .remove(shelfSlideKey(it))
        }
        prefs.apply()
    }

    companion object {
        private const val ACTION_STEP = "com.marginalia.widget.STEP"
        private const val ACTION_TOGGLE_MODE = "com.marginalia.widget.TOGGLE_MODE"
        private const val ACTION_MIDNIGHT = "com.marginalia.widget.MIDNIGHT"
        private const val EXTRA_DIRECTION = "direction"

        private const val MODE_CARDS = 0
        private const val MODE_SHELF = 1

        fun refreshAll(context: Context) {
            val manager = AppWidgetManager.getInstance(context)
            val ids = manager.getAppWidgetIds(ComponentName(context, CardWidgetProvider::class.java))
            ids.forEach { manager.updateAppWidget(it, render(context, it)) }
            if (ids.isNotEmpty()) scheduleMidnight(context)
        }

        private fun state(context: Context) = context.getSharedPreferences("widget_state", Context.MODE_PRIVATE)
        private fun slideKey(id: Int) = "slide_$id"
        private fun dayKey(id: Int) = "day_$id"
        private fun cardKey(id: Int) = "card_$id"
        private fun modeKey(id: Int) = "mode_$id"
        private fun shelfKey(id: Int) = "shelf_idx_$id"
        private fun shelfSlideKey(id: Int) = "shelf_slide_$id"
        private fun cardId(context: Context) = Cards.all(context)[Cards.todayIndex(context)].id

        private fun currentMode(context: Context, id: Int): Int {
            return Prefs.todayMode(context)
        }

        private fun toggleMode(context: Context, id: Int) {
            val newMode = if (currentMode(context, id) == MODE_CARDS) MODE_SHELF else MODE_CARDS
            Prefs.setMode(context, newMode)
            refreshAll(context)
        }

        /** Which slide this widget is on in Card mode (0 to 4). */
        private fun currentSlide(context: Context, id: Int): Int {
            val prefs = state(context)
            val today = LocalDate.now().toEpochDay()
            val card = cardId(context)
            if (prefs.getLong(dayKey(id), -1) != today || prefs.getString(cardKey(id), null) != card) {
                prefs.edit().putLong(dayKey(id), today).putString(cardKey(id), card).putInt(slideKey(id), 0).apply()
                return 0
            }
            return prefs.getInt(slideKey(id), 0).coerceIn(0, Cards.slides(context).lastIndex)
        }

        data class WidgetShelfChunk(
            val label: String,
            val pill: String,
            val text: String,
            val isLine: Boolean,
            val step: Int = 1,
            val total: Int = 1
        )

        private fun getWidgetShelfSlides(q: BankQuote, maxWords: Int = 60): List<WidgetShelfChunk> {
            val slides = mutableListOf<WidgetShelfChunk>()
            slides.add(WidgetShelfChunk(label = "The Line", pill = "THE LINE", text = q.quote, isLine = true))

            val paragraphs = q.explanation.split("\n\n").map { it.trim() }.filter { it.isNotEmpty() }
            paragraphs.forEachIndexed { pIdx, paragraph ->
                val (baseLabel, basePill) = when (pIdx) {
                    0 -> "The Predicament" to "THE PREDICAMENT"
                    1 -> "The Mirror" to "THE MIRROR"
                    else -> "The Insight" to "THE INSIGHT"
                }
                val words = paragraph.split(Regex("\\s+"))
                if (words.size <= maxWords) {
                    slides.add(WidgetShelfChunk(label = baseLabel, pill = basePill, text = paragraph, isLine = false))
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
                        slides.add(WidgetShelfChunk(label = chunkLabel, pill = chunkPill, text = chunk, isLine = false))
                    }
                }
            }

            val total = slides.size
            return slides.mapIndexed { idx, s ->
                s.copy(
                    step = idx + 1,
                    total = total
                )
            }
        }

        /** Which quote in Shelf mode (always today's quote). */
        private fun currentShelfIndex(context: Context, id: Int): Int {
            return QuoteBank.todayIndex(context)
        }

        /** Which slide in Shelf mode. Resets to 0 each morning. */
        private fun currentShelfSlide(context: Context, id: Int, totalSlides: Int): Int {
            val prefs = state(context)
            val today = LocalDate.now().toEpochDay()
            val shelfDayKey = "shelf_day_$id"
            if (prefs.getLong(shelfDayKey, -1) != today) {
                prefs.edit().putLong(shelfDayKey, today).putInt(shelfSlideKey(id), 0).apply()
                return 0
            }
            return prefs.getInt(shelfSlideKey(id), 0).coerceIn(0, (totalSlides - 1).coerceAtLeast(0))
        }

        private fun step(context: Context, id: Int, direction: Int) {
            if (currentMode(context, id) == MODE_CARDS) {
                val count = Cards.slides(context).size
                val next = Math.floorMod(currentSlide(context, id) + direction, count)
                state(context).edit().putInt(slideKey(id), next).putLong(dayKey(id), LocalDate.now().toEpochDay())
                    .putString(cardKey(id), cardId(context)).apply()
            } else {
                val quotes = QuoteBank.all(context)
                if (quotes.isNotEmpty()) {
                    val q = quotes[currentShelfIndex(context, id)]
                    val widgetSlides = getWidgetShelfSlides(q)
                    val total = widgetSlides.size
                    val slide = currentShelfSlide(context, id, total)
                    val nextSlide = Math.floorMod(slide + direction, total)
                    state(context).edit().putInt(shelfSlideKey(id), nextSlide)
                        .putLong("shelf_day_$id", LocalDate.now().toEpochDay()).apply()
                }
            }
            AppWidgetManager.getInstance(context).updateAppWidget(id, render(context, id))
        }

        private fun render(context: Context, id: Int): RemoteViews {
            val mode = currentMode(context, id)
            val size = WidgetFit.size(context, id)

            return RemoteViews(context.packageName, R.layout.widget_card).apply {
                setOnClickPendingIntent(R.id.widget_mode_toggle, toggleModeIntent(context, id))
                setOnClickPendingIntent(R.id.tap_back, stepIntent(context, id, -1))
                setOnClickPendingIntent(R.id.tap_next, stepIntent(context, id, 1))

                if (mode == MODE_CARDS) {
                    renderCardsMode(context, id, size, this)
                } else {
                    renderShelfMode(context, id, size, this)
                }
            }
        }

        private fun renderCardsMode(context: Context, id: Int, size: WidgetFit.Size, views: RemoteViews) {
            val slides = Cards.slides(context)
            val index = Cards.todayIndex(context)
            val card = Cards.all(context)[index]
            val position = currentSlide(context, id)
            val slide = slides[position]
            val isHook = slide == Slide.HOOK
            val isLine = slide == Slide.LINE

            val colors = Palette.today()
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                views.setColorInt(R.id.widget_bg, "setColorFilter", colors.light(slide), colors.dark(slide))
            } else {
                views.setInt(R.id.widget_bg, "setColorFilter", colors.color(context, slide))
            }

            views.setViewVisibility(R.id.shelf, View.GONE)
            views.setViewVisibility(R.id.hook, if (isHook) View.VISIBLE else View.GONE)
            views.setViewVisibility(R.id.content, if (isHook) View.GONE else View.VISIBLE)

            if (isHook) {
                views.setViewVisibility(R.id.hook_pill, if (Slide.hasHowTo(card)) View.VISIBLE else View.GONE)
                views.setTextColor(R.id.hook_pill, colors.hook)
                views.setTextViewText(R.id.hook_author, card.author)
                views.setViewVisibility(R.id.hook_hint, if (size.compact) View.GONE else View.VISIBLE)
                views.setImageViewBitmap(R.id.hook_title, HookArt.draw(context, size, Slide.hookTitle(card)))
                views.setContentDescription(R.id.hook_title, card.job)
            } else {
                val credit = Markup.credit(card)
                views.setTextViewText(R.id.slide_kicker, slide.label.uppercase())
                views.setViewVisibility(R.id.slide_kicker, if (size.compact) View.GONE else View.VISIBLE)
                views.setViewVisibility(R.id.slide_line, if (isLine) View.VISIBLE else View.GONE)
                views.setViewVisibility(R.id.slide_note, if (isLine) View.GONE else View.VISIBLE)
                views.setViewVisibility(R.id.slide_credit, if (isLine) View.VISIBLE else View.GONE)
                views.setViewVisibility(R.id.slide_job, if (size.compact) View.GONE else View.VISIBLE)
                val body = fitted(context, size, slide.body(context, card), isLine, if (isLine) credit else null)
                if (isLine) {
                    views.setTextViewText(R.id.slide_line, body)
                    views.setTextViewText(R.id.slide_credit, credit)
                } else {
                    views.setTextViewText(R.id.slide_note, body)
                }
                views.setTextViewText(R.id.slide_job, card.job)
            }

            views.textColor(context, R.id.widget_progress, if (isHook) R.color.hook_soft else R.color.widget_soft)
            views.textColor(context, R.id.widget_open, if (isHook) R.color.hook_ink else R.color.widget_text)
            views.textColor(context, R.id.widget_mode_toggle, if (isHook) R.color.hook_ink else R.color.widget_text)

            views.setTextViewText(
                R.id.widget_progress,
                context.getString(R.string.progress, position + 1, slides.size, slide.label),
            )
            views.setTextViewText(R.id.widget_mode_toggle, context.getString(R.string.toggle_shelf))

            val open = Intent(context, MainActivity::class.java)
                .putExtra(MainActivity.EXTRA_MODE, MainActivity.MODE_CARDS)
                .putExtra(MainActivity.EXTRA_CARD, index)
                .putExtra(MainActivity.EXTRA_SLIDE, position)
            views.setOnClickPendingIntent(
                R.id.widget_open,
                PendingIntent.getActivity(
                    context, id, open,
                    PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
                ),
            )
        }

        private fun renderShelfMode(context: Context, id: Int, size: WidgetFit.Size, views: RemoteViews) {
            val quotes = QuoteBank.all(context)
            if (quotes.isEmpty()) return

            val shelfIdx = currentShelfIndex(context, id)
            val q = quotes[shelfIdx]
            val widgetSlides = getWidgetShelfSlides(q)
            val totalSlides = widgetSlides.size
            val shelfSlide = currentShelfSlide(context, id, totalSlides)
            val current = widgetSlides[shelfSlide]

            // Tint widget background with a deep literary tone
            val shelfColorLight = Color.parseColor("#f4f5f2")
            val shelfColorDark = Color.parseColor("#1a1d22")
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                views.setColorInt(R.id.widget_bg, "setColorFilter", shelfColorLight, shelfColorDark)
            } else {
                views.setInt(R.id.widget_bg, "setColorFilter", shelfColorDark)
            }

            views.setViewVisibility(R.id.hook, View.GONE)
            views.setViewVisibility(R.id.content, View.GONE)
            views.setViewVisibility(R.id.shelf, View.VISIBLE)

            val progressPill = current.pill
            val navHint = if (shelfSlide < totalSlides - 1) "Next →" else "Restart ↺"

            if (current.isLine) {
                // Slide 1: The Line
                views.setViewVisibility(R.id.shelf_line_layout, View.VISIBLE)
                views.setViewVisibility(R.id.shelf_context_layout, View.GONE)

                views.setTextViewText(R.id.shelf_book, q.work)
                views.setTextViewText(R.id.shelf_pill, progressPill)
                views.setTextViewText(R.id.shelf_quote, "“${current.text}”")
                val yearStr = if (q.year != null) " · ${q.year}" else ""
                views.setTextViewText(R.id.shelf_author, "— ${q.author}$yearStr")
                views.setTextViewText(R.id.shelf_nav_hint, navHint)

                views.setTextViewText(R.id.widget_progress, "${shelfSlide + 1} of $totalSlides · ${current.label}")
            } else {
                // Context Slides: Segregated chunks (Full height, never cut off!)
                views.setViewVisibility(R.id.shelf_line_layout, View.GONE)
                views.setViewVisibility(R.id.shelf_context_layout, View.VISIBLE)

                views.setTextViewText(R.id.shelf_context_book, q.work)
                views.setTextViewText(R.id.shelf_context_pill, progressPill)
                views.setTextViewText(R.id.shelf_explanation, current.text)
                views.setTextViewText(R.id.shelf_context_author, "— ${q.author}")
                views.setTextViewText(R.id.shelf_context_nav_hint, navHint)

                views.setTextViewText(R.id.widget_progress, "${shelfSlide + 1} of $totalSlides · ${current.label}")
            }

            views.textColor(context, R.id.widget_progress, R.color.widget_soft)
            views.textColor(context, R.id.widget_open, R.color.widget_text)
            views.textColor(context, R.id.widget_mode_toggle, R.color.widget_text)

            views.setTextViewText(R.id.widget_mode_toggle, context.getString(R.string.toggle_craft))

            // Open Quote Bank view in MainActivity right on this quote!
            val open = Intent(context, MainActivity::class.java)
                .putExtra(MainActivity.EXTRA_MODE, MainActivity.MODE_BANK)
                .putExtra(MainActivity.EXTRA_BANK_INDEX, shelfIdx)
                .putExtra(MainActivity.EXTRA_SLIDE, shelfSlide)
            views.setOnClickPendingIntent(
                R.id.widget_open,
                PendingIntent.getActivity(
                    context, id, open,
                    PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
                ),
            )
        }

        private fun RemoteViews.textColor(context: Context, view: Int, @ColorRes color: Int) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                setColorStateList(view, "setTextColor", color)
            } else {
                setTextColor(view, ContextCompat.getColor(context, color))
            }
        }

        private fun fitted(context: Context, size: WidgetFit.Size, text: CharSequence, isLine: Boolean, credit: CharSequence?): CharSequence {
            val width = WidgetFit.dp(context, size.widthDp - 40f).toInt()
            val paint = TextPaint(TextPaint.ANTI_ALIAS_FLAG).apply {
                typeface = if (isLine) Typeface.create(Typeface.SERIF, Typeface.BOLD) else Typeface.DEFAULT
                textSize = WidgetFit.sp(context, if (isLine) LINE_FIT_SP else NOTE_FIT_SP)
            }
            var reserved = WidgetFit.dp(context, if (size.compact) 78f else 94f)
            if (credit != null) {
                val creditPaint = TextPaint(TextPaint.ANTI_ALIAS_FLAG).apply { textSize = WidgetFit.sp(context, 13f) }
                val lines = WidgetFit.layout(credit, creditPaint, width, 1f).lineCount.coerceIn(1, 2)
                reserved += WidgetFit.dp(context, 8f) + lines * WidgetFit.sp(context, 17f)
            }
            if (!size.compact) reserved += WidgetFit.dp(context, 8f) + WidgetFit.sp(context, 15f)
            val height = ((WidgetFit.dp(context, size.heightDp.toFloat()) - reserved) * 0.95f).toInt().coerceAtLeast(1)
            val spacing = if (isLine) 1.15f else 1.25f
            return WidgetFit.fit(text, paint, width, height, spacing, closing = if (isLine) "”" else "")
        }

        private const val LINE_FIT_SP = 14f
        private const val NOTE_FIT_SP = 12f

        private fun stepIntent(context: Context, id: Int, direction: Int): PendingIntent {
            val intent = Intent(context, CardWidgetProvider::class.java)
                .setAction(ACTION_STEP)
                .putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, id)
                .putExtra(EXTRA_DIRECTION, direction)
            val requestCode = id * 4 + if (direction > 0) 1 else 0
            return PendingIntent.getBroadcast(
                context, requestCode, intent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
            )
        }

        private fun toggleModeIntent(context: Context, id: Int): PendingIntent {
            val intent = Intent(context, CardWidgetProvider::class.java)
                .setAction(ACTION_TOGGLE_MODE)
                .putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, id)
            val requestCode = id * 4 + 2
            return PendingIntent.getBroadcast(
                context, requestCode, intent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
            )
        }

        private fun scheduleMidnight(context: Context) {
            val alarms = context.getSystemService(AlarmManager::class.java) ?: return
            val zone = ZoneId.systemDefault()
            val at = LocalDate.now(zone).plusDays(1).atStartOfDay(zone).plusMinutes(1).toInstant().toEpochMilli()
            val intent = PendingIntent.getBroadcast(
                context, 0,
                Intent(context, CardWidgetProvider::class.java).setAction(ACTION_MIDNIGHT),
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
            )
            alarms.set(AlarmManager.RTC, at, intent)
        }
    }
}
