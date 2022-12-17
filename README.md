# How To Use

- Get your data from Youtube using Google Takeout
- Your playlists will be located in `YourTakeoutFolder/YouTube and YouTube Music/playlists`
- Copy all these csv files for the playlist into the same folder as this script (or specify the folder with `--csv-dir`)
- Get a base Invidious data json file
  - Make sure you have an account for Invidious on an instance.
  - From your Invidious instance export your data by going into `Settings Gear Icon->Data Preferences->Import/Export Data->Export Invidious Data as json`
- Install the requirements (see below)
- Run the script with `python main.py`

# Install

You must have python installed.

## System Wide Install

```
pip install -r requirements.txt
```

To run

```
python main.py
```

## pipenv install (for isolating package installs from your system Python env)

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
