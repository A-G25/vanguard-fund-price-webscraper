# Vanguard Fund Price Scraper

This program scrapes investment fund information from the Vanguard UK website
and emails the user to let them know which fund experienced the largest
drop in price (or smallest increase) over the previous day and what the 3 
largest holdings in the fund are.

## How the Application Works
1. Initialises a Selenium webdriver and browses to the Vanguard UK website: 
https://www.vanguardinvestor.co.uk/what-we-offer/all-products
1. Scrapes the investment fund prices and identifies which fund has experienced the largest
daily % drop (or smallest increase) in price.
1. Accesses the portfolio information page for the fund and extracts a lists of the
3 biggest holdings.
1. Sends an email to the user containing the funds name, % daily price change and 
3 largest holdings.
<br>

|            Vanguard Investment Funds:                   |               Email Notification:                |
| ------------------------------------------------------- | ------------------------------------------------ |
| <img src="/images/vanguard-fund-prices.png">            |<img src="/images/email-notification.png">       |

## Using the Application
* Download main.py or clone this repository.
* Install Selenium using pip.
* Download the correct Selenium binary for the operating system and browser you wish to use:
 <https://www.selenium.dev/documentation/en/webdriver/driver_requirements/>
* If you wish to receive email notifications, then provide your email address and password
using the variables in main.py (EMAIL_ADDRESS, EMAIL_PASSWORD).
* Run main.py to commence the webscraping.


## Supporting Libraries and APIs
* Selenium (for browser automation and webscraping): https://www.selenium.dev/documentation/en/webdriver/  