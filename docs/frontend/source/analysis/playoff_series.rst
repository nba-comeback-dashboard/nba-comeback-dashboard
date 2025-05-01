***************************************************
Playoffs: The Odds of Coming Back Or Closing It Out
***************************************************


.. _comeback-odds-occurrence-rate-versus-a-series-deficit:

Comeback Odds and Occurrence Rate of a Seven-Game Series Deficit
================================================================

We can also look at the odds of coming back from a series deficit :doc:`plotted on a
normal probability plot </analysis/methodology_forming_the_plot_trend_lines>` and look
at a lot of playoff series statistics with just a few charts.

First, let's look at the odds of coming back and winning a best-of-seven series versus
series deficit since 1996 (note, 1st round series before 2003 -- which were 5-game
series -- are ignored):

.. raw:: html

    <div id="playoff_series/playoff_series_all_time" class="nbacd-chart"></div>

Since the 1996 season, only 8 teams out of the 167 series where someone fell down 1-3
have come back, leading to about a 5% chance of a series comeback if you fall down 1-3.
Also notable: teams that fall down 0-1 only have about a 1 in 4 chance of winning. And
we're still waiting for someone to come back from a 0-3 hole.

We can also plot the occurrence rates of each series score:

.. raw:: html

    <div id="playoff_series/playoff_series_all_time_occurs" class="nbacd-chart"></div>


Note, these charts can be mirrored -- so if you are up 3-2 in the series, you have
about an 82% chance of closing it out (100% - 18%). And the occurrence rate of 3-2
series is equal to the occurrence rate of 2-3 series - they happen about 54% of the
time.

.. _garbage-time-series:

How Many "Garbage Time" Series?
===============================
.  Among other things, the charts above show that:

* 18% of series have been 4-0 sweeps and 28% have been 4-1 closeouts, leading
  to 170 out of 372 or 46% of series being lopsided affairs. With the large difference
  in team strength in the first rounds, this may be expected. But :ref:`this stat holds
  up over most rounds <odds-and-occurrence-by-playoff-round>` with 12 out of the last
  28 Finals (or 43%) being either 4-0 or 4-1 affairs.

* In 28% of series, teams fall into a 0-3 hole, a virtual playoff death sentence.

* In nearly 60% of all series, a team falls down 0-2. And despite this
  supposedly being the normal state of affairs of just holding home court advantage,
  it's a very bad place to be: using the chart above, you only have about a 10% chance
  of coming back if you fall down 0-2. Which means the majority of series are not very
  competitive (although thankfully, this may not be apparent without the benefit of
  hindsight).

On the level, this is probably to be expected in any competitive sport, with roughly
half the matches being not that close (with the stats about the Finals being a little
unexpected). And on the happy side, this should be contrasted with the fact that:

* 54% of series have the losing side getting at least 2 wins.

* About 60% of series do get tied up at some point (individual tied series scores also
  shown).

With so many 0-2 starts and so many tied series, how can we square this? Well, of those
216 0-2 starts, 65 of those teams have come back and evened up the series at some
point, or about 35% of the time.

However, there have only been 21 teams that have come back from a 0-2 hole (and of
course tied the series up at some point). So that means that even if a team ties up the
series, they still only have a 21 out of 65 or a 32% chance of winning. I would have
thought that if a team fell down 0-2 and then tied it up, momentum would have been on
their side and at least gotten to a 50% win rate, but it turns out that they are still
behind in the odds.

Here's a list of the 21 teams that have pulled off this somewhat rare feat:

.. include:: playoff_series_table.rst



.. _how-big-a-deal-is-home-court-advantage:

How Big Is the Home Court Advantage?
====================================

In short, very large. Out of the 372 7-game series so far, the team with home court
advantage has won 275 of them or about 73.9% (the majority of this benefit owing to
team strength and not the actual home court advantage). And this advantage persists
even when facing a series deficit. Looking at the odds of coming back from various
deficits for @Home (has home court advantage) versus @Away (does not):

.. raw:: html

    <div id="playoff_series/playoff_series_all_time_home_v_away" class="nbacd-chart"></div>

Here, a team that goes down 0-1 at home still has about a 53% chance of winning the
series. And a team with home court advantage has about an 11% chance of coming back
from a 1-3 deficit, much better than the overall 5% average and about the same odds as
the team without home court advantage coming back from a 2-3 deficit (12.8%).


.. _odds-and-occurrence-by-playoff-round:

Odds and Occurrence by Playoff Round
====================================

1st and 2nd Round
-----------------

We can now compare the 1st and 2nd rounds over the same time period:

.. raw:: html

    <div id="playoff_series/playoff_series_all_time_by_round_1_2" class="nbacd-chart"></div>

.. raw:: html

    <div id="playoff_series/playoff_series_all_time_by_round_1_2_occurs" class="nbacd-chart"></div>

Conference Finals and Finals
----------------------------

We can also now compare the Conference Finals versus the Finals over the same time
period:

.. raw:: html

    <div id="playoff_series/playoff_series_all_time_by_round_3_4" class="nbacd-chart"></div>

.. raw:: html

    <div id="playoff_series/playoff_series_all_time_by_round_3_4_occurs" class="nbacd-chart"></div>

Here:
 
* An amazing 18% of the Conference Finals since the 1996-1997 season have been sweeps.

* 3 Finals out of the last 28 -- or over 10% -- have also been sweeps.

* Only 4 of the 28 Finals have gone 7 games.

* And even for the Conference Finals, in nearly 60% of series, a team falls down 0-2
  and has only a 12% chance of coming back to win. And it's not that much better for
  the Finals. It is surprising that this stat does not change much as you compare the
  different rounds of the playoffs.



.. _comparing-old-school-versus-modern-eras:

Comparing Old School Versus Modern Eras
=======================================

There's not much here, but because it was easy to do, I plotted the same charts
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
distributed (with really only the 0-1 chances throwing off the normality). I did this
by using this mapping:

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
