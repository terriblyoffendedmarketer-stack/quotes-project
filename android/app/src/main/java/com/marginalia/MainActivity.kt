package com.marginalia

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.widget.EditText
import android.widget.HorizontalScrollView
import android.widget.LinearLayout
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.viewpager2.widget.ViewPager2
import com.marginalia.widget.CardWidgetProvider
import java.time.LocalDate

class MainActivity : Activity() {

    // Studio Header & Main Tabs
    private lateinit var tabDaily: TextView
    private lateinit var tabLibrary: TextView
    private lateinit var viewDaily: LinearLayout
    private lateinit var viewLibrary: LinearLayout

    // Daily View elements
    private lateinit var pager: ViewPager2
    private lateinit var tabs: LinearLayout
    private lateinit var tabsScroll: HorizontalScrollView
    private lateinit var dayLabel: TextView
    private lateinit var count: TextView
    private lateinit var stealToggle: TextView
    private lateinit var modeCardsBtn: TextView
    private lateinit var modeBankBtn: TextView
    private lateinit var btnSurprise: TextView
    private lateinit var horizonsScroll: HorizontalScrollView
    private lateinit var horizonsBar: LinearLayout
    private val slideAdapter = SlideAdapter()

    // Library View elements
    private lateinit var libSearch: EditText
    private lateinit var libBtnSurprise: TextView
    private lateinit var libHorizonsBar: LinearLayout
    private lateinit var libMatchCount: TextView
    private lateinit var libActiveTagContainer: LinearLayout
    private lateinit var libActiveTagText: TextView
    private lateinit var libBtnClearTag: TextView
    private lateinit var libBtnSparkQueue: TextView
    private lateinit var libRecycler: RecyclerView
    private lateinit var libAdapter: QuoteCardAdapter

    // State
    private var currentStudioTab = TAB_DAILY
    private var currentMode = MODE_CARDS
    private var activeHorizon = "all"
    private var cardIndex = 0
    private var bankIndex = 0
    private var cardSlides: List<Slide> = emptyList()

    // Library State
    private var libQuery = ""
    private var libActiveHorizon = "all"
    private var libActiveTag: String? = null
    private var libShowingSparkQueue = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Studio tabs
        tabDaily = findViewById(R.id.tab_daily)
        tabLibrary = findViewById(R.id.tab_library)
        viewDaily = findViewById(R.id.view_daily)
        viewLibrary = findViewById(R.id.view_library)

        // Daily View
        pager = findViewById(R.id.pager)
        tabs = findViewById(R.id.tabs)
        tabsScroll = findViewById(R.id.tabs_scroll)
        dayLabel = findViewById(R.id.day_label)
        count = findViewById(R.id.count)
        stealToggle = findViewById(R.id.steal_toggle)
        modeCardsBtn = findViewById(R.id.mode_cards)
        modeBankBtn = findViewById(R.id.mode_bank)
        btnSurprise = findViewById(R.id.btn_surprise)
        horizonsScroll = findViewById(R.id.horizons_scroll)
        horizonsBar = findViewById(R.id.horizons_bar)

        // Library View
        libSearch = findViewById(R.id.lib_search)
        libBtnSurprise = findViewById(R.id.lib_btn_surprise)
        libHorizonsBar = findViewById(R.id.lib_horizons_bar)
        libMatchCount = findViewById(R.id.lib_match_count)
        libActiveTagContainer = findViewById(R.id.lib_active_tag_container)
        libActiveTagText = findViewById(R.id.lib_active_tag_text)
        libBtnClearTag = findViewById(R.id.lib_btn_clear_tag)
        libBtnSparkQueue = findViewById(R.id.lib_btn_spark_queue)
        libRecycler = findViewById(R.id.lib_recycler)

        findViewById<View>(R.id.deck).clipToOutline = true
        pager.adapter = slideAdapter
        pager.registerOnPageChangeCallback(object : ViewPager2.OnPageChangeCallback() {
            override fun onPageSelected(position: Int) = markTab(position)
        })

