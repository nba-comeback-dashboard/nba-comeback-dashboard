****************
20 is the New 18
****************

.. green-box::
    
    Last updated 4/25/2025

.. _are-big-leads-no-longer-safe:

Are Big Leads No Longer Safe?
=============================

There's a perception that, in recent times, teams are climbing out of big deficits more
often than ever before. Just as `Kevin Pelton and Baxter Holmes noted in 2019
<https://www.espn.com/nba/story/_/id/26725776/this-season-massive-comeback-nba>`_, so
did ESPN reporter Andrew Lopez in `'20 is the old 12': Why no lead is safe in the NBA
anymore
<https://www.espn.com/nba/story/_/id/39698420/no-lead-safe-nba-big-comebacks-blown-leads>`_.
There he points out that the 2023-24 season had already seen the most 20-point
comebacks in a single season since 1996-97 and continues with analysis by Steve Kerr:

.. pull-quote::

    "Way more early possession 3s now. It just feels like you are up 12 and the other
    team gets two quick stops on you and they race down, they throw it ahead and they
    hit two 3s. It's a six-point game now. So 20 is the old 12; 12 is the old seven. I
    mean, there's definitely an awareness from everybody that leads are not safe."


But is this true? In short... not really. While a statistically large and significant
shift has occurred comparing new to old, the shift is more about 2 to 2.5 points, not 8.

To frame this, I decided to break up the available play-by-play data into:

* 1996-97 to 2016-17 (old-school) versus
* 2017-18 to 2024-25 (modern)

(:ref:`As explained below <deciding-on-eras-breakdown>`, a more targeted recent modern
era does not change the analysis so the larger dataset was chosen).

Looking at this data, the chance of coming back from 20 points-or-more down (``~5.3%``)
is about the same as coming back from 18 points-or-more down (``~4.9%``) in the earlier
era. To put this in perspective, this overall 2 to 2.5 point shift is on par with but
not quite as pronounced as :doc:`the advantage a home team has over a road team
</analysis/home_v_away>` when attempting a comeback. Note, there are :doc:`many ways to
compare the comeback chances of the eras
</analysis/understanding_and_using_the_plots>`, but roughly 2 points is a fairly stable
characterization of the shift under varying conditions.

To be clear, there has been a marked shift in the data: there are about 1.8 times as
many 20-points-or-more comebacks comparing the eras. And when viewed through the lens
of a point spread in sports betting, a 2-3 point shift is significant.

But as a fan watching the game, the data shows that leads are *roughly* as safe as they
have been, perhaps needing an extra bucket to maintain the same level of security.


.. _win-percentages-when-max-deficit-is-n-or-more-points:

Win Percentages When Max Deficit is N *Or More* Points
======================================================

:ref:`A very common way of looking at comebacks<max-points-down-or-more>` is
calculating the % chance of coming back from down N points *or more* over an entire
game:

.. raw:: html

    <div id="plots/old_school_v_modern/max_down_or_more_48" class="nbacd-chart"></div>

An insight is that percent chance of coming back versus point deficit is normally
distributed under most conditions.  So when plotted on a `normal probability plot
<https://en.wikipedia.org/wiki/Normal_probability_plot>`_ and :doc:`trend lines (e.g. a
normal model) are fit to the statistical data
</analysis/methodology_forming_the_plot_trend_lines>` one can then better examine the
lower probability events and also more easily compare different eras or situations.

And when comparing these two eras, one can see a mostly stable and constant shift of
about 2-3 points to the left for the modern era versus the past.

You can :ref:`interact with this chart <using-the-plot-controls>` and hover over and
click the points to see which games compose a point and compare it with a `list of
biggest comebacks <https://en.wikipedia.org/wiki/Comeback_(sports)#NBA>`_ if so
inclined (on mobile, go full screen before clicking).  To focus on a few we get:

.. list-table:: Win % Increases When Comparing Modern Versus Old School Eras
   :header-rows: 1

   * - Points Down Or More
     - 1996-2016 Win %
     - 2017-2024 Win %
     - Total Win % Increase
   * - 30
     -  0.15 %
     -  0.42 %
     - 2.8x (180% increase)
   * - 20
     - 2.89 %
     - 5.31 %
     - 1.83x (80% increase)
   * - 18
     - 4.88 %
     - 7.93 %
     - 1.59x (60% increase)
   * - 15
     -  9.22 %
     - 12.82 %
     - 1.39x (39% increase)

