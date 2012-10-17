#Many thanks to http://www.nomachetejuggling.com/2012/03/30/how-to-clean-up-your-chrome-bookmark-bar/

from urllib2 import urlopen, URLError

#try:
#    import ujson as json
#except ImportError:
#    print >> sys.stderr, '[WARN] Unable to load ujson, loading slower default json instead'
#    import json

#Trailing whitespace but in ujson means we'll have to skip this for now.
import json

if __name__ == "__main__":
    import sys, os, fileinput
    data = json.loads("".join(fileinput.input()))

    print '''<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>'''

    for entry in data:
        if 'icon' not in entry:
            break
        icon = entry['icon']
        #No point re-rendering empties!
        if icon is not None:
            href = entry['raw_attrs']['href']
            icon = entry['icon']
            add_date = entry['raw_attrs']['add_date']
            if entry['strip_name'] == False:
                name = entry['name']
            else:
                name = None
            if name is None:
                name = ""
            print '''<DT><A HREF="%s" ADD_DATE="%s" ICON="%s">%s</A>''' % (href, add_date, icon, name)

    print '''</DL><p>'''