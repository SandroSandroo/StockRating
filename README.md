

<h1>StockRating</h1>

https://stockrating.herokuapp.com/
<p>200 API requests per day<p>

<h5>StockRating puts together a comprehensive stock market analysis, company stock description, and gainer, active and loser stocks every day (latest update). Search for a particular ticker and get the stock price, rating recommendation, cash flow, and growth of the company's financial statements</h5>

<h3>Features</h3>
<ul>
<li>Register to search company stock symbol (ticker)</li>
<li>Create different type of watchlist</li>
<li>Save ticker to watchlist</li>
<li>get company stock details, (financial statements)</li>
<li>Create, Update, Delete, info(Personal,Watchlist,Tickers)</li>
</ul>

<h3>Data:</h3>
from financialmodelingprep API.
<a href="https://site.financialmodelingprep.com/developer/docs">FMP API</a>

<h3>Front End:</h3>
HTML templates using Jinja and WTForms for forms Design using Bootstrap, Font Awesome and raw CSS

<h3>Backend:</h3>
Routes and Models using Python3 and Flask SQLAlchemy as a database ORM Database using PostgreSQL

<h3>Deployment:</h3>
Heroku


<h3>To get the code on your local machine</h3> 
<h4>Environment:<h4>
<ol>
<li>create a PostgreSQL database </li>
<li>set up a virtual environment(venv) in Python, </li>
<li>get an API key from financialmodelingprep API.</li>
</ol> 
<ul>
 <li> git clone https://github.com/SandroSandroo/StockRating.git</li>
 <li>python -m venv venv</li>
 <li>source venv/bin/activate</li>
 <li>pip3 install -r requirements.txt</li>
 <li>python3 -m flask run</li>
</ul>


<h4>Because Financial Modeling Prep API Documentation plan is free, sometimes data does not return to the correct object, which I describe as an ERROR! will be
 <p>"API response ERROR (under CONSTRUCTION sorry)"</p>
 
</h4>

![1](/img/DB_disagne_schema.png)
![2](/img/main.png)
![3](/img/register.png)
![4](/img/home.png)
![5](/img/ticker.png)
![6](/img/ticker_in_wtlist.png)
![7](/img/add_ticker.png)
![8](/img/Watchlist.png)
![9](/img/profile.png)

