# TILredditReader
Read titles off of /r/todayilearned with text to speech.

This is a script I wrote a year or two back, so I do not remember exactly how it works. What it does however is
to retrieve thread titles from www.reddit.com/r/todayilearned using the API and read them using built in text to speech.
The script will then continue to look for new threads in intervals and read them too. Send the audio to
something like a Skype group chat for increased fun.

Disclaimer: The python text to speech wrapper used can be found at https://github.com/parente/pyttsx

Get the additional drivers to have it work outside of a win32 environment.
