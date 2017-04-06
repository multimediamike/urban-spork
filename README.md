# YouTube2Podcast

## Author

"Multimedia" Mike Melanson (mike -at- multimedia.cx), multimedia hacker and podcast addict.

Blog @ [Breaking Eggs and Making Omelettes](https://multimedia.cx/eggs/).

## About

YouTube2Podcast (`yt2pod`) solves one very simple problem: It allows a podcast client to download the audio portion of a YouTube video so that it can be treated as a proper podcast.

While most podcasts provide an RSS feed pointing to the audio files to be downloaded, some podcasts (and some videos that are basically just talking heads yammering for a long time and can be treated as podcasts) insist on making their content available as YouTube videos. This program is essentially a proxy between a podcast client and a YouTube channel or playlist.

## Requirements

The main proxy program use pure Python and its standard libraries. It relies on [youtube-dl](https://rg3.github.io/youtube-dl/) to query metadata from YouTube.

## Configuring and Running

The base directory contains a file called `yt2pod.conf.json.example`. Copy this file to `yt2pod.conf.json` so that it will be read by the proxy. This file contains configurations for the YouTube feeds that you wish to convert into podcast feeds.

This is an example configuration block, based on a channel called [Nerd to the Third](https://www.youtube.com/channel/UCcdIVzL01YHcxUBYFWDWKMg) which publishes podcasts in video form (they do have a proper podcast feed but it's not often kept up to date).

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

`yt2pod` maintains a cache of the absolute download URLs. It is useful to pre-cache these URLs with the following command:

`./yt2pod-proxy --cache`

This command will ask you to select a feed to pre-cache.

In order to subscribe to a feed via your podcast client, run the proxy in server mode:

`./yt2pod-proxy`

This will run the proxy on port 54321 on all public interfaces. To select an alternate port, use `-p` or `--port`. With the proxy running, you will be able to point a web browser directly at the root, e.g., `lan-ip-address:54321` and you will receive a list of subscription links. This allows you to conveniently copy and paste the feeds into your podcast client.

Note that the direct audio download URLs that are cached by `yt2pod` will expire in short order after they are retrieved (they have expiration timestamps built in). Thus, it is useful to download proxied episodes shortly after updating a feed via the reader. If a feed's links are stale, you can run:

`./yt2pod-proxy --refresh`

As with the `--cache` option, this will prompt you to select a feed. It will then refresh all of the cached download links corresponding to this feed.

## Supported Podcast Clients

YouTube's audio download links are in .MP4 format. Thus, a podcast client needs to be able to cope with that format (rather than .MP3 files).

So far, this system has been found to work great with the [BeyondPod podcast client for Android](http://www.beyondpod.mobi/android/index.htm).
