package com.marginalia

import android.app.Activity
import android.app.AlertDialog
import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.HorizontalScrollView
import android.widget.LinearLayout
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.viewpager2.widget.ViewPager2
import com.marginalia.widget.CardWidgetProvider
import java.time.LocalDate

class MainActivity : Activity() {

    private lateinit var pager: ViewPager2
    private lateinit var tabs: LinearLayout
    private lateinit var dayLabel: TextView
    private lateinit var count: TextView
    private lateinit var stealToggle: TextView
    private lateinit var modeCardsBtn: TextView
    private lateinit var modeBankBtn: TextView
    private lateinit var btnSurprise: TextView
    private lateinit var btnCatalog: TextView
    private lateinit var horizonsScroll: HorizontalScrollView
    private lateinit var horizonsBar: LinearLayout
    private val adapter = SlideAdapter()

    private var currentMode = MODE_CARDS
    private var activeHorizon = "all"
    private var cardIndex = 0
    private var bankIndex = 0
    private var cardSlides: List<Slide> = emptyList()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        pager = findViewById(R.id.pager)
        tabs = findViewById(R.id.tabs)
        dayLabel = findViewById(R.id.day_label)
        count = findViewById(R.id.count)
        stealToggle = findViewById(R.id.steal_toggle)
        modeCardsBtn = findViewById(R.id.mode_cards)
        modeBankBtn = findViewById(R.id.mode_bank)
        btnSurprise = findViewById(R.id.btn_surprise)
        btnCatalog = findViewById(R.id.btn_catalog)
        horizonsScroll = findViewById(R.id.horizons_scroll)
        horizonsBar = findViewById(R.id.horizons_bar)

        findViewById<View>(R.id.deck).clipToOutline = true
        pager.adapter = adapter
        pager.registerOnPageChangeCallback(object : ViewPager2.OnPageChangeCallback() {
            override fun onPageSelected(position: Int) = markTab(position)
        })

        findViewById<View>(R.id.prev).setOnClickListener { step(-1) }
        findViewById<View>(R.id.next).setOnClickListener { step(1) }

        modeCardsBtn.setOnClickListener {
            if (currentMode != MODE_CARDS) {
                currentMode = MODE_CARDS
                render(0)
            }
        }

        modeBankBtn.setOnClickListener {
            if (currentMode != MODE_BANK) {
                currentMode = MODE_BANK
                render(0)
            }
        }

        btnSurprise.setOnClickListener {
            val quotes = QuoteBank.forHorizon(this, activeHorizon)
            if (quotes.isNotEmpty()) {
                bankIndex = (0 until quotes.size).random()
                render(0)
            }
        }

        btnCatalog.setOnClickListener {
            showCatalogDialog()
        }

        dayLabel.setOnClickListener {
            if (currentMode == MODE_CARDS) {
                cardIndex = Cards.todayIndex(this)
            } else {
                activeHorizon = "all"
                bankIndex = QuoteBank.todayIndex(this)
            }
            render(0)
        }

        stealToggle.setOnClickListener {
            Prefs.setShowSteal(this, !Prefs.showSteal(this))
            render(0)
            CardWidgetProvider.refreshAll(this)
        }

        currentMode = savedInstanceState?.getInt(KEY_MODE) ?: MODE_CARDS
        activeHorizon = savedInstanceState?.getString(KEY_HORIZON) ?: "all"
        cardIndex = savedInstanceState?.getInt(KEY_INDEX) ?: Cards.todayIndex(this)
        bankIndex = savedInstanceState?.getInt(KEY_BANK_INDEX) ?: QuoteBank.todayIndex(this)
        
