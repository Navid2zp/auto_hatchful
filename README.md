# auto_hatchful
Bypass Shopify's bot detection and create bulk logos using hatchful logo maker.

## Requirements
You need chrome driver to run this script. Download the driver here: https://sites.google.com/a/chromium.org/chromedriver/downloads

Driver file should be located in the root of the script (next to `main.py`):

```
|-- auto_hatchful
        |-- main.py
        |-- scraper.py
        |-- chromedriver.exe # or chromedriver depending on your OS
```

## Usage
Edit the `list.csv` and add as many "name" and "slogan" you want (leave the logo empty) and then run the script: `python main.py`

The script will create each logo and will place them in the `logos` folder.

The script will skip any row in `list.csv` file with a logo path so you can run the script multiple times and it will ignore all the ones with logo path and only creates a logo for the ones without a path.

### Using FireFox driver
You can use FireFox driver by overriding the [`_browser`](https://github.com/Navid2zp/auto_hatchful/blob/b8167cf1dcd3aca3329ab7bac96796e3640d55d3/scraper.py#L27) variable in [`__init__`](https://github.com/Navid2zp/auto_hatchful/blob/b8167cf1dcd3aca3329ab7bac96796e3640d55d3/scraper.py#L19) function in [`HatchfulScraper`](https://github.com/Navid2zp/auto_hatchful/blob/b8167cf1dcd3aca3329ab7bac96796e3640d55d3/scraper.py#L18) class located in [`scraper.py`](https://github.com/Navid2zp/auto_hatchful/blob/master/scraper.py) file.

### Script behavior

#### Delays and random movements

There are random periods of sleep and mouse movements to avoid being detected as a bot. You can probably change and lower the times to make the script work faster but you need to try different durations to get to the minimum delay numbers/durations.

#### Change number of tries for failure

The script will retry 5 times if creating a logo fails. You can change the number of tries [here](https://github.com/Navid2zp/auto_hatchful/blob/b8167cf1dcd3aca3329ab7bac96796e3640d55d3/main.py#L36) located in `main.py` file.

License
----

MIT
