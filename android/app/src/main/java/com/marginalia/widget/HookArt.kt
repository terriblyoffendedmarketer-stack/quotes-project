package com.marginalia.widget

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.text.Layout
import android.text.StaticLayout
import android.text.TextPaint
import androidx.core.content.ContextCompat
import androidx.core.content.res.ResourcesCompat
import com.marginalia.R
import kotlin.math.roundToInt

/**
 * Draws the hook ("make the impossible believable") as a picture, in the display font and
 * as large as it fits. Widgets can't reliably use a font bundled with the app, so the text
 * is painted into a bitmap sized to the space the widget has.
 */
object HookArt {

    // Space the rest of the hook slide takes up, in dp: side padding, then the pill,
    // the hint (left out on small widgets) and the footer above and below the title.
    private const val SIDE_DP = 40
    private const val CHROME_DP = 136
    private const val HINT_DP = 23

    fun draw(context: Context, size: WidgetFit.Size, text: String): Bitmap {
        val metrics = context.resources.displayMetrics
        val chrome = if (size.compact) CHROME_DP - HINT_DP else CHROME_DP
        val width = ((size.widthDp - SIDE_DP) * metrics.density).roundToInt().coerceAtLeast(100)
        val height = ((size.heightDp - chrome) * metrics.density).roundToInt().coerceAtLeast(60)

        val paint = TextPaint(TextPaint.ANTI_ALIAS_FLAG).apply {
            typeface = ResourcesCompat.getFont(context, R.font.fraunces_soft_bold)
            color = ContextCompat.getColor(context, R.color.hook_ink)
            letterSpacing = -0.01f
        }

        // The largest size where the text fits the height and no single word has to break.
        val longestWord = text.split(' ').maxByOrNull { it.length } ?: text
        var low = 14f * metrics.density
        var high = 160f * metrics.density
        var layout = layout(text, paint.withSize(low), width)
        repeat(12) {
            val mid = (low + high) / 2
            val p = paint.withSize(mid)
            val candidate = layout(text, p, width)
            // Leave room for a descender (the tail of a "j" or "y") under the last line.
            val fits = candidate.height + p.fontMetrics.descent <= height
            if (fits && p.measureText(longestWord) <= width) {
                low = mid
                layout = candidate
            } else {
                high = mid
            }
        }

        val bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
        val canvas = Canvas(bitmap)
        canvas.translate(0f, ((height - layout.height) / 2f).coerceAtLeast(0f))
        layout.draw(canvas)
        return bitmap
    }

    private fun TextPaint.withSize(size: Float) = TextPaint(this).also { it.textSize = size }

    private fun layout(text: String, paint: TextPaint, width: Int): StaticLayout =
        StaticLayout.Builder.obtain(text, 0, text.length, paint, width)
            .setAlignment(Layout.Alignment.ALIGN_NORMAL)
            .setLineSpacing(0f, 1.0f)
            .setIncludePad(false)
            .setBreakStrategy(Layout.BREAK_STRATEGY_BALANCED)
            .build()
}