So while coming back from down 30 or more happens 2.8 times more often than in the
past, it's still very unlikely. In fact, you need to move over a little less than one
three-pointer to get about the same chance: in the old school era, if you were down -27
or more there was about a ``~0.50%`` chance of winning. And being down 20 or more now
has just about the same chance of winning as being down 18 or more back in the day
(``~5.0%``).

.. green-box::

    Note, this uses the raw data points, which is a little more intuitive. You can also
    do this using the trend line in the chart, which cleans up the noise in the data
    and is statistically more accurate. Overall, either way draws the same conclusion.

As time dwindles, this shift is slightly smaller. Looking at biggest 4th quarter
comebacks we get:

.. raw:: html

    <div id="plots/old_school_v_modern/max_down_or_more_12" class="nbacd-chart"></div>

Now, the shift is about 1.5 points, an even smaller shift.

To me at least, looking at the point shift gives me a better feel for how dramatically
(or not) the game has changed. I can be convinced you could look at it both ways (Win %
Increase is more dramatic, point shift is more modest), but as a fan watching your team
sink into a 20 point hole, I don't think the data is telling you to say "20 points,
that's nothing anymore".



.. _max-down-at-most-n-points:

Win Percentages When Max Deficit is N Points At Most
====================================================

:ref:`Another way of looking at comebacks<max-points-down-at-most>` is calculating the
% chance of coming back from down N points *at most* over an entire game:


.. raw:: html

    <div id="plots/old_school_v_modern/max_down_48" class="nbacd-chart"></div>

And from halftime:

.. raw:: html

    <div id="plots/old_school_v_modern/max_down_24" class="nbacd-chart"></div>

Here the shift is a little larger, about 2.75 points.


.. _win-percentages-when-teams-are-down-n-points-with-so-much-time-left:

Win Percentages When Teams Are Down N Points With So Much Time Left
===================================================================

:ref:`Another way to look at it and the more natural way to think about it while you
are watching a game live<points-down-at-time>` (as opposed to describing a game after
the fact) is to look at the win percentages when teams are down *exactly* N points with
so much time left. Here's a chart for the start of the 2nd half:

.. raw:: html

    <div id="plots/old_school_v_modern/down_at_24" class="nbacd-chart"></div>

The data is a bit noisier here, because we are not accumulating the games as we move
from left to right like we did when looking at points down *or more*. Here, for the old
school era, we have the case that there was one game (``11/27/1996 DEN @ UTA:
103-107``) where UTA was down -34 at the half and won. But no team in that era won when
down *exactly* -33, -32, -31, -30 or -29 at the half.

Now, the divide here is no longer as much of a shift as a change in slope of about 20%
more for the modern era.  So being down 20 in the modern era is about the same as being
down 16.75 points in the old school era (a 3.25 point shift). And being down 10 points
now is the same as being down 8.5 points in the past (a 1.5 point shift).

But as time decreases it tightens up -- looking at starting the 4th quarter we see that
the change in slope is about 13% now -- so being 20 points down (``~0.17%``) is about
the same as 17.75 points down when comparing new to old:

.. raw:: html

    <div id="plots/old_school_v_modern/down_at_12" class="nbacd-chart"></div>



.. _20-is-18-win-versus-time:

Win % Versus Time
=================

Collecting this data for every minute, :ref:`we can focus on a single percentage and
plot the time v point deficit for that percentage
<percent-chance-of-winning-time-v-points-down>`.  Doing that for 10% while comparing
the eras we get:

.. raw:: html

    <div id="plots/old_school_v_modern/percent_plot_10_percent" class="nbacd-chart"></div>


And doing it for 1% we get:

.. raw:: html

    <div id="plots/old_school_v_modern/percent_plot_1_percent" class="nbacd-chart"></div>

The point spread changes over time, but between 2 - 3 points is a fairly good
characterization.

.. _real-time-probabilities:

Real Time Probabilities
=======================

