# SageToEmby
Python Script to Symlink SageTV Files to Emby Format

This is a very kludgy script to create symlinks for SageTV shows into Emby/Kodi format. It is not effecient, but it works. It does keep track of found files and does not search them again. It uses IMDB and TVMAZE to search for movies and a fuzzy search on episodes names, because sometimes SageTV does not scrape the Season/Episode. It still makes a few mistakes, but good enough

It uses SageX api to get the show name, because parsing filenames is not very good.
Edit the directories to your liking. You need to create the top level directories yourself. Also edit your Sage IP address

I like using symlinks because I still use Sage 99% of the time. I only use Emby/Kodi when on the road.

You also have to:
pip install python-tvmaze
pip install IMDbPY
pip install fuzzywuzzy
pip install fuzzywuzzy[speedup] # Optional, would not compile on my windows machine
