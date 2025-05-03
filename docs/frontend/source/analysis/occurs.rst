****************************************************************************
Occurrence Frequencies of Points Scored, Points Down, and Garbage Time Games
****************************************************************************

.. published-date::
   :published: April 17, 2025
   :updated: May 2, 2025

.. _largest-and-smallest-final-scores:

Largest and Smallest Final Scores
=================================

The probability density function of the final score for each team of every game since
1996 is shown below. Remarkably, the 1st and 2nd highest scores since 1996 come from
the same game -- `a double overtime win by the Kings over the Clippers 176-175 on
02/24/2023 <https://www.nba.com/game/0022200902>`_.

.. raw:: html

    <div id="occurs/all_time_scores" class="nbacd-chart"></div>

Cumulating the probabilities from left to right gives us this plot, which tells us the
median score of an NBA game since 1996 is 101 points.

.. raw:: html

    <div id="occurs/all_time_scores_or_more" class="nbacd-chart"></div>

.. _max-points-down:

Max Points Down
===============

We can do a similar analysis for the maximum points down at any point in the game. Here
is the probability density function, which tells us that:

* The tightest games ever since 1996 have been within 5 points for the entire game, and
  it's happened 8 times.

* Only about 1,000 games out of 36,000 have been within 8 points for the entire game.

* And the biggest blowout ever reached a whopping 78-point deficit.

.. raw:: html

    <div id="occurs/all_time_max_48_point_margin" class="nbacd-chart"></div>

And we can integrate it again from left to right to get the probability of being down
max points or more, which tells us the median game runs at least a 17-point deficit.

.. raw:: html

    <div id="occurs/all_time_max_or_more_48_point_margin" class="nbacd-chart"></div>

.. _garbage-time-games:

Garbage Time Games
==================

.. corner-quote::
   :text: A full 28% of games -- over 1 in 4 -- are effectively over by
          the 6-minute mark, needing a 15-point comeback or more (which has about a 1%
          or lower chance of happening).

There's no exact definition of a garbage time game, so I am just going to propose a
working one: being down so much at the 6-minute mark that you have a 1% or less chance
of coming back. With this definition in mind, let's build up the data we need to count
how often we get games that meet this criterion.

We can now look at the point margins exactly at 6 minutes:

.. raw:: html

    <div id="occurs/all_time_at_6_point_margin" class="nbacd-chart"></div>

And again, integrating to get points down or more at 6 minutes:

.. raw:: html

    <div id="occurs/all_time_at_or_more_6_point_margin" class="nbacd-chart"></div>

And this can tell us some interesting things. `From the dashboard we can see
<https://nba-comeback-dashboard.github.io/dashboard/index.html?p=3&t=6&s=1996-2024-B&m=auto>`_
that:

* If you are down 15 points, you have about a 1% chance of coming back based on
  historical data from 1996.

* The record since 1996 was when the Kings came back after being down 22 points at the
  six-minute mark. It was given up by our `Minnesota Timberwolves on 1/27/2020
  <https://www.nba.com/game/0021900696>`_.

Using those two numbers we can say:

* A full 28% of games -- over 1 in 4 -- are effectively over by the 6-minute mark,
  needing a 15-point comeback or more (which has about a 1% or lower chance of
  happening).
    
* And 10.4% of games would require a record-setting 23-point comeback.

That's a lot of garbage time games, even though about 35% of games are within 6-7
points or less.

And the 1% is a bit of an arbitrary choice, but I chose it because the 5% point of 10
points seems, emotionally at least, very surmountable. And being down 18 is about 1 in
500 odds and close to the record of 22 points, which seems a bit too much.

To be fair, there could have been more drama before the 6-minute mark. Walking back in
time gets a little better. Looking at the 4th quarter we get:

.. raw:: html

    <div id="occurs/all_time_at_or_more_12_point_margin" class="nbacd-chart"></div>

Here:

* `The team down 20 points starting the 4th has about a 1% chance of coming back
  <https://nba-comeback-dashboard.github.io/dashboard/index.html?p=3&t=12&s=1996-2024-B&m=auto>`_.
  And only about 13-14% of games have a deficit of 20 points or more starting the 4th.
* And games down 28 points or more at the half -- which would require breaking `the
  current record of 27-point 4th quarter comeback
  <https://www.nba.com/game/0020200278>`_ -- only happen about 4% of the time.

And at halftime:

.. raw:: html

    <div id="occurs/all_time_at_or_more_24_point_margin" class="nbacd-chart"></div>

