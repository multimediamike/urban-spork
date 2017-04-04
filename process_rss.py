#!/usr/bin/python

import commands
import dbm
import json
import requests
import StringIO
import sys
import xml.etree.ElementTree as ET

YOUTUBE_DL = "/usr/local/bin/youtube-dl"

def transform_rss_xml(input_xml, verbose=False, refresh=False):
    cache = dbm.open("yt2pod.cache", "c")

    xml_string_file = StringIO.StringIO(input_xml)
    in_tree = ET.parse(xml_string_file)
    in_root = in_tree.getroot()

    # establish output RSS framework
    root_rss = ET.Element('rss', attrib={'version': '2.0'})
    out_tree = ET.ElementTree(root_rss)
    channel = ET.Element('channel')
    root_rss.append(channel)

    # transfer the top-level metadata
    in_title = in_root.find('{http://www.w3.org/2005/Atom}title')
    out_title = ET.Element('title')
    out_title.text = in_title.text
    channel.append(out_title)
    description = ET.Element('description')
    description.text = "YouTube audio-only feed for '%s'" % (out_title.text)
    channel.append(description)
    published = in_root.find('{http://www.w3.org/2005/Atom}published')
    lastBuildDate = ET.Element('published')
    lastBuildDate.text = published.text
    channel.append(lastBuildDate)

    # iterate through the items and transfer each
    for child in in_root:
        if child.tag.endswith('entry'):
            item = ET.Element('item')
            media_group = child.find('{http://search.yahoo.com/mrss/}group')
            # transfer metadata - title
            in_title = child.find('{http://www.w3.org/2005/Atom}title')
            out_title = ET.Element('title')
            out_title.text = in_title.text
            item.append(out_title)
            # description
            in_desc = media_group.find('{http://search.yahoo.com/mrss/}description')
            out_desc = ET.Element('description')
            out_desc.text = in_desc.text
            item.append(out_desc)
            # published -> pubDate
            in_date = child.find('{http://www.w3.org/2005/Atom}published')
            out_date = ET.Element('pubDate')
            out_date.text = in_date.text
            item.append(out_date)
            # thumbnail
#            in_thumb = media_group.find('{http://search.yahoo.com/mrss/}thumbnail')
#            out_thumb = ET.Element('thumbnail')
#            out_thumb.attrib = in_thumb.attrib
#            item.append(out_thumb)

            # pick out the main YouTube URL
            link_elem = child.find('{http://www.w3.org/2005/Atom}link')
            yt_link = link_elem.get("href")
            if verbose:
                print "Fetching " + yt_link + "...",
            if not refresh and yt_link in cache:
                if verbose:
                    print "cached"
                cached = json.loads(cache[yt_link])
                dl_link = cached['dl_link']
                dl_size = cached['dl_size']
            else:
                # invoke youtube-dl to fetch the download link
                cmd = YOUTUBE_DL + " --get-url --format 140 " + yt_link
                if verbose:
                    print "caching..."
                (status, dl_link) = commands.getstatusoutput(cmd)

                # invoke requests module with a HEAD request to get size
                head_req = requests.head(dl_link)
                dl_size = head_req.headers['Content-Length']

                # cache the downloaded information
                cached = { 'dl_link': dl_link,
                    'dl_size': dl_size
                }
                cache[yt_link] = json.dumps(cached)

            # create a new element and insert into the item
            attrib = { 'url': dl_link,
                'type': 'audio/mpeg',
                'length': dl_size
            }
            enclosure = ET.Element("enclosure", attrib)
            item.append(enclosure)
            channel.append(item)

    output_xml = StringIO.StringIO()
    out_tree.write(output_xml, encoding="utf8", xml_declaration=True)
    return output_xml.getvalue()

