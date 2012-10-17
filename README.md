Chrome-Faviconlets
==================

Simple Python script to let you (easily) apply favicons to bookmarklets.

Credit to http://www.nomachetejuggling.com/2012/03/30/how-to-clean-up-your-chrome-bookmark-bar/ for inspiration and explanation.

Usage
=====

Export your Chrome bookmark HTML and do the following:

    python show-missing-favicons.py userdata/bookmarks.unprocessed.html | python autodetect-favicons.py | python render-importable-html.py > userdata/import-me.html

This will create `userdata/import-me.html` which can be imported in to Chrome. Importing this file in to Chrome's bookmark manager will create a new folder called "Imported" (or "Imported (1)" if it already exists, etc.) which will contain copies of all bookmarklets for which favicon auto-detection succeeded.

Chrome (luckily) does not allow for two bookmarks with identical link data (in this case, javascript code) to have independent favicons; by importing these copies all of the original bookmarklets will have icons set with no extra work. It is safe to delete the "Imported" folder - note that Chrome Bookmark Manager will not necessarily show the icons until reloaded but the icons should be immediately visible on the bookmark bar.

Future Work
===========

* Improved auto-detection of favicons
 * Potentially build a library of popular replacements
 * Support meta tag declaration of favicon as well as `favicon.ico`
* More favicon sources
 * Support for popular icon libraries such as Silk
 * Support for importing local icons disk
* Better integration
 * External graphical editor?
 * Automating export/import/delete "Imported" folder
  * Selenium?
   * Doesn't seem to be designed for this
  * AutoIt or Automator?
   * Windows or Mac only
 * Chrome extension
  * http://developer.chrome.com/extensions/bookmarks.html has no support for icons
  * http://code.google.com/p/chromium/issues/detail?id=59519 tracks this
 * Direct editing of profile?
  * Requires Chrome to be closed
  * Requires re-calculating checksums
* Support for non-bookmarklet bookmarks
* Better documentation

Near-Term Issues
================

* No threading of icon downloads.
* Minimal caching; will download favicons many times if they are used by many bookmarklets.
* Ignores hash and emits multiple (useless) copies of the same bookmarklet if it is present many times in the source.
* Manual rendering of json is hackish and inelegant.
* ujson dies if there is a trailing whitespace in input; currently using builtin json to circumvent this.

Included Scripts
================

Each tool has a separate, simple, function.

show-missing-favicons.py
------------------------

Consumes a bookmark export file and produces a JSON dump of every bookmarklet without an icon. Does some crude matching to see if there's a source domain hiding in the bookmarklet. For example, here's the "popup with tags" bookmarklet from http://pinboard.in/howto/:

    javascript:q%3Dlocation.href%3Bif(document.getSelection)%7Bd%3Ddocument.getSelection()%3B%7Delse%7Bd%3D%27%27%3B%7D%3Bp%3Ddocument.title%3Bvoid(open(%27https://pinboard.in/add%3Fshowtags%3Dyes%26url%3D%27%2BencodeURIComponent(q)%2B%27%26description%3D%27%2BencodeURIComponent(d)%2B%27%26title%3D%27%2BencodeURIComponent(p),%27Pinboard%27,%27toolbar%3Dno,scrollbars%3Dyes,width%3D750,height%3D700%27))%3B

This contains `//pinboard.in/` - and `.in` is a valid TLD - so the autodetected domain is `pinboard.in`.

Bookmarklets are ignored if they already have an icon.

The output (JSON) contains for-future-use fields.

autodetect-favicons.py
----------------------

Consumes the JSON product of `show-missing-favicons.py` in order to download favicons.

The output is the same as `show-missing-favicons.py` but the "icon" field will be populated with the detected domain's favicon.

Currently lacks both threading and caching; may also download the same favicon several times as a result.

render-importable-html.py
-------------------------

Consumes the JSON product of `autodetect-favicons.py` and produces an importable HTML bookmark file. Only bookmarklets with icons will be present in the output.
