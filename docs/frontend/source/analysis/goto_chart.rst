**************
The Goto Chart
**************

.. green-box::
    
    Last updated 4/22/2025

.. _all-the-available-data:

All The Available Data
======================

Overall, I feel the most useful dashboard chart is this one:

.. raw:: html

    <div id="goto/nbacd_points_versus_36_time_all_eras" class="nbacd-chart"></div>

This includes all games from 1996 (which is about ~36,000 games). If your team is down,
this gives you a pretty good sense of how steep of a mountain your team has to climb
(and of course on the flip side, how safe your lead is). Plus, I like being able to see
the current record for a given time, knowing that if you are beyond the record it would
be, well, a record if you came back. (And just noting that the :doc:`Minnesota
Timberwolves </analysis/do_the_twolves_give_up_big_leads>` hold or tie the record for
allowing the biggest comebacks at the 3, 6, 7, and 10 minute marks).

You can click on data points and see which game(s) hold the record. Going full screen
makes it easier, and on mobile, you have to go full screen first. Once you go full
screen, then you can click on any point to get the summary for that minute.

Please note, the 'Record' is calculated by getting the point margin exactly at that
minute mark, so if a team was down 25 at the start of the 4th and then went down 26 and
then back to 25 by the 11th minute, the 26 is not recorded here.

Of course, this is all games from 1996 with no other conditions (e.g., recent years,
home vs. away, etc.). And this :doc:`chart will change if you change the conditions
</analysis/rule_of_thumb_that_actually_works>`.

.. _how-this-compares-versus-espns-live-win-probability:

How This Compares Versus ESPN's Live Win Probability
====================================================

A useful way to judge the utility of this chart is to see how it compares to ESPN's
running win probabilities for a given game. Even though the ESPN model is a complicated
model, relying heavily on their `Basketball Power Index
<https://www.espn.com/nba/story/_/page/Basketball-Power-Index/espn-nba-basketball-power-index>`_,
and the dashboard model is simply relying on the raw game data from 1996 and
:doc:`fitting a normal model to the data
</analysis/methodology_forming_the_plot_trend_lines>`, both models mostly tell a
similar story about a team's overall comeback chances.

Timberwolves @ Bucks on 04/09/2025
----------------------------------

So let's look at a recent run-of-the-mill Timberwolves game `against the Bucks on
04/09/2025 <https://www.nba.com/news/bucks-stun-timberwolves-4th-quarter-comeback>`_:

.. raw:: html

    <div id="goto/espn_v_dashboard_all_time_min_at_bucks_401705718" class="nbacd-chart"></div>

Here, we are again plotting on a normal probability plot instead of a linear y-axis so
we can better examine the extreme probabilities. The dashboard probabilities are taken
from the same ones shown in the goto chart at the top of this page. In fact, for any
dashboard point, you can click on it and it will bring you to the interactive dashboard
page and show the exact regression fit line used to calculate the probability for that
point. And if you click on the 10 minutes remaining point, you will see that the
Timberwolves hold the record for losing a game when up 24 points with 10 minutes to go.

.. raw:: html

    <div id="goto/espn_v_dashboard_all_time_min_at_bucks_401705718" class="nbacd-chart"></div>

But results vary from game to game. Let's just look at a few more games I watched
recently:

.. raw:: html

    <div id="goto/espn_v_dashboard_all_time_gsw_at_hou_401767823" class="nbacd-chart"></div>

.. raw:: html

    <div id="goto/espn_v_dashboard_all_time_min_at_lal_401767915" class="nbacd-chart"></div>

.. raw:: html

    <div id="goto/espn_v_dashboard_all_time_grizz_at_okc_401767903" class="nbacd-chart"></div>

Some features are notable:

* Clearly, ESPN's BPI index is more heavily discounting certain teams independent of
  record.
  
* The differences are larger until about the 4th quarter, where they tend to converge.

.. _adding-conditionals-home-versus-away-for-the-modern-era:

Adding Conditionals: Home Versus Away For The Modern Era
========================================================

The conditional providing the greatest discrimination is probably adding whether
:doc:`the team coming back is at home or away </analysis/home_v_away>`. Then,
:doc:`limiting the seasons to the modern era </analysis/20_is_new_18>`.

Adding those two conditions gives you these two plots, which will give you a more
accurate probability:

.. raw:: html

    <div id="goto/nbacd_points_versus_36_for_home_modern_era" class="nbacd-chart"></div>

.. raw:: html

    <div id="goto/nbacd_points_versus_36_for_away_modern_era" class="nbacd-chart"></div>

Comparing To The ESPN Model
---------------------------

You can add conditions to help discriminate on the current game. For example, we can
plot this same game again but :doc:`limit to seasons to the last 8 years
</analysis/20_is_new_18>` and take the :doc:`home team advantage
</analysis/home_v_away>` into account:

.. raw:: html

    <div id="goto/espn_v_dashboard_modern_at_home_min_at_bucks_401705718" class="nbacd-chart"></div>

.. raw:: html

    <div id="goto/espn_v_dashboard_modern_at_home_gsw_at_hou_401767823" class="nbacd-chart"></div>

.. raw:: html

    <div id="goto/espn_v_dashboard_modern_at_home_min_at_lal_401767915" class="nbacd-chart"></div>

.. raw:: html

    <div id="goto/espn_v_dashboard_modern_at_home_grizz_at_okc_401767903" class="nbacd-chart"></div>

Making the dashboard model account for home court advantage and increased chances of
coming back in the modern era leads the fit to be a little worse for some cases (and a
little better in others).

Understanding how difficult it is to compare probability models, there still are some
data points that stand out. For example, for the April 20 GSW @ HOU game, at 18 minutes
remaining with Golden State having a 21-point lead, ESPN has them with a win
probability of 98.4%.

Based just on all games from 1996 until now, the odds are about 97.8% -- however, when
we account for the fact that Golden State was the away team and limit our data to the
modern era (where comebacks are slightly more likely), the dashboard model drops the
win probability to 95.9%. Seeing how Houston was the 2nd seed in the west and Golden
State got in through the play-in, I am curious what data ESPN has that pushes them
above the historical average by a point.

.. _supplementals:

Supplementals
=============

Even though the first chart gets you most of the way there, sometimes a chart like this
limited to our recent history is also useful:

.. raw:: html

    <div id="goto/twolves_leads_12_recent" class="nbacd-chart"></div>

Just to get a sense of what we're capable of!




