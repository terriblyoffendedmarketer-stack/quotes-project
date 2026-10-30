package com.marginalia

import android.content.Context
import android.graphics.Typeface
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.LinearLayout
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.RecyclerView

class QuoteCardAdapter(
    private val context: Context,
    private val onSparkToggle: (BankQuote) -> Unit,
    private val onTagClick: (String) -> Unit,
    private val onOpenDaily: (BankQuote) -> Unit
) : RecyclerView.Adapter<QuoteCardAdapter.CardHolder>() {

    private var items: List<BankQuote> = emptyList()
    private var sparkQueue: Set<String> = emptySet()
    private val expandedQuotes = HashSet<String>()

    fun submitList(quotes: List<BankQuote>, sparks: Set<String>) {
        this.items = quotes
        this.sparkQueue = sparks
        notifyDataSetChanged()
    }

    override fun getItemCount(): Int = items.size

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CardHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_quote_card, parent, false)
        return CardHolder(view)
    }

    override fun onBindViewHolder(holder: CardHolder, position: Int) {
        holder.bind(items[position])
    }

    inner class CardHolder(view: View) : RecyclerView.ViewHolder(view) {
        private val horizonView: TextView = view.findViewById(R.id.qc_horizon)
        private val btnSpark: TextView = view.findViewById(R.id.qc_btn_spark)
        private val jobView: TextView = view.findViewById(R.id.qc_job)
        private val quoteView: TextView = view.findViewById(R.id.qc_quote)
        private val attributionView: TextView = view.findViewById(R.id.qc_attribution)
        private val btnNote: TextView = view.findViewById(R.id.qc_btn_note)
        private val noteBody: LinearLayout = view.findViewById(R.id.qc_note_body)
        private val tier1Kicker: TextView = view.findViewById(R.id.qc_tier1_kicker)
        private val tier1Text: TextView = view.findViewById(R.id.qc_tier1_text)
        private val tier2Kicker: TextView = view.findViewById(R.id.qc_tier2_kicker)
        private val tier2Text: TextView = view.findViewById(R.id.qc_tier2_text)
        private val tagsContainer: LinearLayout = view.findViewById(R.id.qc_tags_container)
        private val btnOpenDaily: TextView = view.findViewById(R.id.qc_btn_open_daily)

        fun bind(quote: BankQuote) {
            quoteView.text = "“${quote.quote}”"
            quoteView.textSize = if (quote.quote.length > 220) 16f else 18f

            val yearText = if (quote.year != null) " · ${quote.year}" else ""
            attributionView.text = "— ${quote.author}, ${quote.work}$yearText"

            if (quote.isCard) {
                jobView.visibility = View.VISIBLE
                jobView.text = quote.cardJob ?: ""
                horizonView.text = "✨ HOW-TO: PROSE CRAFT"
                horizonView.setTextColor(ContextCompat.getColor(context, R.color.spark_gold))
                btnSpark.visibility = View.GONE

                val hasLook = !quote.lookCloser.isNullOrEmpty()
                val hasAround = !quote.aroundIt.isNullOrEmpty()
                if (hasLook || hasAround) {
                    btnNote.visibility = View.VISIBLE
                    val isExpanded = expandedQuotes.contains(quote.quote)
                    noteBody.visibility = if (isExpanded) View.VISIBLE else View.GONE
                    btnNote.text = if (isExpanded) "▴ Hide Craft Breakdown" else "▾ Read Craft Breakdown"

                    tier1Kicker.text = "LOOK CLOSER"
                    tier1Text.text = quote.lookCloser ?: ""

                    if (hasAround) {
                        tier2Kicker.visibility = View.VISIBLE
                        tier2Text.visibility = View.VISIBLE
                        tier2Kicker.text = "AROUND IT"
                        tier2Text.text = quote.aroundIt ?: ""
                    } else {
                        tier2Kicker.visibility = View.GONE
                        tier2Text.visibility = View.GONE
                    }

                    btnNote.setOnClickListener {
                        if (expandedQuotes.contains(quote.quote)) {
                            expandedQuotes.remove(quote.quote)
                            noteBody.visibility = View.GONE
                            btnNote.text = "▾ Read Craft Breakdown"
                        } else {
                            expandedQuotes.add(quote.quote)
                            noteBody.visibility = View.VISIBLE
                            btnNote.text = "▴ Hide Craft Breakdown"
                        }
                    }
                } else {
                    btnNote.visibility = View.GONE
                    noteBody.visibility = View.GONE
                }
            } else {
                jobView.visibility = View.GONE
                horizonView.text = "#${quote.horizon}"
                horizonView.setTextColor(ContextCompat.getColor(context, R.color.ink_soft))
                btnSpark.visibility = View.VISIBLE

                val isSaved = sparkQueue.contains(quote.work)
                if (isSaved) {
                    btnSpark.text = "★ Saved"
                    btnSpark.setTextColor(ContextCompat.getColor(context, R.color.spark_gold))
                } else {
                    btnSpark.text = "☆ Read Next"
                    btnSpark.setTextColor(ContextCompat.getColor(context, R.color.ink_soft))
                }

                btnSpark.setOnClickListener {
                    onSparkToggle(quote)
                }

                val paragraphs = quote.explanation.split("\n\n").map { it.trim() }.filter { it.isNotEmpty() }
                if (paragraphs.isNotEmpty()) {
                    btnNote.visibility = View.VISIBLE
                    val isExpanded = expandedQuotes.contains(quote.quote)
                    noteBody.visibility = if (isExpanded) View.VISIBLE else View.GONE
                    btnNote.text = if (isExpanded) "▴ Hide Companion Note" else "▾ Read Companion Note"

                    tier1Kicker.text = "THE PREDICAMENT"
                    tier1Text.text = paragraphs[0]
                    if (paragraphs.size > 1) {
                        tier2Kicker.visibility = View.VISIBLE
                        tier2Text.visibility = View.VISIBLE
                        tier2Kicker.text = "THE MIRROR"
                        tier2Text.text = paragraphs[1]
                    } else {
                        tier2Kicker.visibility = View.GONE
                        tier2Text.visibility = View.GONE
                    }

                    btnNote.setOnClickListener {
                        if (expandedQuotes.contains(quote.quote)) {
                            expandedQuotes.remove(quote.quote)
                            noteBody.visibility = View.GONE
                            btnNote.text = "▾ Read Companion Note"
                        } else {
                            expandedQuotes.add(quote.quote)
                            noteBody.visibility = View.VISIBLE
                            btnNote.text = "▴ Hide Companion Note"
                        }
                    }
                } else {
                    btnNote.visibility = View.GONE
                    noteBody.visibility = View.GONE
                }
            }

            // Tags
            tagsContainer.removeAllViews()
            val allTags = mutableListOf<String>()
            allTags.add(quote.horizon)
            allTags.addAll(quote.tags.filter { it != quote.horizon })

            allTags.forEach { tag ->
                val tagChip = TextView(context).apply {
                    text = "#$tag"
                    textSize = 10.5f
                    typeface = Typeface.MONOSPACE
                    setTextColor(ContextCompat.getColor(context, R.color.ink_soft))
                    setBackgroundResource(R.drawable.tag_chip_bg)
                    setPadding(
                        (8 * context.resources.displayMetrics.density).toInt(),
                        (3 * context.resources.displayMetrics.density).toInt(),
                        (8 * context.resources.displayMetrics.density).toInt(),
                        (3 * context.resources.displayMetrics.density).toInt()
                    )
                    val params = LinearLayout.LayoutParams(
                        ViewGroup.LayoutParams.WRAP_CONTENT,
                        ViewGroup.LayoutParams.WRAP_CONTENT
                    ).apply {
                        marginEnd = (4 * context.resources.displayMetrics.density).toInt()
                    }
                    layoutParams = params
                    setOnClickListener { onTagClick(tag) }
                }
                tagsContainer.addView(tagChip)
            }

            btnOpenDaily.setOnClickListener {
                onOpenDaily(quote)
            }
            itemView.setOnClickListener {
                onOpenDaily(quote)
            }
        }
    }
}
