#!/usr/bin/python

# yt2pod-proxy.py
#  by Mike Melanson (mike -at- multimedia.cx)
# Part of the YouTube2Podcast project.

import BaseHTTPServer
import commands
import getopt
import json
import os
import requests
import sys

import process_rss

DEFAULT_HTTP_PORT = 54321
FEED_BASE_URL = "https://www.youtube.com/feeds/videos.xml?"
CONF_JSON = "yt2pod.conf.json"

feed_list = {}

def get_yt_rss_feed(req_path):
    if req_path.startswith('/videos/'):
        feed_url = FEED_BASE_URL + "channel_id=" + req_path[8:]
    else:
        feed_url = FEED_BASE_URL + "playlist_id=" + req_path[10:]
    r = requests.get(feed_url)
    return (r.status_code, r.text)

class YT2PodHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            # list index
            html = "<html><head><title>Feed List</title></head>\n"
            html += "<body><ul>"
            for feed in feed_list:
                html += "<li><a href='/" + feed['type'] + "/" + feed['uid'] + "'>" + feed['name'] + "</a></li>\n"
            html += "</body></html>"

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html)
            
        elif self.path.startswith('/videos/') or self.path.startswith('/playlist/'):
            (status_code, rss_xml) = get_yt_rss_feed(self.path)
            self.send_response(status_code)
            self.send_header("Content-type", "text/xml")
            self.end_headers()
            if (status_code == 200):
                self.wfile.write(process_rss.transform_rss_xml(rss_xml.encode('utf8')))

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("Path '%s' does not exist" % (self.path))

def run(port,
        server_class=BaseHTTPServer.HTTPServer,
        handler_class=YT2PodHandler):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print "YT2Pod server running on port %d... (Ctrl-C to exit)" % (port)
    httpd.serve_forever()


def usage():
    print """USAGE: yt2pod-server.py <options>
  -h, --help: Print this message
  -p, --port=[number]: Port on which to run the HTTP server
  -c, --cache: Request to pre-process a feed into the cache
"""

if __name__ == '__main__':

    port = DEFAULT_HTTP_PORT
    if os.path.exists(CONF_JSON):
        feed_list = json.loads(open(CONF_JSON, "r").read())

    # process command line arguments
    opts, args = getopt.getopt(sys.argv[1:], "chp:r", ["cache", "help", "port=", "refresh"])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-p", "--port"):
            try:
                port = int(arg)
            except ValueError:
                print "Invalid port number"
                sys.exit()
        elif opt in ("-c", "--cache", "-r", "--refresh"):
            if len(feed_list) == 0:
                print "Feed list is empty (or '%s' does not exist)" % (CONF_JSON)
                sys.exit(0)
            force_refresh = False
            if opt in ("-r", "--refresh"):
                force_refresh = True
            print "Select a feed to preprocess into the cache:"
            n = 1
            for feed in feed_list:
                print "%d: %s (%s)" % (n, feed['name'], feed['type'])
                n += 1
            choice = int(input()) - 1
            if choice < 0 or choice >= len(feed_list):
                print "choice out of range %d" % (choice + 1)
                sys.exit(1)
            feed = feed_list[choice]
            feed_url = "/" + feed['type'] + "/" + feed['uid']
            print "caching '%s': '%s'" % (feed['name'], feed_url)
            (status_code, rss_xml) = get_yt_rss_feed(feed_url)
            process_rss.transform_rss_xml(rss_xml.encode('utf8'), verbose=True, refresh=force_refresh)
            sys.exit(0)

    # kick off the server
    run(port)
