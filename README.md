

<h1>StockRating</h1>

StockRating puts together a comprehensive stock market analysis, company stock description, and gainer, active and loser stocks every day (latest update). Search for a particular ticker and get the stock price, rating recommendation, cash flow, and growth of the company's financial statements

Features
Register to search company stock symbol (ticker)
Create different type of watchlist
Save ticker to watchlist
get company stock details, (financial statements)
Create, Update, Delete, info(Personal,Watchlist,Tickers)

Data:
from financialmodelingprep API.

Front End:
HTML templates using Jinja and WTForms for forms Design using Bootstrap, Font Awesome and raw CSS

Backend:
Routes and Models using Python3 and Flask SQLAlchemy as a database ORM Database using PostgreSQL



To get the code on your local machine, 
Local Environment:
1)create a PostgreSQL database 
2)set up a virtual environment(venv) in Python, 
3)get an API key from financialmodelingprep API.

> git clone https://github.com/SandroSandroo/StockRating.git
> python -m venv venv
> pip3 install -r requirements.txt
> source venv/bin/activate
> flask run
