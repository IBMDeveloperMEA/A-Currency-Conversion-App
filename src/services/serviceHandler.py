from urllib.request import urlopen, Request  # noqa: 401
from urllib.error import HTTPError  # noqa: 401
import json
import logging

#logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

BASE_URL_ENDPOINT = "http://data.fixer.io/api/"
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class NotFoundException(Exception):
    pass


def __callExtRestEndPoint(url):
    request = Request(url)
    try:
        response = urlopen(request)
    except HTTPError as httpex:
        raise NotFoundException(httpex.reason)

    data = json.loads(response.read())
    return data


def getCurrencyExchangeRates(timeIndicator="latest"):
    currencyUrl = "{}{}".format(BASE_URL_ENDPOINT, timeIndicator)
    data = __callExtRestEndPoint(currencyUrl + "?access_key=dc058dc915aa4846e04c749d3567fe9c")
    return data


def getCurrencyExchangeRate(
    countryCurrencyCode, baseCode="EUR", timeIndicator="latest"
):

    countryCurrencyCode = countryCurrencyCode.upper()
    baseCode = baseCode.upper()

    currencyUrl = "{}{}?symbols={}".format(BASE_URL_ENDPOINT, timeIndicator, baseCode)
    data = __callExtRestEndPoint(currencyUrl + "&access_key=dc058dc915aa4846e04c749d3567fe9c")
    logging.debug("URL = " + currencyUrl + "&access_key=dc058dc915aa4846e04c749d3567fe9c")
    logging.debug("data = " + json.dumps(data))
    logging.debug("countryCurrencyCode = " + countryCurrencyCode)
    logging.debug("baseCode = " + baseCode)

    return data["rates"][baseCode]


def convertCurrency(
    fromValue, fromCurrencyCode, toCurrencyCode, historicalDate="latest"
):
    exchangeRate = getCurrencyExchangeRate(
        toCurrencyCode, fromCurrencyCode, historicalDate
    )

    return fromValue * exchangeRate
