from enum import Enum


class Spiders(str, Enum):
    TJAL = "spider_tjal"
    TJCE = "tjce_spider"


class Tribunais(str, Enum):
    TJAL = "02"
    TJCE = "06"