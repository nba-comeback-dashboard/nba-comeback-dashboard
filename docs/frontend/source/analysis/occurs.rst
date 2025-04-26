****************************************************************************
Occurrence Frequencies of Points Scored, Points Down, and Garbage Time Games
****************************************************************************

.. green-box::
    
    Last updated 4/25/2025




.. _largest-and-smallest-final-scores:

Largest and Smallest Final Scores
=================================

The probability density function of the final score for each team is shown below.
Remarkably, the 1st and 2nd record since 1996 come from the same 02/24/2023 game -- `a
double over time win by Kings over the Clippers 176-175
<https://www.nba.com/game/0022200902>`_.

.. raw:: html

    <div id="occurs/all_time_scores" class="nbacd-chart"></div>

Cumulating the probabilties from left to right gives us this plot, which tells us the
median score of an NBA game since 1996 is 101 points.

.. raw:: html

    <div id="occurs/all_time_scores_or_more" class="nbacd-chart"></div>

.. _max-points-down:

Max Points Down
===============

We can do a similar analysis for the maximum points down at any point in the game. Here
is the probability density function, which tells us that:

* The tightest games since 1996 have been within 5 points and it's happened 8 times.

* Only about 1,000 games out of 36,000 have been 'wire-to-wire' with either team's
  lead being 8 or less.

* And the biggest blowout ever got up to a 78 point deficit.

.. raw:: html

    <div id="occurs/all_time_max_48_point_margin" class="nbacd-chart"></div>

And we can integrate it again from left to right to get the probability of being down
max points or more, which tells us the median game runs at least a 17 point deficit.

.. raw:: html

    <div id="occurs/all_time_max_or_more_48_point_margin" class="nbacd-chart"></div>

.. _garbage-time-games:

Garbage Time Games  
==================

We can now look at the point margins exactly at 6 minutes:

.. raw:: html

    <div id="occurs/all_time_at_6_point_margin" class="nbacd-chart"></div>

And again, integrating to get points down or more at 6 minutes:

.. raw:: html

    <div id="occurs/all_time_at_or_more_6_point_margin" class="nbacd-chart"></div>

And this can tell us some interesting things.  `From the dashboard
<https://nba-comeback-dashboard.github.io/dashboard/index.html?p=2&t=6&s=1996-2024-B&m=auto>`_
we can see that:

* If you are down 15 points, you have about a 1% chance of coming back based
  historical data from 1996.

* The record comeback since 1996 was 22 points and given up by our `Minnesota
  Timberwolves to the Kings on 1/27/2020 <https://www.nba.com/game/0021900696>`_.

Using those two numbers we can say:

* A full 28% of games -- over 1 in 4! -- are effectively over by the 6-minute mark
  needing a 15 point comeback or more.
  
* And 10.4% of games would require a 23 point comeback to set a record.

That's a lot of garbage time games!  Even though, about 35% of games are within 6-7
points or less.

But, to be fair, there could have been more drama before the 6 minute mark.  Walking up
in time gets a little better.  Looking at the 4th quarter we get:

.. raw:: html

    <div id="occurs/all_time_at_or_more_12_point_margin" class="nbacd-chart"></div>

Here:

* `The team down 20 points starting the 4th has about a 1% chance of coming
  <https://nba-comeback-dashboard.github.io/dashboard/index.html?p=2&t=12&s=1996-2024-B&m=auto>`_
  and that's only about 13-14% of games where the deficit is 20 points or more starting
  the 4th.
* And games down 28 points or more -- which would require breaking `the current record
  of 27 point 4th quarter comeback <https://www.nba.com/game/0020200278>`_ -- only
  happen about 4% of the time.

And at halftime:

.. raw:: html

    <div id="occurs/all_time_at_or_more_24_point_margin" class="nbacd-chart"></div>

* `The since-1996 historical 1% chance of coming back is about a 27 point deficit
  <https://nba-comeback-dashboard.github.io/dashboard/index.html?p=2&t=24&s=1996-2024-B&m=auto>`_
  and that's only 1.5% of games.
* The 10% chance if about 15 points which is only about 17% of all games since 1996.

So it's pretty rare you need to turn off the TV at halftime.


.. _comparing-occurs-eras:

Comparing Old School (1996-2016) to Modern (2017-2024)
======================================================

Shift in Final Scores
---------------------

There has been a remarkable shift in the final scores of NBA games, with the median
score of games in the modern era being about 111 points versus 97 in the past, a 14
point shift.  And this a static shift in the mean of the data, the slope or standard
variation remains almost perfectly constant:

.. raw:: html

    <div id="occurs/old_school_v_modern_scores" class="nbacd-chart"></div>

.. raw:: html

    <div id="occurs/old_school_v_modern_scores_or_more" class="nbacd-chart"></div>

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


Garbage Time Games
------------------

Looking at max down or more at the 6 minute mark, we see a similar shift:

.. raw:: html

    <div id="occurs/old_school_v_modern_at_or_more_6_point_margin" class="nbacd-chart"></div>

But the amount of games where "it's over" stays about the same: while there are more
games with larger deficits this is offset by modern teams being able to overcome about
:doc:`2-3 more points at the same probability as in the past </analysis/20_is_new_18>`.


