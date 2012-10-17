#Many thanks to http://www.nomachetejuggling.com/2012/03/30/how-to-clean-up-your-chrome-bookmark-bar/

from urllib2 import urlopen, URLError

#try:
#    import ujson as json
#except ImportError:
#    print >> sys.stderr, '[WARN] Unable to load ujson, loading slower default json instead'
#    import json

#Trailing whitespace but in ujson means we'll have to skip this for now.
import json

import base64, fileinput

DEFAULT_FILEPATH = "missing-favicons.json"

#Chrome requires certain (different) MIME types than what servers will return.
MIME_CONVERSION = {
    #The official MIME type for ".ico" files
    "image/x-icon" : "image/vnd.microsoft.icon",
    "text/plain"   : "image/vnd.microsoft.icon",
}

DEFAULT_MIME = "image/vnd.microsoft.icon"



def render_icon(data):
    mime = data.headers['content-type']
    if mime in MIME_CONVERSION:
        mime = MIME_CONVERSION[mime]
    b64 = base64.b64encode(data.read())
    return "data:%s;base64,%s" % (mime, b64)

if __name__ == "__main__":
    import sys, os, fileinput
    data = json.loads("".join(fileinput.input()))

    for entry in data:
        if 'detected_domain' not in entry:
            break
        domain = entry['detected_domain']
        if domain is not None:
            try:
                u = urlopen("http://%s/favicon.ico" % domain)
                if u.code == 200 and entry['icon'] is None:
                    entry['icon'] = render_icon(u)
            except URLError:
                print >> sys.stderr, "[WARN] Unable to load domain %s" % domain

    print json.dumps(data, sort_keys=True, indent=4)