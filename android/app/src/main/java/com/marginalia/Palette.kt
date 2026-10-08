package com.marginalia

import android.content.Context
import android.content.res.Configuration
import java.time.LocalDate
import kotlin.random.Random

/**
 * Each day gets its own colours: one bold colour for the hook and four lighter ones for the
 * slides after it, shuffled so the same slide rarely gets the same colour two days running.
 * The app and the widget pick the same colours for the same day.
 */
object Palette {

    /** Bold hook colours. The hook's cream text works on all of them, in light and dark mode. */
    private val HOOKS = intArrayOf(
        0xFF2D3BE8.toInt(), // cobalt
        0xFFD9402A.toInt(), // tomato
        0xFF1F6B45.toInt(), // forest
        0xFF7A2A7A.toInt(), // plum
        0xFF0F6E74.toInt(), // teal
        0xFFBF4A17.toInt(), // burnt orange
        0xFFC21F6E.toInt(), // magenta
        0xFF5B2BD9.toInt(), // violet
        0xFF14161B.toInt(), // ink
    )

    /** Slide colours for light mode, each paired with the darker one at the same place for dark mode. */
    private val LIGHT = intArrayOf(
        0xFFFFE9A8.toInt(), // butter
        0xFFFFD0E1.toInt(), // bubblegum
        0xFFD2F3B0.toInt(), // lime
        0xFFDCD0FF.toInt(), // lilac
        0xFFFFD6BF.toInt(), // peach
        0xFFCDE7FF.toInt(), // sky
        0xFFC4F0E0.toInt(), // mint
        0xFFF2E3C6.toInt(), // sand
        0xFFFFC2B8.toInt(), // coral
    )
    private val DARK = intArrayOf(
        0xFF5E460C.toInt(), // ochre
        0xFF571F3B.toInt(), // berry
        0xFF1F4527.toInt(), // forest
        0xFF2E2870.toInt(), // indigo
        0xFF6A2E14.toInt(), // rust
        0xFF173A5E.toInt(), // navy
        0xFF0F4A44.toInt(), // teal
        0xFF4A3524.toInt(), // cocoa
        0xFF6B1F2A.toInt(), // wine
    )

    // Butter is too close to the highlighter for "Look closer", which is full of highlights.
    private const val BUTTER = 0

    class Day(val hook: Int, private val light: Map<Slide, Int>, private val dark: Map<Slide, Int>) {
        fun light(slide: Slide) = if (slide == Slide.HOOK) hook else light.getValue(slide)
        fun dark(slide: Slide) = if (slide == Slide.HOOK) hook else dark.getValue(slide)
        fun color(context: Context, slide: Slide) = if (isNight(context)) dark(slide) else light(slide)
    }

    fun today(): Day = forDay(LocalDate.now().toEpochDay())

    fun forDay(day: Long): Day {
        // The hooks go round in a shuffled cycle, so every colour comes up once before any repeats.
        val round = Math.floorDiv(day, HOOKS.size.toLong())
        val order = HOOKS.indices.shuffled(Random(round * 7919 + 17))
        val hook = HOOKS[order[Math.floorMod(day, HOOKS.size.toLong()).toInt()]]

        val picks = LIGHT.indices.shuffled(Random(day * 104729 + 3)).take(4).toMutableList()
        val look = 1 // LINE, LOOK, STEAL, AROUND
        if (picks[look] == BUTTER) picks[look] = picks[0].also { picks[0] = BUTTER }

        val after = listOf(Slide.LINE, Slide.LOOK, Slide.STEAL, Slide.AROUND)
        return Day(
            hook,
            after.zip(picks.map { LIGHT[it] }).toMap(),
            after.zip(picks.map { DARK[it] }).toMap(),
        )
    }

    private fun isNight(context: Context) =
        context.resources.configuration.uiMode and Configuration.UI_MODE_NIGHT_MASK == Configuration.UI_MODE_NIGHT_YES
}
