from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import sys

app_id = "dj0zaiZpPVd3OE52UEJhZlRVTSZzPWNvbnN1bWVyc2VjcmV0Jng9ZGI-"
page_url = "https://jlp.yahooapis.jp/MAService/V1/parse"

def split( sentence, app_id=app_id, results="ma", filter='1|2|4|5|9|10'):
    ret = []
    sentence = quote_plus(sentence.encode("utf-8"))
    query = "%s?appid=%s&results=%s&uniq_filter=%s&sentence=%s" % \
            (page_url,app_id,results,filter,sentence)
    soup = BeautifulSoup(urlopen(query), features="lxml")
    try:
        return [l.surface.string for l in soup.ma_result.word_list]
    except:
        return []

print(split(sys.argv[1]))
