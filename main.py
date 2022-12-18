import pandas
from glob import glob
import json
import typer
import os
from typing import Optional
from rich import print

INVIDIOUS_JSON = "subscription_manager.json"
OUT_DIR = "out"
MAX_PLAYLIST_LENGTH = 490


def appendPlaylist(json, playlistNum: int, videos: list):
    for video in videos:
        if video not in json["playlists"][playlistNum]["videos"]:
            json["playlists"][playlistNum]["videos"].append(video)

    return json


def appendSubs(data, subs):
    print("[deep_pink4]Appending subscriptions[/deep_pink4]")
    for sub in subs:
        if sub not in data["subscriptions"]:
            data["subscriptions"].append(sub)

    return data

def addPlaylist(json, name: str, videos: list, privacy: str):
    json["playlists"].append({
        "title": name,
        "description": "",
        "privacy": privacy,
        "videos": videos
    })

    return json


def playlistNumber(json, name: str):
    for index, playlist in enumerate(json["playlists"]):
        if playlist["title"].strip().lower() == name.strip().lower():
            playlist["title"] = name.strip()
            return index
    return -1


def makeOutDirectory():
    # make sure the output directory exists
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)


def shouldAppend(name: str):
    while True:
        res = typer.prompt(
            f"Should this playlist `{name}` be appended to? (y/n)")
        if res != "y" and res != "n":
            print("[red] Invalid response. Enter y or n")
        if res == "y":
            return True
        if res == "n":
            return False


def divideVideos(videos: list):
    # this is reversed so that we have the oldest playlists take up the max length.
    # thus the newest playlist won't be full length and thus can be appended to
    videos = list(reversed(videos))

    res = [videos[i:i + MAX_PLAYLIST_LENGTH]
           for i in range(0, len(videos), MAX_PLAYLIST_LENGTH)]

    # reverse it back so all playlists have their videos still in chronological order
    return [list(reversed(r)) for r in res]


def splitLongPlaylists(json, privacy: str):
    for index, playlist in enumerate(json["playlists"]):
        if len(playlist["videos"]) > MAX_PLAYLIST_LENGTH:
            print(
                f"\n[orange1]Splitting playlist [/orange1] {playlist['title']} since it is above the maximum length of {MAX_PLAYLIST_LENGTH}")

            videos = divideVideos(playlist["videos"])

            for index, smaller_playlist in enumerate(videos):
                name = f"{playlist['title']}_{index}"
                json["playlists"].append({
                    "title": name,
                    "description": "",
                    "privacy": privacy,
                    "videos": smaller_playlist
                })
            # remove the original playlist that was over the limit
            json["playlists"].pop(index)

    return json


def getCSVs(csv_dir: str)-> list:
    os.chdir(csv_dir)
    files = glob("*.csv")

    if len(files) == 0 or files == None:
        # expand path to absolute path
        csv_dir = os.path.abspath(csv_dir)

        print(f"[red]No CSV files found in the directory {csv_dir}")
        exit(1)
    return files        


def main(csv_dir: str, include_subs: bool, append_all: bool, out_dir: str, invidious: str, split: bool, privacy: str):

    makeOutDirectory()

    files = getCSVs(csv_dir)

    try:
        read_file = open(invidious, "r")
    except FileNotFoundError:
        print(f"[red]Invidious json data titled `{invidious}` was not found")
        exit(1)

    data = json.load(read_file)
    for f in files:

        if f == "subscriptions.csv" and include_subs:
            df = pandas.read_csv(f)["Channel Id"]
            subs = df.values.tolist()
            data = appendSubs(data, subs)
            continue

        try:
            df = pandas.read_csv(f, skiprows=2)["Video Id"]
        except:
            print(
                f"[red]Error reading in csv playlist titled `{f}`. Skipping it")

        name = (f).split(".")[:-1]
        name = " ".join(name)
        videos: list = df.values.tolist()
        playlistNum = playlistNumber(data, name)
        if playlistNum != -1:
            proceed = True if append_all else shouldAppend(name)
            if proceed:
                print(f"[light_slate_blue]Appending playlist [/light_slate_blue]{name}")
                data = appendPlaylist(data, playlistNum, videos, privacy)
            continue
        print(f"Adding playlist {name}")
        data = addPlaylist(data, name, videos, privacy)

    data = splitLongPlaylists(data, privacy) if split else data

    output = os.path.join(out_dir, "new_appended_data.json")

    print(f"[green]Writing new invidious data to {output}")

    json.dump(data, open(f"{output}", "w"), indent=4)
    read_file.close()


def cli_runner(
    subs: Optional[bool] = typer.Option(
        False, help="Append subscriptions from subscriptions.csv"),
    csv_dir: str = typer.Option(
        ".", help="Directory where CSV files are read in from"),
    append_all: Optional[bool] = typer.Option(
        False, help="Don't ask before appending. Add to existing playlist if the same name is in both the Invidious json and Youtube csv"),
    out_dir: Optional[str] = typer.Option(
        OUT_DIR, help="Directory where json output is written to"),
    invidious: Optional[str] = typer.Option(
        INVIDIOUS_JSON, help="Relative path to Invidious data file"),
    split: Optional[bool] = typer.Option(
        True, help=f"Split playlists with len>{MAX_PLAYLIST_LENGTH} to accomodate for Invidious playlist size limit"),
    privacy: Optional[str] = typer.Option(
        "Private", help="Privacy setting for playlists. Either Private or Public")
):
    if privacy != "Private" and privacy != "Public":
        print("[red]Invalid privacy setting. Must be either Private or Public")
        exit(1)
    # sanitize csv dir
    csv_dir = os.path.abspath(csv_dir)

    main(csv_dir, subs, append_all, out_dir, invidious, split, privacy)


if __name__ == "__main__":
    typer.run(cli_runner)