One interesting way to look at the data is to show what the running probabilities would
be using data from the modern era versus the past.

.. raw:: html

    <div id="20_18/espn_v_dashboard_old_school_v_modern_min_at_lal_401767915" class="nbacd-chart"></div>

So at halftime, the wolves had 12.9% chance of winning using modern data versus a 9.1%
chance if you use data from the past.

Here's another game:

.. raw:: html

    <div id="20_18/espn_v_dashboard_old_school_v_modern_min_at_bucks_401705718" class="nbacd-chart"></div>

The same basic trend emerges: from a statistical standpoint, there are notable large
shifts in percentages comparing the eras (3-4% in some cases).  But the shift is not
large enough to greatly effect how it "feels" as a fan to be down, say, 15 points at
the half.

.. _what-an-8-point-shift-looks-like:

What An 8 Point Shift Looks Like
================================

When I started to compare the modern versus old school eras, I was expecting (based on
the current perception out there) that the shift was going to be large.  When it
wasn't, I assumed there were simply bugs in my setup and I spent a lot of time sanity
checking the results (and, if I still have mistakes, lines are open).

In that context, I thought it would be useful to get a sense of what an 8 point shift
looks like and the kind of trend I was expecting to see.  So if we look at top 10 teams
(out of 30) vs. bottom 10 teams in the modern era we get:

.. raw:: html

    <div id="20_18/dramatic" class="nbacd-chart"></div>

Here, the chance of top ten team playing a bottom 10 team coming back from a
20-points-or-more deficit (``~20%``) is about the same for any team coming back from 12
or more down against any other team.


.. _what-else-could-be-going-on:

What Else Could Be Going On?
============================

I am making the case that, in face of popular opinion, blowing a 20-point lead has
about the same chances as blowing an 18-point lead in the past. That two-point shift is
significant but I don't think matches what `I see people saying about leads these days
<https://www.reddit.com/r/nba/comments/1cc2qqv/dumb_question_is_blowing_a_20_point_lead_that_bad/>`_.
 
So I just want to consider a few points that I think are useful when thinking about
this issue:

* Scoring is up dramatically. :ref:`The median score is 111 points in the modern era
  <comparing-occurs-eras>` as compared to 97 in the past: a 14-point shift. Also, teams
  getting down 30 or more points happens 60% more often and teams getting down 20 or
  more points happens 30% more now than in the past.

* However, the fact that teams can score more quickly does not automatically
  lead to the conclusion that big comebacks should be more probable: I mean, if you are
  down and can score quickly, so can your opponent and keep you down. So while points
  are a little easier to come by, this effect is offset by the counter fact that they
  are also a little easier to give up.

* I do think part of the problem is `availability bias
  <https://www.simplypsychology.org/availability-heuristic.html>`_: that is, things
  that happen recently, especially ones you've witnessed personally, lead to the false
  conclusion that they are happening more often than in the past. After personally
  watching a series of garbage time games recently, I got to thinking "ok, but for sure
  this is an increasing phenomenon". :ref:`But when I look at the data
  <comparing-occurs-eras>` it's almost constant (there are slightly more large deficit
  games but this is offset by a 2-point shift in a team's chances of coming back).

* I do want to compare the average size and min/max size of runs between the two eras.
  It may be that large swings are much more common, leading to a perception of
  increased chances of coming back. But here again, if it's an option for you to go on
  a run, it's also an option for your opponent.

  For another day.

.. _supplemental:

Supplemental
============

.. _deciding-on-eras-breakdown:

Why I Chose My Years Breakdown
------------------------------

If you:

* :doc:`Break up the old school eras into two even decades from 1996-2006 v 2007-2016
  </analysis/plots/old_old_school_v_old_school>` you can see there is very little shift
  in the numbers.

* Similarly, if you :doc:`break up the modern era into the more fine-grained 4 year
  chunks of 2017-2020 v 2021-2024 </analysis/plots/new_school_v_new_new_school>` you
  again see very little difference.

So -- always wanting as many games as possible to reduce the statistical noise -- I
felt that was the fairest breakdown: :doc:`1996-2016 v
2017-2024</analysis/plots/old_school_v_modern>`.  I also tried to create the most
dramatic shift possible between something considered modern versus historical.




