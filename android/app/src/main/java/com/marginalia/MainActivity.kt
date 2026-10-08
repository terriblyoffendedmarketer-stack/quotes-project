package com.marginalia

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.view.View
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
    private val adapter = SlideAdapter()

    private var index = 0
    private var slides: List<Slide> = emptyList()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        pager = findViewById(R.id.pager)
        tabs = findViewById(R.id.tabs)
        dayLabel = findViewById(R.id.day_label)
        count = findViewById(R.id.count)
        stealToggle = findViewById(R.id.steal_toggle)

        // Slides carry their own colours, so clip them to the deck's rounded corners.
        findViewById<View>(R.id.deck).clipToOutline = true
        pager.adapter = adapter
        pager.registerOnPageChangeCallback(object : ViewPager2.OnPageChangeCallback() {
            override fun onPageSelected(position: Int) = markTab(position)
        })

        findViewById<View>(R.id.prev).setOnClickListener { step(-1) }
        findViewById<View>(R.id.next).setOnClickListener { step(1) }
        dayLabel.setOnClickListener { index = Cards.todayIndex(this); render(0) }
        stealToggle.setOnClickListener {
            Prefs.setShowSteal(this, !Prefs.showSteal(this))
            render(0)
            CardWidgetProvider.refreshAll(this)
        }

        index = savedInstanceState?.getInt(KEY_INDEX) ?: Cards.todayIndex(this)
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
        // Pick up new or edited cards from GitHub, then redraw if anything arrived.
        val before = Cards.all(this)
        ContentSync.syncIfDue(this) {
            runOnUiThread {
                if (!isFinishing && Cards.all(this) !== before) {
                    index = index.coerceIn(0, Cards.all(this).lastIndex)
                    render(pager.currentItem)
                }
            }
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putInt(KEY_INDEX, index)
        outState.putInt(KEY_SLIDE, pager.currentItem)
    }

    /** A tap on the widget opens the card and slide that was tapped. */
    private fun handle(intent: Intent?) {
        if (intent == null || !intent.hasExtra(EXTRA_CARD)) return
        index = intent.getIntExtra(EXTRA_CARD, Cards.todayIndex(this))
            .coerceIn(0, Cards.all(this).lastIndex)
        render(intent.getIntExtra(EXTRA_SLIDE, 0))
        intent.removeExtra(EXTRA_CARD)
    }

    private fun step(delta: Int) {
        val n = Cards.all(this).size
        index = Math.floorMod(index + delta, n)
        render(0)
    }

    private fun render(slide: Int) {
        val cards = Cards.all(this)
        slides = Cards.slides(this)
        // Each card in the colours of the day it's shown on, so browsing looks like the days do.
        val day = LocalDate.now().toEpochDay() + index - Cards.todayIndex(this)
        adapter.show(cards[index], slides, Palette.forDay(day))

        val today = index == Cards.todayIndex(this)
        dayLabel.text = if (today) getString(R.string.today) else getString(R.string.back_to_today)
        count.text = getString(R.string.count, index + 1, cards.size)
        stealToggle.text = getString(if (Prefs.showSteal(this)) R.string.hide_steal else R.string.show_steal)

        tabs.removeAllViews()
        slides.forEachIndexed { i, s ->
            val tab = layoutInflater.inflate(R.layout.tab_chip, tabs, false) as TextView
            tab.text = s.label
            tab.setOnClickListener { pager.currentItem = i }
            tabs.addView(tab)
        }
        val target = slide.coerceIn(0, slides.lastIndex)
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
        const val EXTRA_CARD = "com.marginalia.CARD"
        const val EXTRA_SLIDE = "com.marginalia.SLIDE"
        private const val KEY_INDEX = "index"
        private const val KEY_SLIDE = "slide"
    }
}
