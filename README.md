The general flow of this project is as follows:
1. Read in raw data from fbref (soccer database for english premier league)
2. Clean raw data and get it in a pandas df that has cleaned player stats in columns
3. Write pandas df to DB using SQL
4. Clean SQL table
5. Perform ML on data pulled from DB
6. Host code on AWS so that the ML results can be accessed via REST API
