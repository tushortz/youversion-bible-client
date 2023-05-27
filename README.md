# Youversion Bible API

Unofficial Youversion bible api

## How to install

Run the following command in the terminal

```sh
$ pip install youversion-bible-client
```

## How to use

Import the client object

```py
from youversion.utils import Client
```

Create a new client object and instantiate it with a login credential.

```py
client = Client("<username_or_email>", "<password>")
```

call available methods on it

- moments()
- highlights()
- daily_verses()
- plan_progress()
- bookmarks()
- my_images()
- notes()
- plan_subscriptions()
- convert_note_to_md()


### Verse of the day

Getting the verse of the day

```py

# Get verse of the day for the current day
votd = client.verse_of_the_day()
print(votd)
>>> Votd(day=27, usfm=['PHP.4.19'], image_id=None)

# Prints the verse of the day object as a dictionary
print(votd.dict)
>>> {'day': 27, 'usfm': ['PHP.4.19'], 'image_id': None}

print(votd.day)
>>> 27
```


You can also get the verse of the day for a specific day

```py
votd = client.verse_of_the_day(355)

print(votd)
>>> Votd(day=355, usfm=['PSA.100.2'], image_id=None)
```


###

# TODO

* [x] login
* [ ] send friend request
* [ ] view friend requests
* [x] view moments
* [x] view notes
* [ ] create notes
* [ ] modify notes
* [ ] delete note
* [ ] write documentation
* [ ] write test

> Many more todo

