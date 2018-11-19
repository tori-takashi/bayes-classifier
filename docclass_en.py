import re
#regular expression

import math
import sys

def getwords(doc):
    splitter = re.compile('\\W+')
    words =[s.lower() for s in splitter.split(doc) if len(s)>2 and len(s) < 20]
    return dict([(w,1) for w in words])

print( getwords(sys.argv[1]) )
