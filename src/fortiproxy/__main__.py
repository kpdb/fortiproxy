import os
import anyio
import pyotp
import asyncclick as click
from pyppeteer import launch
from pyppeteer.page import Page
from dotenv import load_dotenv


load_dotenv()


@click.command()
async def read_saml_cookie():
    browser = await launch(executablePath=os.getenv("BROWSER_PATH"), headless=True)
    page = await browser.newPage()
    totp = pyotp.TOTP(os.getenv("SECRET"))

    await page.goto(os.getenv("SAML_URL"))
    await anyio.sleep(0.5)

    await fill_email(page, os.getenv("EMAIL"))
    await fill_password(page, os.getenv("PASSWORD"))
    await fill_otp(page, totp.now())

    cookie_value = await read_cookie(page)
    print(cookie_value)

    await browser.close()


async def fill_email(page: Page, email: str) -> None:
    await page.waitForSelector("input[type=email]", visible=True)
    await page.type("input[type=email]", email)
    await page.click("input[type=submit]")
    await anyio.sleep(1.0)


async def fill_password(page: Page, password: str) -> None:
    await page.waitForSelector("input[type=password]", visible=True)
    await page.type("input[type=password]", password)
    await page.click("input[type=submit]")
    await anyio.sleep(1.0)


async def fill_otp(page: Page, token: str) -> None:
    await page.waitForSelector("input[name=otc]", visible=True)
    await page.type("input[name=otc]", token)
    await page.click("input[type=submit]")


async def read_cookie(page: Page) -> None:
    await page.waitForSelector("div.fortinet-grid-icon", visible=True)
    all_cookies = await page.cookies()
    cookie_value = next(
        cookie_data["value"]
        for cookie_data in all_cookies
        if cookie_data["name"] == "SVPNCOOKIE"
    )
    return cookie_value


def save_cookie(cookie_value: str) -> None:
    with open("/vpn/token", "w") as f:
        f.write(cookie_value)


if __name__ == "__main__":
    read_saml_cookie(_anyio_backend="asyncio")
