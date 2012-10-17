#Many thanks to http://www.nomachetejuggling.com/2012/03/30/how-to-clean-up-your-chrome-bookmark-bar/

from HTMLParser import HTMLParser
import hashlib, os

from urllib2 import urlopen

#try:
#    import ujson as json
#except ImportError:
#    print >> sys.stderr, '[WARN] Unable to load ujson, loading slower default json instead'
#    import json

#Trailing whitespace but in ujson means we'll have to skip this for now.
import json

def get_tlds():
    if get_tlds.cache is not None:
        return get_tlds.cache

    if not os.path.exists('tlds-alpha-by-domain.txt'):
        with open('tlds-alpha-by-domain.txt', 'wb') as f:
            f.readline() #Skip the initial comment line
            f.write(urlopen("http://data.iana.org/TLD/tlds-alpha-by-domain.txt").read())

    with open("tlds-alpha-by-domain.txt", 'rb') as f:
        get_tlds.cache = [line.strip() for line in f]
        return get_tlds.cache
get_tlds.cache = None

class BookmarkHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tlds = get_tlds()
        self.in_name = False
        self.hasher = hashlib.md5

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.defer_attrs = dict(attrs)
            attrs = self.defer_attrs
            if "icon" not in attrs and attrs['href'].startswith('javascript'):
                self.in_name = True
                print "    {"

    def handle_endtag(self, tag):
        if self.in_name:
            attrs = self.defer_attrs
            if "icon" not in attrs and attrs['href'].startswith('javascript'):
                self.in_name = True
                s = attrs['href'].split("//")
                detected_domain = None
                for v in s[1:]:
                    c = v.split("/")[0]
                    e = c.split(".")[-1]
                    if e.upper() in self.tlds:
                        detected_domain = c
                        break
                #For sanity's sake, keep this in sort order.
                print '        "detected_domain": %s,' % json.dumps(detected_domain)
                print '        "hash": %s,' % json.dumps(self.hasher(attrs['href']).hexdigest())
                print '        "icon": %s,' % json.dumps(None)
                print '        "name": %s,' % json.dumps(self.data)
                print '        "raw_attrs": %s,' % json.dumps(attrs)
                print '        "strip_name": %s' % json.dumps(True)
                print "    },"
        self.in_name = False
        self.defer_attrs = None
        self.data = None
    def handle_data(self, data):
        if self.in_name:
            self.data = data

### Begin the utility chunk of this script...



DEFAULT_FILEPATH = "userdata/bookmarks.unprocessed.html"

if __name__ == "__main__":
    import sys, os, fileinput
    get_tlds()

    print '['
    # instantiate the parser and fed it some HTML
    parser = BookmarkHTMLParser()
    for line in fileinput.input():
        parser.feed(line)
    print '{}]' #Small hack to remove the trailing comma problem.
