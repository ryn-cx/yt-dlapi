from gapi import remove_redundant_files

from yt_dlapi.constants import FILES_PATH, YT_DLAPI_PATH

if __name__ == "__main__":
    for model in YT_DLAPI_PATH.iterdir():
        if not model.is_dir() or model.name.startswith("_"):
            continue
        input_folder = FILES_PATH / model.name
        json_files = list(input_folder.glob("*.json"))
        remove_redundant_files(json_files)
