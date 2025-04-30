***************************************************
Playoffs: The Odds of Coming Back Or Closing It Out
***************************************************


.. _comeback-odds-occurence-rate-versus-a-series-deficit:

Comeback Odds / Occurrence Rate Versus A Series Deficit
=======================================================

With some slight modification to how the plotting tool works, we can look at the odds
of coming back from a given series deficit:

.. raw:: html

    <div id="playoff_series/playoff_series_all_time" class="nbacd-chart"></div>

Since the 1996 season only 8 teams out of the 167 series where someone fell down 1-3
have come back, leading to about a 5% chance of a series comeback if you fall down 1-3.
Also notable: teams that fall down 0-1 only have about a 1 in 4 chance of winning.  And
we're still waiting for someone to comeback from a 0-3 hole.

We can also plot the occurrence rates of each series score:

.. raw:: html

    <div id="playoff_series/playoff_series_all_time_occurs" class="nbacd-chart"></div>

This shows that 17% of series have been 4-0 sweeps. Also surprising, in nearly 60% of
series teams fall down 0-2 and, using the chart above, only have a 10% chance of coming
back (i.e., most series are over quickly -- which isn't surprising when you think of
the mismatches in the beginning rounds).


.. _comparing-old-school-versus-modern-eras:

Comparing Old School Versus Modern Eras
=======================================

There's not much here, but because it was easy to do I plotted the same charts
:doc:`comparing the eras </analysis/20_is_new_18>`:

.. raw:: html

    <div id="playoff_series/playoff_series_old_school_versus_modern" class="nbacd-chart"></div>

.. raw:: html

    <div id="playoff_series/playoff_series_old_school_versus_modern_occurs" class="nbacd-chart"></div>

This shows that coming back from 0-2 now (15.25%) is about twice as likely as in the
past (7.64%). There's not a ton of data points here, so some or most of this could just
be noise, but that data is presented here for one to speculate.


.. _notes-on-win--plot:

Notes on Win % Plot
===================

When 'Win % Versus Series Score' is plotted on a `normal probability plot
<https://en.wikipedia.org/wiki/Normal_probability_plot>`_, the data is fairly normally
distributed (with really only the 0-1 chances throwing off the normality).  This is
just more of curiosity than anything else.  I did this by using this mapping:

.. list-table:: Series Score Mapping
   :header-rows: 1
   :widths: auto

   * - Series Score
     - Integer Value
   * - 0-3  # Down 3 games
     - -6
   * - 1-3  # Down 2 games
     - -5
   * - 0-2  # Down 2 games
     - -4
   * - 2-3  # Down 1 game
     - -3
   * - 1-2  # Down 1 game
     - -2
   * - 0-1  # Down 1 game
     - -1
   * - Tied
     - 0
