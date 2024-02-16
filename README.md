# Cryptocurrency-backtester

CS122 Final Presentation: Building a Cryptocurrency Backtester
GROUP MEMBERS: Shalini Chandar, Michelle Liang, Calvin Chu, JX Xu
March 12, 2018

In this file you will find a description of the project and of 
each of the files in the crypto_website folder. 

An overview of our project can be found at the following link:
[https://docs.google.com/presentation/d/1IRw2CAZUggStlQui1iLmNkWGrDhN6cKb3sXao_Freog/edit#slide=id.g2f1c04b915_0_5](https://docs.google.com/presentation/d/1uDKrRHRf44le6iswrt7WnTfBzQs-JxBj4vX4rpi8eN8/edit?usp=sharing)

Project Description:

	Goal: build an interactive cryptocurrency backtester to analyze different trading strategies for cryptocurrencies (or coins)
	Based on trading strategies, determine absolute returns, returns relative to a benchmark, and Sharpe ratio
	Save best strategies on a leaderboard (ranked by Sharpe ratios)

	Trading Strategies Tested:

	- Test if the letter a coin starts with influences returns
		- Coins that begin with A may have more exposure
	- Analyze a coin’s white paper complexity using NLTK
		- Coins with more complex language in their white paper may have a more advanced development team and a better product
	- Reddit subscriber growth and total subscriber at end of period
		- Faster growing subreddits indicate high buyer interest
	- Google Trends search volume change over time
		- Increased search volume may lead price movement
	- Twitter mentions of various coins on 2018-03-01
		- Increased number of mentions may lead price movement 

Table of Contents:

Note: there is a "ghost" column in many of the CSVs called "Twitter_Mentions". This is here because we initially intended to find day-to-day Twitter mentions data, but eventually were not able to. We did not want to re-generate all of the CSVs, so the values in each of these columns is 1. 

- historical_dfs: folder containing CSVs for coins we were able to get historical price and volume data for (244 coins)

- All_Coin_dfs: folder of CSVs containing day-to-day Google Trends data

- reddit_dfs: folder of CSVs containing day-to-day Reddit subscriber data

- final_coins: folder containing final CSVs for all 250 coins
(including all time-dependent data available)

- whitepaper_pdfs: PDFs of coins' white papers

- whitepaper_text_files: PDF content in .txt format

- mysite: folder containing code for Django website

- predictors: folder containing code for strategy selection/testing application

- all_data.p: dumped pickle dictionary. Contains data from each coin's JSON file from the CoinMarketCap API

- unclean_data.p: unclean version of all_data.p

- backtester.py: contains functions to analyze DataFrames and build backtester (called in views.py in predictors)

- chromedriver: required to run webdriver from Selenium

- create_leaderboard.py: contains functions to create strategy leaderboard (called in views.py in predictors)

- Cryptocoins.csv: contains information (coin name and ticker, specifically) for cryptocurrencies 

- Updated_Cryptocoins.csv: same as Cryptocoins.csv, with corrections to format of some of the coins' names

- get_data.py: contains functions to generate all of the CSVs/DataFrames. 

- leaderboard.csv: file containing the current strategy leaderboard

- Static_Params.csv: file containing all the non-time-dependent data for each coin

- twitter.csv: file containing number of Twitter mentions for each coin on March 1, 2018

- twitter.py: contains code to count number of Twitter mentions for each coin on March 1, 2018, and export the data to a CSV
















