from playsound import playsound


def playSound(url: str):
    try:
        playsound(url)
    except:
        print("Error playing sound")
