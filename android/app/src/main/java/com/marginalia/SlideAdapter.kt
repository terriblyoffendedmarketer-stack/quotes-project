package com.marginalia

import android.graphics.Color
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
    private var bankQuote: BankQuote? = null
    private var shelfSlides: List<ShelfSlide> = emptyList()
    private var colors: Palette.Day = Palette.today()

    fun showCard(card: Card, slides: List<Slide>, colors: Palette.Day) {
        this.card = card
        this.slides = slides
        this.bankQuote = null
        this.shelfSlides = emptyList()
        this.colors = colors
        notifyDataSetChanged()
    }

    fun showBank(quote: BankQuote, shelfSlides: List<ShelfSlide>) {
        this.card = null
        this.slides = emptyList()
        this.bankQuote = quote
        this.shelfSlides = shelfSlides
        notifyDataSetChanged()
    }

    override fun getItemCount(): Int = when {
        card != null -> slides.size
        bankQuote != null -> shelfSlides.size
        else -> 0
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
        Holder(LayoutInflater.from(parent.context).inflate(R.layout.item_slide, parent, false))

    override fun onBindViewHolder(holder: Holder, position: Int) {
        val c = card
        val bq = bankQuote
        if (c != null && position < slides.size) {
            holder.bindCard(c, slides[position], colors, position, slides.size)
        } else if (bq != null && position < shelfSlides.size) {
            holder.bindBank(bq, shelfSlides[position], position, shelfSlides.size)
        }
    }

    class Holder(view: View) : RecyclerView.ViewHolder(view) {
        private val hookPill: TextView = view.findViewById(R.id.hook_pill)
        private val stepCounter: TextView = view.findViewById(R.id.slide_step_counter)
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

        fun bindCard(card: Card, slide: Slide, colors: Palette.Day, position: Int, total: Int) {
            val isHook = slide == Slide.HOOK
            val isLine = slide == Slide.LINE
            itemView.setBackgroundColor(colors.color(itemView.context, slide))

            stepCounter.visibility = View.VISIBLE
            stepCounter.text = "${position + 1} OF $total"

            if (isHook) {
                hookPill.visibility = if (Slide.hasHowTo(card)) View.VISIBLE else View.GONE
                hookPill.text = "HOW TO"
                hookPill.setBackgroundResource(R.drawable.hook_pill)
                hookPill.setTextColor(colors.hook)
                hookPill.textSize = 12f
                stepCounter.setTextColor(ContextCompat.getColor(itemView.context, R.color.hook_soft))
                kicker.visibility = View.GONE
            } else {
                hookPill.visibility = View.VISIBLE
                hookPill.setBackgroundResource(R.drawable.shelf_badge)
                hookPill.text = slide.label.uppercase()
                hookPill.setTextColor(ContextCompat.getColor(itemView.context, R.color.ink))
                hookPill.textSize = 10.5f
                stepCounter.setTextColor(ContextCompat.getColor(itemView.context, R.color.ink_soft))
                kicker.visibility = View.GONE
            }

            hookTitle.visibility = if (isHook) View.VISIBLE else View.GONE
            hookAuthor.visibility = hookTitle.visibility
            hookAuthor.text = card.author
            line.visibility = if (isLine) View.VISIBLE else View.GONE
            body.visibility = if (isHook || isLine) View.GONE else View.VISIBLE
            spacerTop.visibility = View.VISIBLE
            spacerBottom.visibility = View.VISIBLE
            mini.visibility = if (slide == Slide.LOOK) View.VISIBLE else View.GONE
            footer.visibility = if (isHook) View.GONE else View.VISIBLE
            job.visibility = footer.visibility

            when {
                isHook -> hookTitle.text = slide.body(itemView.context, card)
                isLine -> {
                    line.text = slide.body(itemView.context, card)
                    val len = card.quote.length
                    line.textSize = when {
                        len < 80 -> 28f
                        len < 180 -> 24f
                        len < 280 -> 20f
                        else -> 17f
                    }
                }
                else -> body.text = slide.body(itemView.context, card)
            }
            if (slide == Slide.LOOK) mini.text = highlighted(card)
            footer.text = Markup.credit(card, withYear = slide == Slide.AROUND)
            job.text = card.job
        }

        fun bindBank(quote: BankQuote, shelfSlide: ShelfSlide, position: Int, total: Int) {
            val isLine = shelfSlide.isLine
            val context = itemView.context

            val bg = ContextCompat.getColor(context, R.color.sheet)
            itemView.setBackgroundColor(bg)

            hookPill.visibility = View.VISIBLE
            hookPill.setBackgroundResource(R.drawable.shelf_badge)
            hookPill.text = shelfSlide.pill
            hookPill.setTextColor(ContextCompat.getColor(context, R.color.shelf_badge_text))
            hookPill.textSize = 10.5f

            stepCounter.visibility = View.VISIBLE
            stepCounter.text = "${position + 1} OF $total"
            stepCounter.setTextColor(ContextCompat.getColor(context, R.color.ink_soft))

            hookTitle.visibility = View.GONE
            hookAuthor.visibility = View.GONE
            mini.visibility = View.GONE

            kicker.visibility = View.VISIBLE
            kicker.text = quote.work.uppercase()
            kicker.setTextColor(ContextCompat.getColor(context, R.color.ink_soft))

            spacerTop.visibility = View.VISIBLE
            spacerBottom.visibility = View.VISIBLE

            line.visibility = if (isLine) View.VISIBLE else View.GONE
            body.visibility = if (isLine) View.GONE else View.VISIBLE

            line.setTextColor(ContextCompat.getColor(context, R.color.ink))
            body.setTextColor(ContextCompat.getColor(context, R.color.ink))

            if (isLine) {
                line.text = "“${shelfSlide.text}”"
                val len = shelfSlide.text.length
                line.textSize = when {
                    len < 80 -> 28f
                    len < 180 -> 24f
                    len < 280 -> 20f
                    else -> 17f
                }
            } else {
                body.text = shelfSlide.text
                body.textSize = 17f
            }

            footer.visibility = View.VISIBLE
            footer.setTextColor(ContextCompat.getColor(context, R.color.ink_soft))
            val yearStr = if (quote.year != null) " · ${quote.year}" else ""
            footer.text = "${quote.author}, ${quote.work}$yearStr"

            job.visibility = View.VISIBLE
            job.setTextColor(ContextCompat.getColor(context, R.color.ink_soft))
            val tagPrefix = "#${Horizons.titleFor(quote.horizon)}"
            job.text = if (quote.tags.isNotEmpty()) "$tagPrefix  ·  " + quote.tags.joinToString("  #", prefix = "#") else tagPrefix
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
