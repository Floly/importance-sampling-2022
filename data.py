from datetime import datetime, timedelta

import gdown
import pandas as pd

STOCK_URL = 'https://drive.google.com/file/d/1lLQV4oc30mo1_m39p4JXlpd1gV6pLw6A/view?usp=sharing'
COMMODITIES_URL = 'https://drive.google.com/file/d/1GFq1jcV00BjFEa7hmZSO1xD7K4j4gv3O/view?usp=sharing'
CRYPTO_URL = 'https://drive.google.com/file/d/1NLvOCVyvUkVwYBeLL7DjRKlWzQvHh46z/view?usp=sharing'


def previous_date(date):
    tmp = datetime.strptime(date, '%m/%d/%Y')
    tmp += timedelta(days=-1)
    return tmp.strftime('%m/%d/%Y')


def get_portfolio(prices, assets, weights, from_date_new, to_date):
    prices.index = pd.to_datetime(prices.index)
    prices_assets = prices.loc[from_date_new:to_date, assets]
    cnt = 0
    for column in prices_assets:
        prices_assets.loc[:, column] = prices_assets[column] * weights[cnt]
        cnt += 1
    prices_assets['price'] = prices_assets.loc[:, :].sum(axis=1)
    return prices_assets


def get_returns(portfolio, from_date_new):
    returns = []
    for i in range(1, len(portfolio)):
        day_return = (portfolio['price'][i] - portfolio['price'][i - 1]) / portfolio['price'][i - 1]
        returns.append(day_return)
    portfolio = portfolio.drop(index=[from_date_new])
    portfolio['return'] = returns
    return portfolio['return']


def stocks_returns(assets, weights, from_date, to_date):
    gdown.download(STOCK_URL, '_shares.csv', fuzzy=True)
    stock_prices = pd.read_csv('_shares.csv', index_col='Date')
    from_date_new = previous_date(from_date)
    portfolio = get_portfolio(stock_prices, assets, weights, from_date_new, to_date)
    return get_returns(portfolio, from_date_new)


def commodities_returns(assets, weights, from_date, to_date):
    gdown.download(COMMODITIES_URL, '_commodities.csv', fuzzy=True)
    commodities_prices = pd.read_csv('_commodities.csv', index_col='Date')
    from_date_new = previous_date(from_date)
    portfolio = get_portfolio(commodities_prices, assets, weights, from_date_new, to_date)
    return get_returns(portfolio, from_date_new)


def cryptocurrencies_returns(assets, weights, from_date, to_date):
    gdown.download(CRYPTO_URL, '_crypto.csv', fuzzy=True)
    crypto_prices = pd.read_csv('_crypto.csv', index_col='Date')
    new_from_date = previous_date(from_date)
    portfolio = get_portfolio(crypto_prices, assets, weights, new_from_date, to_date)
    return get_returns(portfolio, new_from_date)