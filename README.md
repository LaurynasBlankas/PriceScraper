This code running on GitHub actions, converts the url specified in the_scraper.py into html, and checks the .lowprice class, 
should be changed according to the website.
Then send notifications to telegram bot if it drops bellow the specified price in the same file.

To link your own telegram to get notifications, create .env file in the project with:
api_key=(telegram bot id)
receiver_id=(Telegram users id)
