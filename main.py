import pixabay.core
import requests
from pygame import mixer
import time
import random
import yt_dlp
import os

def choose_sound():
    sound = input("Please specify the path of the recitation you have chosen:\n\n")
    mixer.music.load(sound)

    return sound

def choose_video(px, ayah):
    resultandquery = send_query(px, ayah)
    result = resultandquery[0]
    query = resultandquery[1]
    if len(result) > 0:
        print(f"\n\nFound {len(result)} results\n\n")
        for index in result:
            index.download(f"{query}.mp4", "medium")
            os.system(f"mpv '{query}.mp4'")
            if input("Is this video ok? [y/n]").lower() == "y":
                break
            else:
                os.system(f"rm '{query}.mp4'")
                if input("Would you like to try another query? [y/n]") == "y":
                    return choose_video(px, ayah)
        return f"{query}.mp4"

    else:
        print("Couldn't find any results for that query.")
        return choose_video(px, ayah)


def send_query(px, ayah):
    query = input(f"What query should I send for this ayah:\n\n{ayah}\n\n")
    result = pixabay_searcher(px, query)

    return result, query

def ayah_retriever():
    surahandayahs = input("Enter the range of ayahs this recitation has in the format '[surah]:[ayah]-[ayah]'\n\n")
    surah, ayahrange = surahandayahs.split(":")
    ayah1, ayah2 = ayahrange.split("-")
    index = 0
    ayahs = []

    for i in range(int(ayah1), int(ayah2)):
        ayahs.append(requests.get(f"http://api.alquran.cloud/v1/ayah/{surah}:{i}/en.asad").json()["data"]["text"])

    return ayahs

def pixabay_searcher(pixabay, query: str):
    search_videos = pixabay.queryVideo(query)
    
    return search_videos

def main():
    player = mixer.init()
    px = pixabay.core("45287472-297041ba3024ea4a8882277b8")
    retrieved_ayahs = ayah_retriever()
    ayahs_ok = input(f"The selected ayahs are:\n\n{retrieved_ayahs}\n\nIs this ok? [y/n]").lower()
    files = []
    start_of_ayahs = []

    if ayahs_ok == "n":
        main()
    elif ayahs_ok != "y":
        print("I'm gonna take that as a no :D")
        main()
    else:
        sound = choose_sound()
        epoch = time.time()
        for ayah in retrieved_ayahs:
            if len(start_of_ayahs) > 0:
                mixer.music.play(start=start_of_ayahs[len(start_of_ayahs)-1])
            else:
                mixer.music.play()
            input(f"Press enter when the start of the following ayah is recited: {ayah}")
            start_of_ayahs.append(time.time()-epoch)
            print(start_of_ayahs)
            mixer.music.stop()
        for ayah in retrieved_ayahs:
            video = choose_video(px, ayah)
            files.append(video)

    for file in files:
        os.system(f"rm '{file}'")
    print(start_of_ayahs)

    mixer.music.unload(sound)


main()
