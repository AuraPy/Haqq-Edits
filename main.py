import pixabay.core
import requests
import random
import yt_dlp
import os

def choose_video(px, ayah):
    resultandquery = send_query(px, ayah)
    result = resultandquery[0]
    query = resultandquery[1]
    if len(result) > 0:
        print(f"Found {len(result)} results")
        for index in result:
            index.download(f"{query}.mp4", "medium")
            os.system(f"mpv '{query}.mp4'")
            if input("Is this video ok? [y/n]").lower() == "y":
                break
            else:
                os.system(f"rm '{query}.mp4'")
                if input("\n\nWould you like to try another query? [y/n]") == "y":
                    return choose_video(px, ayah)
        return f"{query}.mp4"

    else:
        print("Couldn't find any results for that query.")
        return choose_video(px, ayah)


def send_query(px, ayah):
    query = input(f"\n\nWhat query should I send for this ayah:\n\n{ayah}\n\n")
    result = pixabay_searcher(px, query)

    return result, query

def ayah_retriever():
    surah = random.randint(70, 114)
    ayahs = []

    for i in range(1, requests.get(f"http://api.alquran.cloud/v1/surah/{surah}/en.asad").json()["data"]["numberOfAyahs"]):
        ayahs.append(requests.get(f"http://api.alquran.cloud/v1/ayah/{surah}:{i}/en.asad").json()["data"]["text"])

    return ayahs

def pixabay_searcher(pixabay, query: str):
    search_videos = pixabay.queryVideo(query)
    
    return search_videos

def main():
    px = pixabay.core("45287472-297041ba3024ea4a8882277b8")
    retrieved_ayahs = ayah_retriever()
    ayahs_ok = input(f"The randomly selected ayahs are:\n\n{retrieved_ayahs}\n\nIs this ok? [y/n]").lower()
    files = []

    if ayahs_ok == "n":
        main()
    elif ayahs_ok != "y":
        print("I'm gonna take that as a no :D")
        main()
    else:
        for ayah in retrieved_ayahs:
            video = choose_video(px, ayah)
            files.append(video)

    for file in files:
        os.system(f"rm '{file}'")


"""
format = {
    "outtmpl": "/home/zayan/Documents/Python_Projects/Haqq-Edits/%(id)s.mp4",
    "quiet": True,
    "no_warnings": True
}

yt = yt_dlp.YoutubeDL(format)
yt.download(url_list=urls)
"""

main()
