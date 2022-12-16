import pandas
import glob
import json
import typer
import os
from typing import Optional

INVIDIOUS_JSON = "subscription_manager.json"
OUT_DIR = "out"


def playlistExists(json, name: str):
    for index, playlist in enumerate(json["playlists"]):
        if playlist["title"].strip() == name.strip():
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
            print(f"Appending playlist `{name}`")
            return True
        if res == "n":
            print(f"Skipping playlist `{name}`")
            return False


def main(csv_dir: str, include_subs: bool, append_all: bool, out_dir: str, invidious: str):

    makeOutDirectory()

    os.chdir(csv_dir)
    files = glob.glob("*.csv")

    if len(files) == 0:
        print(f"No CSV files found in the directory {csv_dir}")
        return

    with open(invidious, "r") as read_file:
        data = json.load(read_file)

        for f in files:
            df = pandas.read_csv(f, skiprows=2)["Video Id"]
            name = (f).split(".")[:-1]
            name = " ".join(name)

            videos = set(df.values.tolist())

            playlistNum = playlistExists(data, name)
            if playlistNum != -1 and append_all == False:
                print(f"Playlist {name} already exists")
                proceed = shouldAppend(name)
                if proceed == False:
                    continue
                elif proceed == True:
                    for video in data["playlists"][playlistNum]["videos"]:
                        videos.add(video)
            print(f"Adding playlist {name}")
            data["playlists"].append({"title": name, "description": "",
                                      "privacy": "Private", "videos": list(videos)})

    print(f"Writing new invidious data to {out_dir}/new_appended_data.json")
    json.dump(data, open(f"{out_dir}/new_appended_data.json", "w"), indent=4)


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
):
    main(csv_dir, include_subs, append_all, out_dir, invidious)


if __name__ == "__main__":
    typer.run(cli_runner)