        findViewById<View>(R.id.prev).setOnClickListener { step(-1) }
        findViewById<View>(R.id.next).setOnClickListener { step(1) }

        // Main Studio Tabs listener
        tabDaily.setOnClickListener { switchStudioTab(TAB_DAILY) }
        tabLibrary.setOnClickListener { switchStudioTab(TAB_LIBRARY) }

        // Daily mode toggle
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

        setupLibraryView()

        currentStudioTab = savedInstanceState?.getInt(KEY_STUDIO_TAB) ?: TAB_DAILY
        currentMode = savedInstanceState?.getInt(KEY_MODE) ?: Prefs.todayMode(this)
        activeHorizon = savedInstanceState?.getString(KEY_HORIZON) ?: "all"
        cardIndex = savedInstanceState?.getInt(KEY_INDEX) ?: Cards.todayIndex(this)
        bankIndex = savedInstanceState?.getInt(KEY_BANK_INDEX) ?: QuoteBank.todayIndex(this)

        render(savedInstanceState?.getInt(KEY_SLIDE) ?: 0)
        switchStudioTab(currentStudioTab)
        handle(intent)
    }

    private fun setupLibraryView() {
        libAdapter = QuoteCardAdapter(
            context = this,
            onSparkToggle = { quote ->
                Prefs.toggleSpark(this, quote.work)
                updateLibraryList()
            },
            onTagClick = { tag ->
                libActiveTag = tag
                updateLibraryList()
            },
            onOpenDaily = { quote ->
                // Switch to Daily tab and open this quote directly in the swipeable deck
                currentMode = MODE_BANK
                activeHorizon = "all"
                val allQuotes = QuoteBank.forHorizon(this, "all")
                val foundIdx = allQuotes.indexOfFirst { it.quote == quote.quote }
                if (foundIdx >= 0) {
                    bankIndex = foundIdx
                }
                switchStudioTab(TAB_DAILY)
                render(0)
            }
        )

        libRecycler.layoutManager = LinearLayoutManager(this)
        libRecycler.adapter = libAdapter

        libSearch.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                libQuery = s?.toString()?.trim() ?: ""
                updateLibraryList()
            }
            override fun afterTextChanged(s: Editable?) {}
        })

        libBtnSurprise.setOnClickListener {
            val allQuotes = QuoteBank.all(this)
            if (allQuotes.isNotEmpty()) {
                libQuery = ""
                libSearch.setText("")
                libActiveTag = null
                libActiveHorizon = "all"
                libShowingSparkQueue = false
                renderLibHorizonsBar()
                val rand = (0 until allQuotes.size).random()
                updateLibraryList()
                libRecycler.scrollToPosition(rand)
            }
        }

        libBtnClearTag.setOnClickListener {
            libActiveTag = null
            updateLibraryList()
        }

        libBtnSparkQueue.setOnClickListener {
            libShowingSparkQueue = !libShowingSparkQueue
            updateLibraryList()
        }

        renderLibHorizonsBar()
        updateLibraryList()
    }

    private fun switchStudioTab(tab: Int) {
        currentStudioTab = tab
        val activeBg = ContextCompat.getDrawable(this, R.drawable.mode_pill_active)
        val activeTextColor = ContextCompat.getColor(this, R.color.pill_active_text)
        val inactiveTextColor = ContextCompat.getColor(this, R.color.pill_inactive_text)

        if (tab == TAB_DAILY) {
            tabDaily.background = activeBg
            tabDaily.setTextColor(activeTextColor)
            tabLibrary.background = null
            tabLibrary.setTextColor(inactiveTextColor)

            viewDaily.visibility = View.VISIBLE
            viewLibrary.visibility = View.GONE
        } else {
            tabDaily.background = null
            tabDaily.setTextColor(inactiveTextColor)
            tabLibrary.background = activeBg
            tabLibrary.setTextColor(activeTextColor)

            viewDaily.visibility = View.GONE
            viewLibrary.visibility = View.VISIBLE
            updateLibraryList()
        }
    }

    private fun renderLibHorizonsBar() {
        libHorizonsBar.removeAllViews()
        val activeBg = ContextCompat.getDrawable(this, R.drawable.mode_pill_active)
        val activeTextColor = ContextCompat.getColor(this, R.color.pill_active_text)
        val inactiveTextColor = ContextCompat.getColor(this, R.color.ink_soft)

        Horizons.ALL.forEach { h ->
            val count = QuoteBank.countForHorizon(this, h.code)
            val chip = layoutInflater.inflate(R.layout.tab_chip, libHorizonsBar, false) as TextView
            chip.text = if (h.code == "all") "All ($count)" else "${h.title} ($count)"

            val isSelected = h.code == libActiveHorizon
            if (isSelected) {
                chip.background = activeBg
                chip.setTextColor(activeTextColor)
            } else {
                chip.setBackgroundResource(R.drawable.chip_bg)
                chip.setTextColor(inactiveTextColor)
            }

            chip.setOnClickListener {
                if (libActiveHorizon != h.code) {
                    libActiveHorizon = h.code
                    renderLibHorizonsBar()
                    updateLibraryList()
                }
            }
            libHorizonsBar.addView(chip)
        }
    }

    private fun updateLibraryList() {
        val allQuotes = QuoteBank.all(this)
        val sparks = Prefs.sparkQueue(this)

        val filtered = allQuotes.filter { q ->
            if (libShowingSparkQueue && !sparks.contains(q.work)) return@filter false
            if (libActiveHorizon != "all" && q.horizon != libActiveHorizon) return@filter false
            if (libActiveTag != null) {
                val matchHorizon = q.horizon.equals(libActiveTag, ignoreCase = true)
                val matchTag = q.tags.any { it.equals(libActiveTag, ignoreCase = true) }
                if (!matchHorizon && !matchTag) return@filter false
            }
            if (libQuery.isNotEmpty()) {
                val haystack = "${q.quote} ${q.author} ${q.work} ${q.explanation} ${q.tags.joinToString(" ")}".lowercase()
                if (!haystack.contains(libQuery.lowercase())) return@filter false
            }
            true
        }

        libAdapter.submitList(filtered, sparks)

        val distinctBooks = filtered.map { it.work }.toSet().size
        libMatchCount.text = "${filtered.size} quotes across $distinctBooks books"

        if (libActiveTag != null) {
            libActiveTagContainer.visibility = View.VISIBLE
            libActiveTagText.text = "#$libActiveTag"
        } else {
            libActiveTagContainer.visibility = View.GONE
        }

        libBtnSparkQueue.text = "✨ Read Next (${sparks.size})"
        if (libShowingSparkQueue) {
            libBtnSparkQueue.setBackgroundResource(R.drawable.mode_pill_active)
            libBtnSparkQueue.setTextColor(ContextCompat.getColor(this, R.color.pill_active_text))
        } else {
            libBtnSparkQueue.setBackgroundResource(R.drawable.chip_button_bg)
            libBtnSparkQueue.setTextColor(ContextCompat.getColor(this, R.color.spark_gold))
        }
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
                    updateLibraryList()
                }
            }
        }
    }

    override fun onPause() {
        super.onPause()
        if (currentMode == MODE_CARDS && cardIndex != Cards.todayIndex(this)) {
            Cards.startFrom(this, cardIndex)
        } else if (currentMode == MODE_BANK && bankIndex != QuoteBank.todayIndex(this)) {
            QuoteBank.startFrom(this, bankIndex)
        }
        Prefs.setMode(this, currentMode)
        CardWidgetProvider.refreshAll(this)
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putInt(KEY_STUDIO_TAB, currentStudioTab)
        outState.putInt(KEY_MODE, currentMode)
        outState.putString(KEY_HORIZON, activeHorizon)
        outState.putInt(KEY_INDEX, cardIndex)
        outState.putInt(KEY_BANK_INDEX, bankIndex)
        outState.putInt(KEY_SLIDE, pager.currentItem)
    }

    private fun handle(intent: Intent?) {
        if (intent == null) return
        var shouldSwitchToDaily = false
        if (intent.hasExtra(EXTRA_MODE)) {
            currentMode = intent.getIntExtra(EXTRA_MODE, MODE_CARDS)
            shouldSwitchToDaily = true
        }
        if (intent.hasExtra(EXTRA_CARD)) {
            cardIndex = intent.getIntExtra(EXTRA_CARD, Cards.todayIndex(this))
                .coerceIn(0, Cards.all(this).lastIndex)
            shouldSwitchToDaily = true
        }
        if (intent.hasExtra(EXTRA_BANK_INDEX)) {
            activeHorizon = "all"
            bankIndex = intent.getIntExtra(EXTRA_BANK_INDEX, QuoteBank.todayIndex(this))
                .coerceIn(0, QuoteBank.all(this).lastIndex)
            shouldSwitchToDaily = true
        }
        if (shouldSwitchToDaily) {
            switchStudioTab(TAB_DAILY)
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
            stealToggle.visibility = View.VISIBLE
        } else {
            modeCardsBtn.background = null
            modeCardsBtn.setTextColor(inactiveTextColor)
            modeBankBtn.background = activeBg
            modeBankBtn.setTextColor(activeTextColor)

            horizonsScroll.visibility = View.VISIBLE
            btnSurprise.visibility = View.VISIBLE
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

    private fun renderCardsMode(targetSlide: Int) {
        val cards = Cards.all(this)
        cardSlides = Cards.slides(this)
        val day = LocalDate.now().toEpochDay() + cardIndex - Cards.todayIndex(this)
        slideAdapter.showCard(cards[cardIndex], cardSlides, Palette.forDay(day))

        val today = cardIndex == Cards.todayIndex(this)
        dayLabel.text = if (today) getString(R.string.today) else getString(R.string.back_to_today)
        count.text = getString(R.string.count, cardIndex + 1, cards.size)
        stealToggle.text = getString(if (Prefs.showSteal(this)) R.string.hide_steal else R.string.show_steal)

        tabs.removeAllViews()
        tabsScroll.scrollTo(0, 0)
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
        slideAdapter.showBank(quote, currentSlides)

        val isGlobalToday = activeHorizon == "all" && bankIndex == QuoteBank.todayIndex(this)
        dayLabel.text = if (isGlobalToday) "TODAY'S SPARK" else "TODAY"
        val horizonTitle = Horizons.titleFor(activeHorizon)
        count.text = "${bankIndex + 1} / ${quotes.size}  ·  $horizonTitle"

        tabs.removeAllViews()
        tabsScroll.scrollTo(0, 0)
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
        tabs.post {
            val selectedTab = tabs.getChildAt(position) ?: return@post
            val targetScrollX = selectedTab.left - (tabsScroll.width - selectedTab.width) / 2
            tabsScroll.smoothScrollTo(targetScrollX.coerceAtLeast(0), 0)
        }
    }

    companion object {
        const val TAB_DAILY = 0
        const val TAB_LIBRARY = 1

        const val EXTRA_MODE = "com.marginalia.MODE"
        const val EXTRA_CARD = "com.marginalia.CARD"
        const val EXTRA_BANK_INDEX = "com.marginalia.BANK_INDEX"
        const val EXTRA_SLIDE = "com.marginalia.SLIDE"

        const val MODE_CARDS = 0
        const val MODE_BANK = 1

        private const val KEY_STUDIO_TAB = "current_studio_tab"
        private const val KEY_MODE = "current_mode"
        private const val KEY_HORIZON = "active_horizon"
        private const val KEY_INDEX = "card_index"
        private const val KEY_BANK_INDEX = "bank_index"
        private const val KEY_SLIDE = "slide"
    }
}
