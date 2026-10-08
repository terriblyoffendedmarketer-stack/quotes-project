package com.marginalia.widget

import android.app.AlarmManager
import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.graphics.Typeface
import android.os.Bundle
import android.text.TextPaint
import android.view.View
import android.widget.RemoteViews
import androidx.core.content.ContextCompat
import com.marginalia.Cards
import com.marginalia.ContentSync
import com.marginalia.MainActivity
import com.marginalia.Markup
import com.marginalia.R
import com.marginalia.Slide
import java.time.LocalDate
import java.time.ZoneId

/**
 * Home-screen widget showing today's card one slide at a time, like stories, each slide in its own colour:
 * tap the right side for the next slide and the left side to go back.
 *
 * Every slide is drawn straight into the widget's views, with no list adapter or service,
 * so the launcher keeps a finished picture and shows it instantly when you come back.
 */
class CardWidgetProvider : AppWidgetProvider() {

    override fun onUpdate(context: Context, manager: AppWidgetManager, ids: IntArray) {
        ids.forEach { manager.updateAppWidget(it, render(context, it)) }
        scheduleMidnight(context)
        // Check for new cards in the background; a download redraws the widget itself.
        val pending = goAsync()
        ContentSync.syncIfDue(context) { pending.finish() }
    }

    override fun onReceive(context: Context, intent: Intent) {
        when (intent.action) {
            ACTION_STEP -> {
                val id = intent.getIntExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, AppWidgetManager.INVALID_APPWIDGET_ID)
                if (id != AppWidgetManager.INVALID_APPWIDGET_ID) step(context, id, intent.getIntExtra(EXTRA_DIRECTION, 1))
            }
            ACTION_MIDNIGHT, Intent.ACTION_TIME_CHANGED, Intent.ACTION_TIMEZONE_CHANGED -> refreshAll(context)
            else -> super.onReceive(context, intent)
        }
    }

    /** Redraw at the new size when the widget is resized, so the hook still fills it. */
    override fun onAppWidgetOptionsChanged(context: Context, manager: AppWidgetManager, id: Int, options: Bundle) {
        manager.updateAppWidget(id, render(context, id))
    }

    override fun onDeleted(context: Context, ids: IntArray) {
        val prefs = state(context).edit()
        ids.forEach { prefs.remove(slideKey(it)).remove(dayKey(it)) }
        prefs.apply()
    }

    companion object {
        private const val ACTION_STEP = "com.marginalia.widget.STEP"
        private const val ACTION_MIDNIGHT = "com.marginalia.widget.MIDNIGHT"
        private const val EXTRA_DIRECTION = "direction"

        fun refreshAll(context: Context) {
            val manager = AppWidgetManager.getInstance(context)
            val ids = manager.getAppWidgetIds(ComponentName(context, CardWidgetProvider::class.java))
            ids.forEach { manager.updateAppWidget(it, render(context, it)) }
            if (ids.isNotEmpty()) scheduleMidnight(context)
        }

        private fun state(context: Context) = context.getSharedPreferences("widget_state", Context.MODE_PRIVATE)
        private fun slideKey(id: Int) = "slide_$id"
        private fun dayKey(id: Int) = "day_$id"

        /** Which slide this widget is on. Starts again from the hook each new day. */
        private fun currentSlide(context: Context, id: Int): Int {
            val prefs = state(context)
            val today = LocalDate.now().toEpochDay()
            if (prefs.getLong(dayKey(id), -1) != today) {
                prefs.edit().putLong(dayKey(id), today).putInt(slideKey(id), 0).apply()
                return 0
            }
            return prefs.getInt(slideKey(id), 0).coerceIn(0, Cards.slides(context).lastIndex)
        }

        private fun step(context: Context, id: Int, direction: Int) {
            val count = Cards.slides(context).size
            val next = Math.floorMod(currentSlide(context, id) + direction, count)
            state(context).edit().putInt(slideKey(id), next).putLong(dayKey(id), LocalDate.now().toEpochDay()).apply()
            AppWidgetManager.getInstance(context).updateAppWidget(id, render(context, id))
        }

        private fun render(context: Context, id: Int): RemoteViews {
            val slides = Cards.slides(context)
            val index = Cards.todayIndex(context)
            val card = Cards.all(context)[index]
            val position = currentSlide(context, id)
            val slide = slides[position]
            val isHook = slide == Slide.HOOK
            val isLine = slide == Slide.LINE
            val size = WidgetFit.size(context, id)

            return RemoteViews(context.packageName, R.layout.widget_card).apply {
                setInt(R.id.widget_root, "setBackgroundResource", slide.widgetBg)
                setViewVisibility(R.id.hook, if (isHook) View.VISIBLE else View.GONE)
                setViewVisibility(R.id.content, if (isHook) View.GONE else View.VISIBLE)
                if (isHook) {
                    setViewVisibility(R.id.hook_pill, if (Slide.hasHowTo(card)) View.VISIBLE else View.GONE)
                    setViewVisibility(R.id.hook_hint, if (size.compact) View.GONE else View.VISIBLE)
                    setImageViewBitmap(R.id.hook_title, HookArt.draw(context, size, Slide.hookTitle(card)))
                    setContentDescription(R.id.hook_title, card.job)
                } else {
                    val credit = Markup.credit(card)
                    setTextViewText(R.id.slide_kicker, slide.label.uppercase())
                    // On a small widget the footer already names the slide, so the kicker makes room.
                    setViewVisibility(R.id.slide_kicker, if (size.compact) View.GONE else View.VISIBLE)
                    setViewVisibility(R.id.slide_line, if (isLine) View.VISIBLE else View.GONE)
                    setViewVisibility(R.id.slide_note, if (isLine) View.GONE else View.VISIBLE)
                    setViewVisibility(R.id.slide_credit, if (isLine) View.VISIBLE else View.GONE)
                    setViewVisibility(R.id.slide_job, if (size.compact) View.GONE else View.VISIBLE)
                    val body = fitted(context, size, slide.body(context, card), isLine, if (isLine) credit else null)
                    if (isLine) {
                        setTextViewText(R.id.slide_line, body)
                        setTextViewText(R.id.slide_credit, credit)
                    } else {
                        setTextViewText(R.id.slide_note, body)
                    }
                    setTextViewText(R.id.slide_job, card.job)
                }
                // The footer takes the hook's ink on the cobalt slide.
                val ink = ContextCompat.getColor(context, if (isHook) R.color.hook_ink else R.color.widget_text)
                val soft = ContextCompat.getColor(context, if (isHook) R.color.hook_soft else R.color.widget_soft)
                setTextColor(R.id.widget_progress, soft)
                setTextColor(R.id.widget_open, ink)
                setTextViewText(
                    R.id.widget_progress,
                    context.getString(R.string.progress, position + 1, slides.size, slide.label),
                )
                setOnClickPendingIntent(R.id.tap_back, stepIntent(context, id, -1))
                setOnClickPendingIntent(R.id.tap_next, stepIntent(context, id, 1))
                val open = Intent(context, MainActivity::class.java)
                    .putExtra(MainActivity.EXTRA_CARD, index)
                    .putExtra(MainActivity.EXTRA_SLIDE, position)
                setOnClickPendingIntent(
                    R.id.widget_open,
                    PendingIntent.getActivity(
                        context, id, open,
                        PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
                    ),
                )
            }
        }

        /**
         * The slide's text, shortened with "…" if even the smallest comfortable size won't fit it
         * in the space this widget has. The text view then sizes it up from there to fill the space.
         */
        private fun fitted(context: Context, size: WidgetFit.Size, text: CharSequence, isLine: Boolean, credit: CharSequence?): CharSequence {
            val width = WidgetFit.dp(context, size.widthDp - 40f).toInt()
            val paint = TextPaint(TextPaint.ANTI_ALIAS_FLAG).apply {
                typeface = if (isLine) Typeface.create(Typeface.SERIF, Typeface.BOLD) else Typeface.DEFAULT
                textSize = WidgetFit.sp(context, if (isLine) LINE_FIT_SP else NOTE_FIT_SP)
            }
            // Everything on a text slide besides the text: padding, the kicker (not on small widgets)
            // and the footer, then the credit (as many lines as it takes) and the fine print.
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

        // The sizes text is fitted at before it's shortened. The views can still go a little
        // smaller (see widget_card.xml), which covers any slack in the space worked out above.
        private const val LINE_FIT_SP = 14f
        private const val NOTE_FIT_SP = 12f

        private fun stepIntent(context: Context, id: Int, direction: Int): PendingIntent {
            val intent = Intent(context, CardWidgetProvider::class.java)
                .setAction(ACTION_STEP)
                .putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, id)
                .putExtra(EXTRA_DIRECTION, direction)
            // A distinct request code per widget and direction keeps the two taps apart.
            val requestCode = id * 2 + if (direction > 0) 1 else 0
            return PendingIntent.getBroadcast(
                context, requestCode, intent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
            )
        }

        /** Wake up just after midnight so the new day's card is there in the morning. */
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
