from urllib.request import urlopen
from urllib.error import HTTPError
import json

from flask.helpers import flash

API_KEY = "56958883a43687bf39a63bd15c3ccec7"
BASE_URL = "https://financialmodelingprep.com/api/v3"


""" financialmodelingprep.com/api method for python """

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``,
    parse it as JSON and return the object.
    Parameters
    ----------
    url : str
    Returns
    -------
    dict
    """
    
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)


""" class for api,  url"""

class APIFunctions():
    

    def __init__(self):

        self.API_KEY=API_KEY
    

    def get_ticker(self, ticker):

        """Show basic ticker quote and info"""   
        start_url = f"{BASE_URL}/company/discounted-cash-flow/{ticker}?apikey={self.API_KEY}"
        url = start_url.replace(" ", "")
        try:
            data = get_jsonparsed_data(url)
            
        except HTTPError:
            return flash("invalid request")
        return data


    def get_rating(self, symbol):
        '''
        Show rating and recomedation
        '''
        url = f"{BASE_URL}/rating/{symbol}?apikey={self.API_KEY}"
        try:
            data = get_jsonparsed_data(url)
        except HTTPError:
            return ("HTTPError invalid request")
        return data


    def get_statement(self, symbol):
        '''
        Show statement anf financial growth
        '''
        url = f"{BASE_URL}/financial-growth/{symbol}?limit=1&apikey={self.API_KEY}"
        try:
            data = get_jsonparsed_data(url)
        except HTTPError:
            return flash("HTTPError invalid request")
        return data


    def get_most_gainers(self):
        """ 
        list most gainer stocks 
        """
        url = f"{BASE_URL}/stock/gainers?apikey={self.API_KEY}"
        try:
            data = get_jsonparsed_data(url)
        except HTTPError:
            return flash("HTTPError invalid request")
        return data


    def get_most_losers(self):
        """ 
        list most gainer stocks 
        """
        url = f"{BASE_URL}/stock/losers?apikey={self.API_KEY}"
        try:
            data = get_jsonparsed_data(url)
        except HTTPError:
            return flash("HTTPError invalid request")
        return data

    
    def get_most_actives(self):
        """ 
        list most gainer stocks 
        """
        url = f"{BASE_URL}/stock/actives?apikey={self.API_KEY}"
        try:
            data = get_jsonparsed_data(url)
        except HTTPError:
            return flash("HTTPError invalid request")
        return data
