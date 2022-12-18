# YoutubeTakeoutToInvidious

Easily import your Youtube playlists and subscriptions into Invidious. Takes CSV files from Youtube Takeout and converts them to Invidious JSON data.

# How To Use

- Get your data from Youtube using Google Takeout
- Your playlists will be located in `Takeout/YouTube and YouTube Music/playlists`
- Copy all these csv files for the playlist into the same folder as this script (or specify the folder with `--csv-dir`)
- Get a base Invidious data json file
  - Make sure you have an account for Invidious on an instance.
  - From your Invidious instance, export your existing data (fine if you don't have any)
    - Found at `Settings Gear Icon->Data Preferences->Import/Export Data->Export Invidious Data as json`
- Install the requirements (see below)
- Run the script with `python main.py`
  - use `--help` to see how to change settings
- Get the output json file from the `out` directory and import it into Invidious
  - Done at `Settings Gear Icon->Data Preferences->Import/Export Data->Import Invidious JSON data`
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
- Invidious does not overwrite playlists when you import data. If you have existing playlists, you may need to delete duplicate playlists in your Invidious account after importing data.
  - However, if you have the same playlist name in both the Invidious json and the Youtube csv, the script will ask you if you want to append the videos in the Youtube csv playlist to the existing Invidious playlist, without adding another new playlist.

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