        render(savedInstanceState?.getInt(KEY_SLIDE) ?: 0)
        handle(intent)
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        handle(intent)
    }

    override fun onResume() {
        super.onResume()
        CardWidgetProvider.refreshAll(this)
        val beforeCards = Cards.all(this)
        val beforeBank = QuoteBank.all(this)
        ContentSync.syncIfDue(this) {
            runOnUiThread {
                if (!isFinishing && (Cards.all(this) !== beforeCards || QuoteBank.all(this) !== beforeBank)) {
                    render(pager.currentItem)
                }
            }
        }
    }

    override fun onPause() {
        super.onPause()
        if (currentMode == MODE_CARDS && cardIndex != Cards.todayIndex(this)) {
            Cards.startFrom(this, cardIndex)
            CardWidgetProvider.refreshAll(this)
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putInt(KEY_MODE, currentMode)
        outState.putString(KEY_HORIZON, activeHorizon)
        outState.putInt(KEY_INDEX, cardIndex)
        outState.putInt(KEY_BANK_INDEX, bankIndex)
        outState.putInt(KEY_SLIDE, pager.currentItem)
    }

    private fun handle(intent: Intent?) {
        if (intent == null) return
        if (intent.hasExtra(EXTRA_MODE)) {
            currentMode = intent.getIntExtra(EXTRA_MODE, MODE_CARDS)
        }
        if (intent.hasExtra(EXTRA_CARD)) {
            cardIndex = intent.getIntExtra(EXTRA_CARD, Cards.todayIndex(this))
                .coerceIn(0, Cards.all(this).lastIndex)
        }
        if (intent.hasExtra(EXTRA_BANK_INDEX)) {
            activeHorizon = "all"
            bankIndex = intent.getIntExtra(EXTRA_BANK_INDEX, QuoteBank.todayIndex(this))
                .coerceIn(0, QuoteBank.all(this).lastIndex)
        }
        render(intent.getIntExtra(EXTRA_SLIDE, 0))
    }

    private fun step(delta: Int) {
        if (currentMode == MODE_CARDS) {
            val n = Cards.all(this).size
            cardIndex = Math.floorMod(cardIndex + delta, n)
        } else {
            val quotes = QuoteBank.forHorizon(this, activeHorizon)
            if (quotes.isNotEmpty()) {
                bankIndex = Math.floorMod(bankIndex + delta, quotes.size)
            }
        }
        render(0)
    }

    private fun render(targetSlide: Int) {
        updateModeTabs()

        if (currentMode == MODE_CARDS) {
            renderCardsMode(targetSlide)
        } else {
            renderBankMode(targetSlide)
        }
    }

    private fun updateModeTabs() {
        val activeBg = ContextCompat.getDrawable(this, R.drawable.mode_pill_active)
        val activeTextColor = ContextCompat.getColor(this, R.color.pill_active_text)
        val inactiveTextColor = ContextCompat.getColor(this, R.color.pill_inactive_text)

        if (currentMode == MODE_CARDS) {
            modeCardsBtn.background = activeBg
            modeCardsBtn.setTextColor(activeTextColor)
            modeBankBtn.background = null
            modeBankBtn.setTextColor(inactiveTextColor)

            horizonsScroll.visibility = View.GONE
            btnSurprise.visibility = View.GONE
            btnCatalog.visibility = View.GONE
            stealToggle.visibility = View.VISIBLE
        } else {
            modeCardsBtn.background = null
            modeCardsBtn.setTextColor(inactiveTextColor)
            modeBankBtn.background = activeBg
            modeBankBtn.setTextColor(activeTextColor)

            horizonsScroll.visibility = View.VISIBLE
            btnSurprise.visibility = View.VISIBLE
            btnCatalog.visibility = View.VISIBLE
            stealToggle.visibility = View.GONE

            renderHorizonsBar()
        }
    }

    private fun renderHorizonsBar() {
        horizonsBar.removeAllViews()
        val activeBg = ContextCompat.getDrawable(this, R.drawable.mode_pill_active)
        val activeTextColor = ContextCompat.getColor(this, R.color.pill_active_text)
        val inactiveTextColor = ContextCompat.getColor(this, R.color.ink_soft)

        Horizons.ALL.forEach { h ->
            val count = QuoteBank.countForHorizon(this, h.code)
            val chip = layoutInflater.inflate(R.layout.tab_chip, horizonsBar, false) as TextView
            chip.text = if (h.code == "all") "All ($count)" else "${h.title.split(" ").first()} ($count)"
            
            val isSelected = h.code == activeHorizon
            if (isSelected) {
                chip.background = activeBg
                chip.setTextColor(activeTextColor)
            } else {
                chip.setBackgroundResource(R.drawable.chip_bg)
                chip.setTextColor(inactiveTextColor)
            }

            chip.setOnClickListener {
                if (activeHorizon != h.code) {
                    activeHorizon = h.code
                    bankIndex = 0
                    render(0)
                }
            }
            horizonsBar.addView(chip)
        }
    }

    private fun showCatalogDialog() {
        val items = Horizons.ALL.map { h ->
            val count = QuoteBank.countForHorizon(this, h.code)
            "${h.title} ($count quotes)"
        }.toTypedArray()

        AlertDialog.Builder(this)
            .setTitle("Thematic Horizons")
            .setItems(items) { _, which ->
                val selected = Horizons.ALL[which]
                activeHorizon = selected.code
                bankIndex = 0
                render(0)
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun renderCardsMode(targetSlide: Int) {
        val cards = Cards.all(this)
        cardSlides = Cards.slides(this)
        val day = LocalDate.now().toEpochDay() + cardIndex - Cards.todayIndex(this)
        adapter.showCard(cards[cardIndex], cardSlides, Palette.forDay(day))

        val today = cardIndex == Cards.todayIndex(this)
        dayLabel.text = if (today) getString(R.string.today) else getString(R.string.back_to_today)
        count.text = getString(R.string.count, cardIndex + 1, cards.size)
        stealToggle.text = getString(if (Prefs.showSteal(this)) R.string.hide_steal else R.string.show_steal)

        tabs.removeAllViews()
        cardSlides.forEachIndexed { i, s ->
            val tab = layoutInflater.inflate(R.layout.tab_chip, tabs, false) as TextView
            tab.text = s.label
            tab.setOnClickListener { pager.currentItem = i }
            tabs.addView(tab)
        }
        val target = targetSlide.coerceIn(0, cardSlides.lastIndex)
        pager.setCurrentItem(target, false)
        markTab(target)
    }

    private fun renderBankMode(targetSlide: Int) {
        val quotes = QuoteBank.forHorizon(this, activeHorizon)
        if (quotes.isEmpty()) {
            if (activeHorizon != "all") {
                activeHorizon = "all"
                renderBankMode(targetSlide)
            }
            return
        }
        bankIndex = bankIndex.coerceIn(0, quotes.lastIndex)
        val quote = quotes[bankIndex]
        val currentSlides = QuoteBank.slidesFor(quote)
        adapter.showBank(quote, currentSlides)

        val isGlobalToday = activeHorizon == "all" && bankIndex == QuoteBank.todayIndex(this)
        dayLabel.text = if (isGlobalToday) "TODAY'S SPARK" else "TODAY"
        val horizonTitle = Horizons.titleFor(activeHorizon)
        count.text = "${bankIndex + 1} / ${quotes.size}  ·  $horizonTitle"

        tabs.removeAllViews()
        currentSlides.forEachIndexed { i, s ->
            val tab = layoutInflater.inflate(R.layout.tab_chip, tabs, false) as TextView
            tab.text = s.label
            tab.setOnClickListener { pager.currentItem = i }
            tabs.addView(tab)
        }
        val target = targetSlide.coerceIn(0, currentSlides.lastIndex)
        pager.setCurrentItem(target, false)
        markTab(target)
    }

    private fun markTab(position: Int) {
        for (i in 0 until tabs.childCount) {
            val tab = tabs.getChildAt(i) as TextView
            val active = i == position
            tab.isSelected = active
            tab.setTextColor(ContextCompat.getColor(this, if (active) R.color.ink else R.color.ink_soft))
        }
    }

    companion object {
        const val EXTRA_MODE = "com.marginalia.MODE"
        const val EXTRA_CARD = "com.marginalia.CARD"
        const val EXTRA_BANK_INDEX = "com.marginalia.BANK_INDEX"
        const val EXTRA_SLIDE = "com.marginalia.SLIDE"

        const val MODE_CARDS = 0
        const val MODE_BANK = 1

        private const val KEY_MODE = "current_mode"
        private const val KEY_HORIZON = "active_horizon"
        private const val KEY_INDEX = "card_index"
        private const val KEY_BANK_INDEX = "bank_index"
        private const val KEY_SLIDE = "slide"
    }
}
