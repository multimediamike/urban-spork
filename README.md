# urban-spork

## About

urban-spork solves one very simple problem: It allows a podcast client to download the audio portion of a YouTube video so that it can be treated as a proper podcast file

While most podcasts provide an RSS feed pointing to the audio files to be downloaded, some podcasts (and some videos that are basically just talking heads yammering for a long time and can be treated as podcasts) insist on making their content available as YouTube videos. This program is essentially a proxy between a podcast client and a YouTube channel or playlist.

The name 'urban-spork' was randomly generated by GitHub while creating this repository.

## Requirements

The main proxy program uses Python and its standard libraries, as well as the [Python requests library](http://docs.python-requests.org/en/master/). It relies on [youtube-dl](https://rg3.github.io/youtube-dl/) to query metadata from YouTube. (It does not download audio files from YouTube; it merely derives the download URLs to pass along to the podcast client, which in turn downloads the audio files.)

## Configuring and Running

The base directory contains a file called `urban-spork.conf.json.example`. Copy this file to `urban-spork.conf.json` so that it will be read by the proxy. This file contains configurations for the YouTube feeds that you wish to convert into podcast feeds.

This is an example configuration block, based on a channel called [Nerd to the Third](https://www.youtube.com/channel/UCcdIVzL01YHcxUBYFWDWKMg) which publishes podcasts in video form (they do have a proper podcast feed but it's not often kept up to date).

The channel URL is https://www.youtube.com/channel/UCcdIVzL01YHcxUBYFWDWKMg, thus, the `uid` key is "UCcdIVzL01YHcxUBYFWDWKMg":

```javascript
[
    {
        "type": "videos",
        "name": "Nerd To The Third",
        "uid": "UCcdIVzL01YHcxUBYFWDWKMg"
    }
]
```

The `type` key is either "videos" or "playlist". The `uid` key is the long string that identifies the video or playlist URL.

urban-spork maintains a cache of the absolute download URLs. It is useful to pre-cache these URLs with the following command:

`./urban-spork.py --cache`

This command will ask you to select a feed to pre-cache.

In order to subscribe to a feed via your podcast client, run the proxy in server mode:

`./urban-spork.py`

This will run the proxy on port 54321 on all public interfaces. To select an alternate port, use `-p` or `--port`. With the proxy running, you will be able to point a web browser directly at the root, e.g., `lan-ip-address:54321` and you will receive a list of proxy subscription links. This allows you to conveniently copy and paste the feeds into your podcast client.

Note that the direct audio download URLs that are cached by urban-spork will expire in short order after they are retrieved (they have expiration timestamps built in). Thus, it is useful to download proxied episodes shortly after updating a feed via the reader. If a feed's links are stale, you can run:

`./urban-spork.py --refresh`

As with the `--cache` option, this will prompt you to select a feed. It will then force a refresh of all the cached download links corresponding to the selected feed.

## Supported Podcast Clients

YouTube's audio download links are in .MP4 format. Thus, a podcast client needs to be able to cope with that format (rather than .MP3 files).

So far, this system has been found to work great with the [BeyondPod podcast client for Android](http://www.beyondpod.mobi/android/index.htm).

## Similar Projects

See also: [yt2pod](https://github.com/frou/yt2pod), a similar project written in the Go language.

## Author

"Multimedia" Mike Melanson (mike -at- multimedia.cx), multimedia hacker and podcast addict.

Blog @ [Breaking Eggs and Making Omelettes](https://multimedia.cx/eggs/).

