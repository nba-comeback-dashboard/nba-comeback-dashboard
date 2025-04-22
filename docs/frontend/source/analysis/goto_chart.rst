******************************************
Goto Chart: The Only Chart You Really Need
******************************************


.. _all-the-available-data:

All The Available Data
======================

Overall, I feel the most useful dashboard chart is this one:

.. raw:: html

    <div id="goto/nbacd_points_versus_36_time_all_eras" class="nbacd-chart"></div>


This includes all games from 1996 (~36,000 games) and -- if you're down -- gives you a
pretty good sense of how steep of a mountain your team has to climb (and of course on
the flip side how safe your lead is).  Plus, I like being able to see the current
record for a given time, knowing that if you are beyond the record it would be, well, a
record if you came back.  (And, ahem, our :doc:`Minnesota Timberwolves
</analysis/do_the_twolves_give_up_big_leads>` hold or tie the record for allowing the
biggest comeback at the 3, 6, 7, and 10 minute marks).

You can click on data points and see which game(s) hold the record. Going full screen
makes it easier (and on mobile, you have to go full screen first -- also, on mobile, it
helps to rotate the screen, go full screen, and then you can click on any point to get
the summary for that minute).

Please note, the 'Record' is calculated by getting the point margin exactly at that
minute mark, so if a team was down 25 at the start of the 4th and then went down 26 and
then back to 25 by the 11th minute, the 26 is not recorded here.

Of course, this is all games and this :doc:`chart will change if you change the
conditions </analysis/rule_of_thumb_that_actually_works>`.



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

.. raw:: html

    <div id="goto/espn_v_dashboard_all_time_min_at_bucks_401705718" class="nbacd-chart"></div>


.. raw:: html

    <div id="goto/espn_v_dashboard_modern_at_home_min_at_bucks_401705718" class="nbacd-chart"></div>


.. 
    .. image:: goto_MIN_MIL_2025_04_09_live_prob.png
    :scale: 20%
    :align: center


    .. raw:: html

        <div id="goto/at_10_at_home_modern_era" class="nbacd-chart"></div>


    .. image:: goto_GSW_HOU_2025_04_21_live_prob.png
    :scale: 20%
    :align: center







.. _supplementals:

Supplementals
=============

Sometimes, watching a Timberwolves game, a chart like this limited to our recent
history is useful to look at during the break:

.. raw:: html

    <div id="goto/twolves_leads_12_recent" class="nbacd-chart"></div>

Just to get a sense of what we're capable of!




