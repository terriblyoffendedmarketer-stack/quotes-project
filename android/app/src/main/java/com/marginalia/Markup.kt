package com.marginalia

import android.graphics.Typeface
import android.text.SpannableStringBuilder
import android.text.Spanned
import android.text.style.StyleSpan

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

    /** “Author, *Work* · trans. X”, with the work in italics. */
    fun credit(card: Card, withYear: Boolean = false): CharSequence = render(buildString {
        append(card.author).append(", *").append(card.work).append("*")
        card.translator?.let { append(" · trans. ").append(it) }
        if (withYear && card.year > 0) append(" · ").append(card.year)
    })
}
