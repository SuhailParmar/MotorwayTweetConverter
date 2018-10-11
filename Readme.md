# Motorway Tweet Converter

This is the 2nd component of the 'Motorway event system'. This component binds to a specific rabbit queue and waits for a condensed tweet. See MotorwayTwitterScraper lib/tweet.py. Once the tweet is recieved this app needs to text mine the contents of this tweet in order to get broken down information. E.g:

```json

{   "screen_name": "Traffic_M6",
    "created_at": "Wed Oct 10 19:13:35 +0000 2018",
    "id": 1050102057091379200,
    "payload": "#M6 J2 southbound exit (Coventry) - Broken down vehicle - Full details at https://t.co/nkWL91Ro1g (Updated every 5 minutes)"
}

```

Will be broken down by the day, time, year, the motorway, the junction, the id, the nearest city, the reason etc.