* `Since 1996 there's about a 1% chance of coming back from a 27-point deficit
  <https://nba-comeback-dashboard.github.io/dashboard/index.html?p=3&t=24&s=1996-2024-B&m=auto>`_,
  and that's only 1.5% of all games where the deficit is 27 or more points starting the
  3rd quarter.
* The 10% chance of coming back is about 15 points, which is only about 17% of all
  games since 1996.

So it's pretty rare that you need to turn off the TV at halftime.

Interestingly, for the playoffs, the situation does not change by much. `From the
dashboard
<https://nba-comeback-dashboard.github.io/dashboard/index.html?p=3&t=6&s=1996-2024-P&m=auto>`_
the 1% point of coming back is again about 15 points. And as we can see:

.. raw:: html

    <div id="occurs/all_time_playoffs_at_or_more_6_point_margin" class="nbacd-chart"></div>

about 29-30% of games meet this criterion, an increase of 1%. This surprised me, as I
would have guessed there would have been many more tight, competitive games during the
playoffs.

.. _comparing-occurs-eras:



.. _comparing-old-school-1996-2016-to-modern-2017-2024:

Comparing Old School (1996-2016) to Modern (2017-2024)
======================================================

Shift in Final Scores
---------------------

There has been a remarkable shift in the final scores of NBA games, with the median
score in the modern era being about 111 points versus 97 in the past, a 14-point shift.
And this is a static shift in the mean of the data; the slope or standard deviation
remains almost perfectly constant:

.. raw:: html

    <div id="occurs/old_school_v_modern_scores" class="nbacd-chart"></div>

.. raw:: html

    <div id="occurs/old_school_v_modern_scores_or_more" class="nbacd-chart"></div>


.. _comparing-occurs-eras-max-points-down:

Max Points Down
---------------

Looking at a chart comparing max points down or more:

.. raw:: html

    <div id="occurs/old_school_v_modern_max_or_more_48_point_margin" class="nbacd-chart"></div>

Now, teams fall down:

* 30 points or more ``~12.2%`` of the time compared to ``~7.6%`` in the past, a notable
  1.59x increase (or about 59% more frequently).

* 20 points or more ``~18.8%`` of the time compared to ``~14.3%`` in the past, a
  not-quite-as-dramatic 1.31x increase (or about 31% more frequently).

.. _comparing-occurs-eras-garbage-time:

Garbage Time Games
------------------

Looking at max down or more at the 6-minute mark, we see a similar shift:

.. raw:: html

    <div id="occurs/old_school_v_modern_at_or_more_6_point_margin" class="nbacd-chart"></div>

But the amount of games where "it's over" stays about the same: while there are more
games with larger deficits, this is offset by modern teams being able to overcome about
:doc:`2-3 more points at the same probability as in the past </analysis/20_is_new_18>`.





.. _comparing-regular-season-versus-the-playoffs-late-game-point-margins:

Comparing Regular Season Versus the Playoffs Late Game Point Margins
====================================================================

Comparing the number of blowout games in the regular season versus the playoffs shows
no appreciable difference. Surprising, given the stakes and that the bottom teams have
been weeded out from contention. It has been stated that `there's an increasing number
of blowouts occurring in the playoffs
<https://www.theringer.com/2022/05/25/nba/playoff-basketball-blowout-trend-historical-analysis>`_,
but looking at the point margins across all games does not bear this out:

.. raw:: html

    <div id="occurs/all_time_reg_v_playoffs_at_or_more_6_point_margin" class="nbacd-chart"></div>

Here, the occurrence of 15 points down or more games is 29.8% for the playoffs versus
28.2% for the regular season, nothing major.

Looking at the point margin at the buzzer, we get a result which tells a similar story:

.. raw:: html

    <div id="occurs/all_time_reg_v_playoffs_at_or_more_0_point_margin" class="nbacd-chart"></div>

We can also check to see if there's been a dramatic shift recently. Comparing all games
since 1996 versus the last four years for how bad the losing team is down at the six-
minute mark, we get:

.. raw:: html

    <div id="occurs/very_modern_vs_all_time_at_or_more_6_point_margin" class="nbacd-chart"></div>


A shift, but this is :doc:`the same two-point shift </analysis/20_is_new_18>` we see
when comparing comeback chances in different eras. For the last four years of playoff
games, roughly 30% of games at the six-minute mark have a point deficit of 16 or more
compared to 14 points or more for all time. And given that teams can overcome about 2
more points of deficit, this is about the same level of "excitement" in the game: for
example, at six minutes about 50% of playoff games have a 10-point deficit in the last
four years versus a 9-point deficit in the past.


