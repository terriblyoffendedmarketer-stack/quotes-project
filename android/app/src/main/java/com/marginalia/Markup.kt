package com.marginalia

import android.content.Context
import android.graphics.Typeface
import android.text.SpannableStringBuilder
import android.text.Spanned
import android.text.style.BackgroundColorSpan
import android.text.style.ForegroundColorSpan
import android.text.style.StyleSpan
import android.text.style.TypefaceSpan
import androidx.core.content.ContextCompat

/** Card text marks book and magazine titles with *asterisks*; this turns them into italics. */
object Markup {
    private val italic = Regex("""\*([^*]+)\*""")

    fun render(text: String): CharSequence {
        val out = SpannableStringBuilder()
        var last = 0
        for (m in italic.findAll(text)) {
            out.append(text, last, m.range.first)
            val start = out.length
            out.append(m.groupValues[1])
            out.setSpan(StyleSpan(Typeface.ITALIC), start, out.length, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE)
            last = m.range.last + 1
        }
        out.append(text, last, text.length)
        return out
    }

    /**
     * Formatting for the explanation slides, so they carry some of the line's look:
     * the opening sentence is bold, and every phrase quoted from the writer is set in
     * serif italics on a highlighter stripe, matching the marks on the quote itself.
     */
    fun note(context: Context, text: String): CharSequence {
        val out = SpannableStringBuilder(render(text))
        val marker = ContextCompat.getColor(context, R.color.marker)
        val markerInk = ContextCompat.getColor(context, R.color.marker_ink)

        leadEnd(out)?.let { end ->
            out.setSpan(StyleSpan(Typeface.BOLD), 0, end, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE)
        }
        for (m in quoted.findAll(out)) {
            val start = m.range.first + 1
            val end = m.range.last
            if (end <= start) continue
            out.setSpan(TypefaceSpan("serif"), start, end, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE)
            out.setSpan(StyleSpan(Typeface.ITALIC), start, end, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE)
            out.setSpan(BackgroundColorSpan(marker), m.range.first, m.range.last + 1, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE)
            out.setSpan(ForegroundColorSpan(markerInk), m.range.first, m.range.last + 1, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE)
        }
        return out
    }

    private val quoted = Regex("“[^”]{1,80}”")
    private val sentenceEnd = Regex("[.!?](?:”)?\\s")

    /** End of the first sentence, skipping very short fragments like “Mrs.”. */
    private fun leadEnd(text: CharSequence): Int? =
        sentenceEnd.findAll(text).map { it.range.first + 1 }.firstOrNull { it >= 12 }
            ?.let { end -> if (end < text.length && text[end] == '”') end + 1 else end }

    /** “Author, *Work* · trans. X”, with the work in italics. */
    fun credit(card: Card, withYear: Boolean = false): CharSequence = render(buildString {
        append(card.author).append(", *").append(card.work).append("*")
        card.translator?.let { append(" · trans. ").append(it) }
        if (withYear && card.year > 0) append(" · ").append(card.year)
    })
}
