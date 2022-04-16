import requests
import json
import instaloader
import time
from instaloader import Profile, Story, StoryItem



# PYTHON 3.9
# By LeTy



class TeleBot:

    def __init__(self, key, channelid, usernames, session, bot):
        self.key = key
        self.channelid = channelid
        self.usernames = usernames
        self.session = session
        self.bot = bot


    def startbot(self):

        data = {}
        for un in self.usernames:
            data[f"{un}"] = {"Lastpost": None, "Num": 0, "Laststory": None, "StoryNum": 0}
        timenow = time.strftime("%H:%M", time.gmtime())
        print(f"\n\n\n[!] LOG: Program started at {timenow}")

        while True:
            for username in self.usernames:
                profile = Profile.from_username(self.bot.context, f"{username}")

                for post in profile.get_posts():

                    if str(post.is_video) == "True":
                        posturl = post.video_url
                    else:
                        posturl = post.url

                    if data[f"{username}"]["Lastpost"] != str(post.url):
                        if data[f"{username}"]["Num"] == 0:
                            data[f"{username}"]["Lastpost"] = str(post.url)
                            data[f"{username}"]["Num"] += 1
                            break
                        postdata = {
                            'chat_id': self.channelid,
                            'document': str(posturl),
                        }
                        source = self.session.post(f"https://api.telegram.org/bot{self.key}/sendDocument", json=postdata)
                        timenow = time.strftime("%H:%M", time.gmtime())
                        data[f"{username}"]["Lastpost"] = str(post.url)
                        if source.status_code == 200:
                            print(f"[!] LOG: New post from {username} sent at {timenow}")
                        else:
                            print(f"[!] LOG: Failed to send post from {username} at {timenow}")
                    break


            for story in self.bot.get_stories():
                if story.owner_username in self.usernames:
                    for post in story.get_items():
                        if str(post.is_video) == "True":
                            posturl = post.video_url
                        else:
                            posturl = post.url

                        if data[f"{username}"]["Laststory"] != str(post.url):
                            if data[f"{username}"]["StoryNum"] == 0:
                                data[f"{username}"]["Laststory"] = str(post.url)
                                data[f"{username}"]["StoryNum"] += 1
                                break
                            postdata = {
                                'chat_id': self.channelid,
                                'document': str(posturl),
                            }
                            source = self.session.post(f"https://api.telegram.org/bot{self.key}/sendDocument",
                                                       json=postdata)
                            timenow = time.strftime("%H:%M", time.gmtime())
                            data[f"{username}"]["Laststory"] = str(post.url)
                            if source.status_code == 200:
                                print(f"[!] LOG: New story from {username} sent at {timenow}")
                            else:
                                print(f"[!] LOG: Failed to send story from {username} at {timenow}")
                        break






            time.sleep(60)







def startup():
    with open("Data/config.json", "r+", encoding="utf-8") as f:
        config = json.load(f)
        key = config["Key"]
        channelid = int(f'-100{config["ChannelID"]}')
        usernames = config["Accounts"]

    try:
        bot = instaloader.Instaloader()
        bot.login(config["Username"], config["Password"])
        rs = requests.Session()
        print(f"[!] Data/config.json")
        print(f"[!] Logged in as {config['Username']}")
        print(f"[!] Channel ID: {channelid}")
        print(f"[!] Usernames: {usernames}")
    except Exception as exc:
        print(
            f"\n\n[!] ERROR: Something went wrong. Make sure both the username & password are correct in Data/config.json")
        print(exc)
        quit()
        return exc

    TeleBot(key, channelid, usernames, rs, bot).startbot()


if __name__ == "__main__":
    startup()

