# lonelyplanet-water-scrape

A commissioned project to lonelyplanet's tpa water for cities and countries.

## Installation

Execute
```
pip install -r requirements.txt
```

Install chromedriver [here](https://sites.google.com/a/chromium.org/chromedriver/) and add to your environment path.

## Running
Execute
```
python main.py
```

## Data Notes
Some cities seem to not report water quality so they're not listed on the csv. Example [here](https://www.lonelyplanet.com/cambodia/siem-reap/health)

Some countries also don't report water quality. Example [here](https://www.lonelyplanet.com/syria/health)

Commas are encoded as %2C to preserve .csv