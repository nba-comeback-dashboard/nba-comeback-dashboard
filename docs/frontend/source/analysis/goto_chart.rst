******************************************
Goto Chart: The Only Chart You Really Need
******************************************

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
(and of course on the flip side how safe your lead is). Plus, I like being able to see
the current record for a given time knowing that if you are beyond the record it would
be, well, a record if you came back. (And, ahem, our :doc:`Minnesota Timberwolves
</analysis/do_the_twolves_give_up_big_leads>` hold or tie the record for allowing the
biggest comebacks at the 3, 6, 7, and 10 minute marks).

You can click on data points and see which game(s) hold the record. Going full screen
makes it easier and on mobile, you have to go full screen first. Once you go full
screen, then you can click on any point to get the summary for that minute.

Please note, the 'Record' is calculated by getting the point margin exactly at that
minute mark, so if a team was down 25 at the start of the 4th and then went down 26 and
then back to 25 by the 11th minute, the 26 is not recorded here.

Of course, this is all games with no other conditions (e.g. home v away, etc.). And
this :doc:`chart will change if you change the conditions
</analysis/rule_of_thumb_that_actually_works>`.


.. _home-versus-away-for-the-modern-era:

Home Versus Away For The Modern Era
===================================

The conditional providing the greatest discrimination is probably adding whether
:doc:`the team coming back is at home or away </analysis/home_v_away>`. Then,
:doc:`limiting the seasons to the modern era </analysis/20_is_new_18>`.

Adding those two conditions gives you these two plots, which will give you a closer
match to the probability given by an in-game probability calculator for example:

.. raw:: html

    <div id="goto/nbacd_points_versus_36_for_home_modern_era" class="nbacd-chart"></div>

.. raw:: html

    <div id="goto/nbacd_points_versus_36_for_away_modern_era" class="nbacd-chart"></div>


.. _how-this-compares-versus-espns-live-win-probability:

How This Compares Versus ESPN's Live Win Probability
====================================================

Using All Game Data
-------------------

To get a sense of how well the :ref:`first chart (which just looks at all available
data) works <all-the-available-data>`, I plotted what probabilities it came up with
versus what ESPN's live game probability page spits out. And, not because :doc:`I'm
obsessed with this game or anything </analysis/do_the_twolves_give_up_big_leads>`,
let's look at a recent run of the mill Timberwolves game `against the Bucks on
04/09/2025 <https://www.nba.com/news/bucks-stun-timberwolves-4th-quarter-comeback>`_:

.. raw:: html

    <div id="goto/espn_v_dashboard_all_time_min_at_bucks_401705718" class="nbacd-chart"></div>

Here, we are again plotting on a normal probability plot instead of a linear y axis so
we can better examine the extreme probabilities. The dashboard probabilities are taken
from the same ones shown in the goto chart at the top of this page. In fact, for any
dashboard point you can click on it and it will bring you to the interactive dashboard
page and show the exact regression fit line used to calculate the probability for that
point.  And if you click on the 10 minutes remaining point you will see that the
Twolves hold the record for losing a game when up 24 points with 10 minutes to go.

Why there are differences between this model and ESPN's model should come as no
surprise: as stated elsewhere, the algorithms used to come up with live game
probability calculator employ `involved formulas
<https://fivethirtyeight.com/methodology/how-our-nba-predictions-work/>`_ that are also
closed so it's not clear what the input conditions are being fed into the model.

In this dashboard model, :doc:`the underlying methodology is meant to be simple and
transparent </analysis/methodology_forming_the_plot_trend_lines>` and you can click on
the data to see exact historical game data used to fit the regression line.


Adding Conditionals
-------------------

You can add conditions to help discriminate on the current game. For example, we can
plot this same game again but :doc:`limit to seasons to the last 8 years
</analysis/20_is_new_18>` and take the :doc:`home team advantage
</analysis/home_v_away>` into account:

.. raw:: html

    <div id="goto/espn_v_dashboard_modern_at_home_min_at_bucks_401705718" class="nbacd-chart"></div>

This now is further away from the ESPN model, but for all practical purposes tells the
same story. Here, the dashboard model is giving a bigger advantage to the home team, it
appears but again exact comparisons are not possible due to the closed nature of the
model (nor would I attempt to understand it even if I had the source code).  It could
be very well that the ESPN model is not taking home court advantage enough into account
but I'm not sure all the variables be fed into the model.

Taking another game at random that I just watched and was testing the dashboard against
was the GSW @ HOU on April 21, 2025. Here's the comparison just using all available
game data since 1996:

.. raw:: html

    <div id="goto/espn_v_dashboard_all_time_gsw_at_hou_401767823" class="nbacd-chart"></div>

And here again using recent years and home team advantage:

.. raw:: html

    <div id="goto/espn_v_dashboard_modern_at_home_gsw_at_hou_401767823" class="nbacd-chart"></div>

.. _supplementals:

Supplementals
=============

Even though the first chart gets you most of the way there, sometimes a chart like this
limited to our recent history is also useful:

.. raw:: html

    <div id="goto/twolves_leads_12_recent" class="nbacd-chart"></div>

Just to get a sense of what we're capable of!




