#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
import tempfile
import requests_cache
from requests import Request
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class Market(object):

	_session = None
	__DEFAULT_BASE_URL = 'https://pro-api.coinmarketcap.com/v1/'
	__SANDBOX_URL = 'https://sandbox-api.coinmarketcap.com/v1/' 
	__DEFAULT_TIMEOUT = 30
	__TEMPDIR_CACHE = True
	__API_KEY = "API Key Required"

	def __init__(self, base_url = __DEFAULT_BASE_URL, request_timeout = __DEFAULT_TIMEOUT, tempdir_cache = __TEMPDIR_CACHE, api_key = __API_KEY, sandbox = False, sandbox_url = __SANDBOX_URL):
		if sandbox :
			self.base_url = sandbox_url
		else: 
			self.base_url = base_url
		self.api_key = api_key
		self.request_timeout = request_timeout
		self.cache_filename = 'coinmarketcap_cache'
		self.cache_name = os.path.join(tempfile.gettempdir(), self.cache_filename) if tempdir_cache else self.cache_filename

	@property
	def session(self):
		if not self._session:
			self._session = requests_cache.core.CachedSession(cache_name=self.cache_name, backend='sqlite', expire_after=120)
			self._session.headers.update({'Accepts': 'application/json'})
			self._session.headers.update({'X-CMC_PRO_API_KEY': self.api_key})
		return self._session

	def __request(self, endpoint, params):
		try:
			response_object = self.session.get(self.base_url + endpoint, params = params, timeout = self.request_timeout)
			response = json.loads(response_object.text)
			if isinstance(response, list) and response_object.status_code == 200:
				response = [dict(item, **{u'cached':response_object.from_cache}) for item in response]
			if isinstance(response, dict) and response_object.status_code == 200:
				response[u'cached'] = response_object.from_cache

		except (ConnectionError, Exception, Timeout, TooManyRedirects) as e:	
			return e

		return response

	def listings(self):
		"""
		This endpoint displays all active cryptocurrency listings in one call. Use the
		"id" field on the Ticker endpoint to query more information on a specific
		cryptocurrency.
		"""

		response = self.__request('cryptocurrency/listings/latest', params=None)
		return response

	def ticker(self, currency="", **kwargs):
		"""
		This endpoint displays cryptocurrency ticker data in order of rank. The maximum
		number of results per call is 100. Pagination is possible by using the
		start and limit parameters.

		GET /ticker/

		Optional parameters:
	    (int) start - return results from rank [start] and above (default is 1)
	    (int) limit - return a maximum of [limit] results (default is 100; max is 100)
	    (string) convert - return pricing info in terms of another currency.
	    Valid fiat currency values are: "AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK",
	    "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN",
	    "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY",
	    "TWD", "ZAR"
	    Valid cryptocurrency values are: "BTC", "ETH" "XRP", "LTC", and "BCH"

		GET /ticker/{id}

		Optional parameters:
		(string) convert - return pricing info in terms of another currency.
    	Valid fiat currency values are: "AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK",
    	"DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN",
    	"MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY",
    	"TWD", "ZAR"
    	Valid cryptocurrency values are: "BTC", "ETH" "XRP", "LTC", and "BCH"
		"""

		params = {}
		params.update(kwargs)

		# see https://github.com/barnumbirr/coinmarketcap/pull/28
		if currency:
			currency = str(currency) + '/'

		response = self.__request('ticker/' + currency, params)
		return response

	def stats(self, **kwargs):
		"""
		This endpoint displays the global data found at the top of coinmarketcap.com.

		Optional parameters:
		(string) convert - return pricing info in terms of another currency.
		Valid fiat currency values are: "AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK",
		"DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN",
		"MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY",
		"TWD", "ZAR"
		Valid cryptocurrency values are: "BTC", "ETH" "XRP", "LTC", and "BCH"
		"""

		params = {}
		params.update(kwargs)
		response = self.__request('global/', params)
		return response
