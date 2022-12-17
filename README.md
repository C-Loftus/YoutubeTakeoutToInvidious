## How To Use

- Get your data from Youtube using Google Takeout
- Your playlists should be located in `YourTakeoutFolder/YouTube and YouTube Music/playlists`
-

## Install

You must have python installed.

### System Wide Install

```
pip install -r requirements.txt
```

To run

```
python main.py
```

### pipenv install (for isolating installs)

```
pipenv install .
```

To run

```
pipenv run python main.py
```

## Limitations

-

## Help

```

host@computer ~/P/json (main)> python ./appendJSON.py --help
Usage: appendJSON.py [OPTIONS]

Options:
--include-subs / --no-include-subs
Append Subscriptions [default: no-include-
subs]
--csv-dir TEXT Directory where CSV files are read in from
[default: .]
--append-all / --no-append-all Append all playlists [default: no-append-
all]
--out-dir TEXT Directory where output is written to
[default: out]
--invidious TEXT Relative path to Invidious data file
[default: subscription_manager.json]
--help Show this message and exit.

```

```

```
