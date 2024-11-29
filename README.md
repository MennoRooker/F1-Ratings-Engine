Formula 1 Ratings Engine
by Menno Rooker, Nov 2024
based on Formula 1 ELO Engine by Mr. V

homepage: (hyperlink here)

Contents
--------
1. Introduction
2. Acknowledgements
3. Layout
4. Features
5. Requirements
6. Uncertainties


Introduction
------------

In this project I will attempt to answer the question "Who is the best Formula 1 driver in the world?" by building an ELO engine that attributes ratings to drivers on the grid based on more than just the results of the races. 

Formula 1 often gets accused of being a sport that rewards a driver's budget over his skill, receiving ridicule from people who have noticed that - more often than not - the driver with the better car gets the better result. It is true that since teams can create their own cars these vehicles vary greatly in performance, making most metrics to determine who the most skilled driver is hard to objectively quantify. However, by looking at how other sports (or games) determine who the best is and adjusting it accordingly we can perhaps determine who the best F1 driver is over the course of a season, or even over their whole career.

The end result of this project will be a web page. Anybody interested in Formula 1 is welcome to check out the results!


Acknowledgements
----------------
This project is very much based on the Formula 1 ELO engine created by YouTuber Mr. V. (https://www.youtube.com/watch?v=U16a8tdrbII)

The way this project differs is in its method of calculating drivers' ratings. In Mr. V's original ELO engine he uses head-to-heads between teammates to determine a change in a driver's rating. This method stems from the original application of [ELO rating of zero-sum games](https://en.wikipedia.org/wiki/Elo_rating_system) where the calculation requires there to be a 1-vs-1 battle between competitors. However, ELO-like rating systems have been altered to fit different kinds of competition, including Battle Royale style videogames, which is what this ELO engine will be based on.

Like Mr. V I will be using the [Formula 1 World Championship (1950 - 2024) ](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020?resource=download) dataset by Vopani.


Layout
--------
 
The web page of the results of my ELO engine will be split up into at least 2, but possibly 3 kinds of pages. The first will be a homepage with some information and a drop-down menu that takes the user to the results of a specific season. There will also be an option to look at the ALL-TIME ELO ratings of all drivers included in the data set.

![Homepage](sketch1.jpg)

After selecting a season the end ratings for that season (or current rating for the ongoing season) will be displayed on a leaderboard.

![Leaderboard](sketch2.jpg)

If the length of the project will allow me to I will implement the individual drivers' pages.
Clicking on a driver (on the leaderboard) will take you to their own personal page, where you can see all their results. I hope to implement graphs of their ELO rating throughout the season(s).

![Driver's Page](sketch3.jpg)

 
Features
--------
Below is a summation list of the features I intend to implement:
 
  * A comprehensive method for determining a driver's rating
  * An interactive website with hyperlinks to leaderboards
  * An ALL-TIME leaderboard where only the peak ratings of drivers are shown

A few more features I HOPE to implement are listed below ordered from highest to lowest priority:

  * Individual drivers' pages with their results history
  * Graphs of ratings over time
  * Stylistic optimizations


Requirements
-------

Like I mentioned before, I will be using the [Formula 1 World Championship (1950 - 2024) ](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020?resource=download) dataset by Vopani. This dataset uses the [Kaggle API](https://www.kaggle.com/docs/api#authentication).


Uncertainties
-------

Some things I imagine will be difficult include:

  * Working with a new API
  * Getting valid results out of my ELO calculations
  * Setting up an interactive website with proper functionality
  * Having enough time left to optimize my ELO engine in case it yields weird results


Author
-------

Menno Rooker

 
  
