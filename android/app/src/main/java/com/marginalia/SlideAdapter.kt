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
    private var colors: Palette.Day = Palette.today()

    fun show(card: Card, slides: List<Slide>, colors: Palette.Day) {
        this.card = card
        this.slides = slides
        this.colors = colors
        notifyDataSetChanged()
    }

    override fun getItemCount() = if (card == null) 0 else slides.size

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
        Holder(LayoutInflater.from(parent.context).inflate(R.layout.item_slide, parent, false))

    override fun onBindViewHolder(holder: Holder, position: Int) {
        holder.bind(card ?: return, slides[position], colors)
    }

    class Holder(view: View) : RecyclerView.ViewHolder(view) {
        private val hookPill: TextView = view.findViewById(R.id.hook_pill)
        private val hookTitle: TextView = view.findViewById(R.id.hook_title)
        private val hookAuthor: TextView = view.findViewById(R.id.hook_author)
        private val kicker: TextView = view.findViewById(R.id.slide_kicker)
        private val mini: TextView = view.findViewById(R.id.slide_mini_quote)
        private val body: TextView = view.findViewById(R.id.slide_body)
        private val line: TextView = view.findViewById(R.id.slide_line)
        private val footer: TextView = view.findViewById(R.id.slide_footer)
        private val job: TextView = view.findViewById(R.id.slide_job)
        private val spacerTop: View = view.findViewById(R.id.spacer_top)
        private val spacerBottom: View = view.findViewById(R.id.spacer_bottom)

        fun bind(card: Card, slide: Slide, colors: Palette.Day) {
            val isHook = slide == Slide.HOOK
            val isLine = slide == Slide.LINE
            itemView.setBackgroundColor(colors.color(itemView.context, slide))
            hookPill.setTextColor(colors.hook)
            hookPill.visibility = if (isHook && Slide.hasHowTo(card)) View.VISIBLE else View.GONE
            hookTitle.visibility = if (isHook) View.VISIBLE else View.GONE
            hookAuthor.visibility = hookTitle.visibility
            hookAuthor.text = card.author
            kicker.visibility = if (isHook) View.GONE else View.VISIBLE
            line.visibility = if (isLine) View.VISIBLE else View.GONE
            body.visibility = if (isHook || isLine) View.GONE else View.VISIBLE
            spacerTop.visibility = if (isHook || isLine) View.VISIBLE else View.GONE
            spacerBottom.visibility = spacerTop.visibility
            mini.visibility = if (slide == Slide.LOOK) View.VISIBLE else View.GONE
            footer.visibility = if (isHook) View.GONE else View.VISIBLE
            job.visibility = footer.visibility

            kicker.text = slide.label
            when {
                isHook -> hookTitle.text = slide.body(itemView.context, card)
                isLine -> {
                    line.text = slide.body(itemView.context, card)
                    line.textSize = if (card.quote.length > 220) 21f else 27f
                }
                else -> body.text = slide.body(itemView.context, card)
            }
            if (slide == Slide.LOOK) mini.text = highlighted(card)
            footer.text = Markup.credit(card, withYear = slide == Slide.AROUND)
            job.text = card.job
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
