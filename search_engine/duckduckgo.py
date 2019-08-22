#!/usr/bin/env python3

from bs4 import BeautifulSoup
from urllib.parse import urlencode

import os
import sys
import urllib.request

def eprint(*args, **kwargs):
    """ Just like the print function, but on stderr
    """
    print(*args, file=sys.stderr, **kwargs)



def has_class(wanted_class):
    def has_class_impl(tag):
        if tag.name != 'div': return False

        c = tag.get('class')
        return c and wanted_class in c

    return has_class_impl



def duckduckgo_raw_results(query):
    duckduckgo = 'https://duckduckgo.com/html/?' + urlencode({ 'q' : query })  + '&t=ffab&ia=videos'
    eprint(duckduckgo)
    soup = BeautifulSoup(urllib.request.urlopen(duckduckgo), 'html.parser')
    results_div = soup.find(has_class('results'))
    return results_div.find_all(has_class('result'), recursive=False)
    # is this a typo? "recusive"?  



def ask_duckduckgo(query):
    results = []
    for raw_results in duckduckgo_raw_results(query):
        result = {}
        def add_result(tag):
            c = tag.get('class')
            if not c: return False

            if tag.name == 'h2' and 'result__title' in c:
                result['title'] = tag
            elif tag.name == 'span' and 'result__icon' in c:
                result['icon'] = tag
            elif tag.name == 'a' and 'result__snippet' in c:
                result['snippet'] = tag

            return False
        raw_results.find_all(add_result, recursive=True);
        results.append(result)
        #print('results=',results)
    return results



def main(argv=None):
    prgname = os.path.basename(__file__) if '__file__' in globals() else 'prg'
    if argv is None:
        argv = sys.argv
   
    query = ' '.join(argv[1:])
    #print('query=',query)

    for result in ask_duckduckgo(query):
        print(' ==============================\n')
        print(result)
        print(' @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n')

    return 0

if __name__ == "__main__":
    sys.exit(main())
