package com.marginalia.widget

import android.appwidget.AppWidgetManager
import android.content.Context
import android.content.res.Configuration
import android.text.Layout
import android.text.SpannableStringBuilder
import android.text.StaticLayout
import android.text.TextPaint
import android.util.TypedValue

/**
 * Keeps every slide readable at whatever size the widget is dragged to.
 *
 * The widget's text views shrink their text to fit, but only down to a floor. Past that,
 * text would be cut off mid-line, so slides that are too long for the space are shortened
 * here first, at a word, and end with "…". "Open ↗" shows the whole slide.
 */
object WidgetFit {

    /** The widget's current size in dp, as the launcher reports it. */
    data class Size(val widthDp: Int, val heightDp: Int) {
        /** Small enough that the extras (the hint, the fine print) give their space to the text. */
        val compact get() = heightDp < 220 || widthDp < 230
    }

    fun size(context: Context, widgetId: Int): Size {
        val options = AppWidgetManager.getInstance(context).getAppWidgetOptions(widgetId)
        val portrait = context.resources.configuration.orientation != Configuration.ORIENTATION_LANDSCAPE
        val width = options.getInt(
            if (portrait) AppWidgetManager.OPTION_APPWIDGET_MIN_WIDTH else AppWidgetManager.OPTION_APPWIDGET_MAX_WIDTH, 0,
        )
        val height = options.getInt(
            if (portrait) AppWidgetManager.OPTION_APPWIDGET_MAX_HEIGHT else AppWidgetManager.OPTION_APPWIDGET_MIN_HEIGHT, 0,
        )
        return Size(if (width > 0) width else 320, if (height > 0) height else 300)
    }

    fun dp(context: Context, value: Float) =
        TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, value, context.resources.displayMetrics)

    fun sp(context: Context, value: Float) =
        TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_SP, value, context.resources.displayMetrics)

    fun layout(text: CharSequence, paint: TextPaint, width: Int, spacing: Float): StaticLayout =
        StaticLayout.Builder.obtain(text, 0, text.length, paint, width.coerceAtLeast(1))
            .setAlignment(Layout.Alignment.ALIGN_NORMAL)
            .setLineSpacing(0f, spacing)
            .setIncludePad(false)
            .build()

    /**
     * [text] as it is if it fits [width] × [height] px at [paint]'s size, otherwise the longest
     * opening that does, cut at a word and ending “…” plus [closing] (such as a closing quote mark).
     */
    fun fit(text: CharSequence, paint: TextPaint, width: Int, height: Int, spacing: Float, closing: String = ""): CharSequence {
        if (layout(text, paint, width, spacing).height <= height) return text

        val breaks = text.indices.filter { text[it] == ' ' || text[it] == '\n' }
        if (breaks.isEmpty()) return text

        fun cut(end: Int): CharSequence {
            var stop = end
            while (stop > 0 && text[stop - 1] in TRAILING) stop--
            return SpannableStringBuilder(text.subSequence(0, stop)).append("…").append(closing)
        }

        var low = 0
        var high = breaks.lastIndex
        var best = cut(breaks[0])
        while (low <= high) {
            val mid = (low + high) / 2
            val candidate = cut(breaks[mid])
            if (layout(candidate, paint, width, spacing).height <= height) {
                best = candidate
                low = mid + 1
            } else {
                high = mid - 1
            }
        }
        return best
    }

    private const val TRAILING = " \n,;:—–-“"
}
