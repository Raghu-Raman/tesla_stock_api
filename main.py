import requests
from datetime import datetime, timedelta
import os
from twilio.rest import Client

account_sid = "AC3262777e01cb1e81898a2c5433e0dc4f"
auth_token = "14c83ffdebf4d2638f2c5fb290dbb7a8"
STOCK = "TSLA"
COMPANY_NAME = "Tesla"
yesterday = datetime.now() - timedelta(1)
day_before_yesterday = datetime.now() - timedelta(2)
yesterday_date = yesterday.strftime('%Y-%m-%d')
# print(type(yesterday.strftime('%Y-%m-%d')))
day_before_yesterday_date = day_before_yesterday.strftime('%Y-%m-%d')
# print(day_before_yesterday_date)
STOCK_ENDPOINT = "https://www.alphavantage.co/query"

stock_param = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "interval": "60min",
    "apikey": "3GEOSFKKB9Q77I1Z"
}
# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_response = requests.get(STOCK_ENDPOINT, stock_param)
# print(stock_response.status_code)
stock_data = stock_response.json()
stock_sum = 0
for key, value in (stock_data['Time Series (Daily)'][yesterday_date].items()):
    if key != "5. volume":
        stock_sum += float(value)
yesterday_stock_average = stock_sum / 4
stock_sum = 0
for key, value in (stock_data['Time Series (Daily)'][day_before_yesterday_date].items()):
    if key != "5. volume":
        stock_sum += float(value)
day_before_yesterday_stock_average = stock_sum / 4
percentage_increase = ((day_before_yesterday_stock_average - yesterday_stock_average) /day_before_yesterday_stock_average) * 100
# print(yesterday_stock_price)

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
NEWS_ENDPOINT = "https://newsapi.org/v2/top-headlines"
news_api_key = '76f508ce4b924b65a8d487871aba5905'
news_param = {
    "country": "us",
    "q": COMPANY_NAME,
    "pageSize": 3,
    "apiKey": news_api_key
}

news_response = requests.get(NEWS_ENDPOINT, news_param)
news_data = news_response.json()
news_source = []
news_title = []
news_url = []
news_description = []
for i in range(len(news_data['articles'])):
    news_source.append(news_data['articles'][i]['source']['name'])
    news_title.append(news_data['articles'][i]['title'])
    news_description.append(news_data['articles'][i]['description'])
    news_url.append(news_data['articles'][i]['url'])
# print(news_title)
# print(news_source)
# print(news_url)
# print(news_description)

# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
client = Client(account_sid, auth_token)
if percentage_increase > 0:
    message = client.messages \
        .create(
            body=f"Stock value of Tesla {yesterday_date}={round(yesterday_stock_average,2)},Stock value of Tesla on {day_before_yesterday_date}={round(day_before_yesterday_stock_average,2)},There is an {round(percentage_increase,2)} increase📈️",
            from_="+16514096517",
            to="+918870668292"
            )
else:
    message = client.messages \
        .create(
            body=f"Stock value of Tesla {yesterday_date}={round(yesterday_stock_average,2)},Stock value of Tesla on {day_before_yesterday_date}={round(day_before_yesterday_stock_average,2)},There is an {round(percentage_increase,2)} decrease📉️",
            from_="+16514096517",
            to="+918870668292"
            )
    print(message.status)