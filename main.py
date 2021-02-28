from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import smtplib

# Path for Selenium binary. The binary is browser/ operating system specific
# (see readme for more details)
DRIVER_PATH = r"lib/chromedriver-win.exe"

VANGUARD_URL = "https://www.vanguardinvestor.co.uk/what-we-offer/all-products"

# If an email address is provided, the program will log into the email
# using smtplib and send an email containing the results of the webscraping
EMAIL_ADDRESS = "example@example.com"
EMAIL_PASSWORD = "exampleexample"


class FundPriceScraper:

    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.fund = {
            'name': '',
            'property_element': '',
            'pct_change': 1000,
            'holdings': []
        }

    def find_cheapest_fund(self):
        self.driver.get(VANGUARD_URL)
        self.driver.maximize_window()

        # Toggles on extra fund details (inc price information)
        toggle_switch = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, ".toggleSwitchContainer")
            )
        )
        toggle_switch.click()

        # Finds the fund with the largest percentage price drop
        funds = self.driver.find_elements_by_css_selector(".EQUITY tr")
        for fund in funds:
            try:
                fund_pct_change = fund.find_element_by_css_selector(
                    ".percentChange .value"
                ).get_attribute("textContent")
            except NoSuchElementException:
                pass
            else:
                fund_pct_change = float(fund_pct_change.replace('%', ''))
                if fund_pct_change < self.fund["pct_change"]:
                    fund_details = fund.find_element_by_css_selector(
                        ".linkMargin"
                    )
                    self.fund['name'] = fund_details.get_attribute(
                        "textContent"
                    )
                    self.fund['details'] = fund_details
                    self.fund['pct_change'] = fund_pct_change
        print(f"{self.fund['name']} experienced the "
              f"largest daily drop: {self.fund['pct_change']} %")

    def extract_portfolio_data(self):
        self.fund['details'].click()

        # Switches to the portfolio data tab for the fund
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, ".portfolioData span")
            )).click()

        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, "#holdingDetailsEquity tbody tr")
            ))

        holdings = self.driver.find_elements_by_css_selector(
            "#holdingDetailsEquity tbody tr"
        )

        # Stores details of the funds largest 3 holdings in a dict
        for stock in holdings[:3]:
            self.fund["holdings"].append({
                'name': stock.find_element_by_css_selector('.name'),
                'pct': stock.find_element_by_css_selector('.marketValPercent')
            })

    def create_email_content(self):
        message = (
            f"Subject: Vanguard Fund Price Alert !\n\n"
            f"{self.fund['name']} experienced the largest daily"
            f" drop yesterday: {self.fund['pct_change']} %"
            f"\n\nThe largest 3 holdings of this fund are:")

        for stock in self.fund["holdings"]:
            message += (
                f"\n{stock['name'].get_attribute('textContent')}"
                f" - {stock['pct'].get_attribute('textContent').strip()}"
            )
        return message

    def shutdown_webdriver(self):
        self.driver.quit()


def send_email(message_content):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        try:
            connection.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
        except smtplib.SMTPAuthenticationError:
            print("Email not sent, authentication failed")
        else:
            connection.sendmail(
                from_addr=EMAIL_ADDRESS,
                to_addrs=EMAIL_ADDRESS,
                msg=message_content.encode('utf-8')
            )


if __name__ == "__main__":
    fund_price_scraper = FundPriceScraper(driver_path=DRIVER_PATH)
    fund_price_scraper.find_cheapest_fund()
    fund_price_scraper.extract_portfolio_data()
    send_email(message_content=fund_price_scraper.create_email_content())
    fund_price_scraper.shutdown_webdriver()
