from scraper import HatchfulScraper
import csv


"""
Some failures might happen due to not proper loading or too many requests.
Script will add every logo that has been created and you can resume at any time.
Try not to create too many logos in a row or use a random proxy if you have to.

Logos will be stored in "logos" directory.
Add your csv file named "list.csv" (or change the name in the code) where main.py is placed.

If you use windows, Place your chromedriver based on the chrome version installed on your windows.
It should be named chromedriver.exe
You should change the driver name in scraper.py:26 if running linux.
Download driver: https://sites.google.com/a/chromium.org/chromedriver/downloads
"""


if __name__ == "__main__":
    with open("list.csv") as f:
        r = csv.reader(f)
        rows = list(r)
    f.close()
    processed = 1
    while processed < len(rows):
        # Skip the rows that already have a logo
        if rows[processed][2] != "":
            print(f'{rows[processed][0]} has a logo, skipping ...')
        else:
            print(f'Creating logo for {rows[processed][0]} with slogan "{rows[processed][1]}":')
            tries = 0
            path = ""
            # Task might fail sometimes due to not loading properly
            # Try 5 times max if it failed
            while tries < 5:
                try:
                    scraper = HatchfulScraper(rows[processed][0], rows[processed][1])
                    path = scraper.create()
                    tries = 10
                except:
                    tries += 1
            rows[processed][2] = path
            with open("list.csv", "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            f.close()
        processed += 1
