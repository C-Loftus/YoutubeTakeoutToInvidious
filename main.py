import pandas
import glob
import json
import typer
import os
from typing import Optional

INVIDIOUS_JSON = "subscription_manager.json"
OUT_DIR = "out"
MAX_PLAYLIST_LENGTH = 499


def appendPlaylist(json, playlistNum: int, videos: list):
    for video in videos:
        if video not in json["playlists"][playlistNum]["videos"]:
            json["playlists"][playlistNum]["videos"].append(video)

    return json


def addPlaylist(json, name: str, videos: list):
    json["playlists"].append({
        "title": name,
        "description": "",
        "privacy": "Private",
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
        res = input(f"Should this playlist `{name}` be appended to? (y/n): ")
        if res != "y" and res != "n":
            print("Invalid response. Enter y or n")
        if res == "y":
            return True
        if res == "n":
            return False


def divideVideos(videos: list):
    return [videos[i:i + MAX_PLAYLIST_LENGTH] for i in range(0, len(videos), MAX_PLAYLIST_LENGTH)]


def splitLongPlaylists(json):
    for index, playlist in enumerate(json["playlists"]):
        if len(playlist["videos"]) > MAX_PLAYLIST_LENGTH:
            print(
                f"Splitting playlist {playlist['title']} since it is above the maximum length of {MAX_PLAYLIST_LENGTH}")

            videos = divideVideos(playlist["videos"])

            for index, smaller_playlist in enumerate(videos):
                name = f"{playlist['title']}_{index}"
                json["playlists"].append({
                    "title": name,
                    "description": "",
                    "privacy": "Private",
                    "videos": smaller_playlist
                })
            # remove the original playlist that was over the limit
            json["playlists"].pop(index)

    return json


def main(csv_dir: str, include_subs: bool, append_all: bool, out_dir: str, invidious: str, split: bool):

    makeOutDirectory()

    os.chdir(csv_dir)
    files = glob.glob("*.csv")

    if len(files) == 0:
        print(f"No CSV files found in the directory {csv_dir}")
        return

    try:
        read_file = open(invidious, "r")
    except FileNotFoundError:
        print(f"File not found: {invidious}")
        read_file.close()
        return

    data = json.load(read_file)
    for f in files:
        df = pandas.read_csv(f, skiprows=2)["Video Id"]
        name = (f).split(".")[:-1]
        name = " ".join(name)
        videos: list = df.values.tolist()
        playlistNum = playlistNumber(data, name)
        if playlistNum != -1:
            proceed = True if append_all else shouldAppend(name)
            if proceed:
                print(f"Appending playlist {name}")
                data = appendPlaylist(data, playlistNum, videos)
            continue
        print(f"Adding playlist {name}")
        data = addPlaylist(data, name, videos)

    data = splitLongPlaylists(data) if split else data

    print(f"Writing new invidious data to {out_dir}/new_appended_data.json")
    json.dump(data, open(f"{out_dir}/new_appended_data.json", "w"), indent=4)
    read_file.close()


def cli_runner(
    include_subs: Optional[bool] = typer.Option(
        False, help="Append Subscriptions"),
    csv_dir: str = typer.Option(
        ".", help="Directory where CSV files are read in from"),
    append_all: Optional[bool] = typer.Option(
        False, help="Append all playlists"),
    out_dir: Optional[str] = typer.Option(
        OUT_DIR, help="Directory where output is written to"),
    invidious: Optional[str] = typer.Option(
        INVIDIOUS_JSON, help="Relative path to Invidious data file"),
    split: Optional[bool] = typer.Option(
        False, help="Split playlists with len>499. Invidious has a limit of 500 videos per playlist")
):
    main(csv_dir, include_subs, append_all, out_dir, invidious, split)


if __name__ == "__main__":
    typer.run(cli_runner)
