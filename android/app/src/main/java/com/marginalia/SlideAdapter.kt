package com.marginalia

import android.text.SpannableString
import android.text.Spanned
import android.text.style.BackgroundColorSpan
import android.text.style.ForegroundColorSpan
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.RecyclerView

class SlideAdapter : RecyclerView.Adapter<SlideAdapter.Holder>() {

    private var card: Card? = null
    private var slides: List<Slide> = emptyList()

    fun show(card: Card, slides: List<Slide>) {
        this.card = card
        this.slides = slides
        notifyDataSetChanged()
    }

    override fun getItemCount() = if (card == null) 0 else slides.size

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
        Holder(LayoutInflater.from(parent.context).inflate(R.layout.item_slide, parent, false))

    override fun onBindViewHolder(holder: Holder, position: Int) {
        holder.bind(card ?: return, slides[position])
    }

    class Holder(view: View) : RecyclerView.ViewHolder(view) {
        private val kicker: TextView = view.findViewById(R.id.slide_kicker)
        private val mini: TextView = view.findViewById(R.id.slide_mini_quote)
        private val body: TextView = view.findViewById(R.id.slide_body)
        private val line: TextView = view.findViewById(R.id.slide_line)
        private val footer: TextView = view.findViewById(R.id.slide_footer)
        private val spacerTop: View = view.findViewById(R.id.spacer_top)
        private val spacerBottom: View = view.findViewById(R.id.spacer_bottom)

        fun bind(card: Card, slide: Slide) {
            val isLine = slide == Slide.LINE
            kicker.text = slide.kicker(card)
            line.visibility = if (isLine) View.VISIBLE else View.GONE
            body.visibility = if (isLine) View.GONE else View.VISIBLE
            spacerTop.visibility = if (isLine) View.VISIBLE else View.GONE
            spacerBottom.visibility = spacerTop.visibility
            mini.visibility = if (slide == Slide.LOOK) View.VISIBLE else View.GONE

            if (isLine) {
                line.text = slide.body(card)
                line.textSize = if (card.quote.length > 220) 21f else 27f
            } else {
                body.text = slide.body(card)
            }
            if (slide == Slide.LOOK) mini.text = highlighted(card)
            footer.text = Markup.credit(card, withYear = slide == Slide.AROUND)
        }

        private fun highlighted(card: Card): CharSequence {
            val context = itemView.context
            val marker = ContextCompat.getColor(context, R.color.marker)
            val markerInk = ContextCompat.getColor(context, R.color.marker_ink)
            val text = SpannableString(card.quote)
            for (phrase in card.highlights) {
                val start = card.quote.indexOf(phrase)
                if (start < 0) continue
                val end = start + phrase.length
                text.setSpan(BackgroundColorSpan(marker), start, end, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE)
                text.setSpan(ForegroundColorSpan(markerInk), start, end, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE)
            }
            return text
        }
    }
}
