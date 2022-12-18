# How To Use

- Get your data from Youtube using Google Takeout
- Your playlists will be located in `Takeout/YouTube and YouTube Music/playlists`
- Copy all these csv files for the playlist into the same folder as this script (or specify the folder with `--csv-dir`)
- Get a base Invidious data json file
  - Make sure you have an account for Invidious on an instance.
  - From your Invidious instance export your data by going into `Settings Gear Icon->Data Preferences->Import/Export Data->Export Invidious Data as json`
- Install the requirements (see below)
- Run the script with `python main.py`
- If you found this to be useful please [star this repo](https://github.com/C-Loftus/YoutubeTakeoutToInvidious)

# Install

You must have python installed.

## System Wide Install

```
pip install -r requirements.txt
```

To then run with `python main.py`

## pipenv install (for isolating package installs from your system Python env)

```
pipenv install
```

Then run with `pipenv run python main.py`

## Limitations

- Invidious limits playlist sizes. This script will split playlists with more than 490 videos into multiple playlists.
- Invidious does not overwrite playlists when you import data. You may need to delete playlists in your Invidious instance after importing data.
- YouTube could change the format of their csv files.

## Help and Settings

```
 Usage: main.py [OPTIONS]

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --subs          --no-subs                Append subscriptions from subscriptions.csv [default: no-subs]                            │
│ --csv-dir                          TEXT  Directory where CSV files are read in from [default: .]                                   │
│ --append-all    --no-append-all          Don't ask before appending. Add to existing playlist if the same name is in both the      │
│                                          Invidious json and Youtube csv                                                            │
│                                          [default: no-append-all]                                                                  │
│ --out-dir                          TEXT  Directory where json output is written to [default: out]                                  │
│ --invidious                        TEXT  Relative path to Invidious data file [default: subscription_manager.json]                 │
│ --split         --no-split               Split playlists with len>490 to accomodate for Invidious playlist size limit              │
│                                          [default: split]                                                                          │
│ --privacy                          TEXT  Privacy setting for playlists. Either Private or Public [default: Private]                │
│ --help                                   Show this message and exit.                                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
