Formula 1 Ratings Engine  
by Menno Rooker, Dec 2024  
based on Formula 1 ELO Engine by Mr. V  

Contents
--------
1. Introduction
2. Acknowledgements
3. Calculations
4. Layout
5. Video


Introduction
------------

Formula 1 often gets accused of being a sport that rewards a driver's budget over his skill, receiving ridicule from people who have noticed that - more often than not - the driver with the better car gets the better result. It is true that since teams can create their own cars these vehicles can vary significantly in performance, making most metrics to determine who the most skilled driver is hard to objectively quantify. However, by looking at how other sports (or games) determine who the best is and adjusting it accordingly we can perhaps determine who the best F1 driver is over the course of a season, or even over their whole career.


Acknowledgements
----------------
This project is very much based on the Formula 1 ELO engine created by YouTuber Mr. V. (https://www.youtube.com/watch?v=U16a8tdrbII)

The way this project differs is in its method of calculating drivers' ratings. In Mr. V's original ELO engine he uses head-to-heads between teammates to determine a change in a driver's rating. This method stems from the original application of [ELO rating of zero-sum games](https://en.wikipedia.org/wiki/Elo_rating_system) where the calculation requires there to be a 1-vs-1 battle between competitors. However, ELO-like rating systems have been altered to fit different kinds of competition, including Battle Royale style videogames, which is what this ELO engine will be based on.

Like Mr. V I will be using the [Formula 1 World Championship (1950 - 2024) ](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020?resource=download) dataset by Vopani.


Calculations
------------

The rating system I used is loosely based on a Battle Royale rating system used in competitive games like [Apex Legends](https://help.ea.com/nl/help/apex-legends/apex-legends/apex-legends-ranked-mode/). The idea behind it is that higher rated players enter a game with negative points and they earn points by ranking higher than opponents by the end of their match. This makes sure that even when 20 teams hop into the same match that they are all competing for points in a balanced manner.  

To apply this idea to Formula 1 all we have to do is apply penalties to drivers based on how their team is doing in the constructors standings. The higher ranking teams will receive a larger penalty at the start of each race and thus we get a more balanced rating system that hopefully rates a driver's individual skill more accurately.

<img src="docs/Ratings Calculations Screenshot.png" alt="calculations" width="400"/>

For consistency reasons the post-2010 scoring system is applied to all seasons and any points earned from the fastest lap are removed.


Layout
------

The homepage lead you to one of 3 different pages: seasonal leaderboards, the all-time leaderboard or season compare. Each page can be viewed by any user by simply going to the links at the top of the homepage or by selecting a season at the bottom.  

The seasonal leaderboards display the regular points earned by the driver and the adjusted points based on this new rating system.

<img src="docs/Leaderboard Screenshot.png" alt="leaderboard" width="400"/>

By clicking on 'Compare Seasons' you can select 2 drivers and 2 corresponding years in which they raced and see how they would have stacked up against each other had they driven in the same era.

<img src="docs/Compare Seasons Screenshot.png" alt="compare seasons" width="400"/>

The graphs in both 'Compare Seasons' and at the bottom of the seasonal leaderboards can be switched from the regular points earned by the drivers during the season to the adjusted points, with penalties applied, by ticking the 'With Penalties' box above the graph.

<img src="docs/With Penalties tick-box.png" alt="tick" width="120"/>

Video
-------

![Watch screencast](https://www.youtube.com/watch?v=308zRVImBsc&feature=youtu.be)


Author
-------

Menno Rooker

 
  
