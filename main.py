import tweepy
import time


consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

print("Connected to Twitter")


fichier_reponse = open("reply.txt", "r")
phrase_reponse = fichier_reponse.read()
fichier_reponse.close()


fichier_USA = open("Cities.txt", "r")
liste_USA = fichier_USA.read().split("\n")
fichier_USA.close()



nom_fichier = "liste_id.txt"
liste_id = []


fichier_keyword = open("keywords.txt", "r")
keyword = fichier_keyword.read()
fichier_keyword.close()

keyword = keyword.split("\n")[0]

def import_tweets_id():
    try:
        fichier_tweets_id1 = open(nom_fichier, "r")
        liste_tweets_id = fichier_tweets_id1.read().split()
        fichier_tweets_id1.close()
        return liste_tweets_id
    except FileNotFoundError:
        sauvegarde_tweets_id()
        import_tweets_id()


def sauvegarde_tweets_id():
    fichier_tweets_id2 = open(nom_fichier, "w")
    fichier_tweets_id2.write("\n".join(liste_id))
    fichier_tweets_id2.close()


def recup_tweets():
    raw_tweets = tweepy.Cursor(api.search, q=keyword, lang="en", result_type="recent").items(300)
    try:
        for tweet in raw_tweets:
            if tweet.text.lower().find(keyword.lower()) > -1:
                if len(set(liste_USA).intersection(tweet.user.location.split(", "))) > 0:
                    if str(tweet.id) in liste_id:
                        pass
                    else:
                        if tweet.in_reply_to_status_id_str == None:
                            try:
                                tweet.retweeted_status.created_at
                            except AttributeError:
                                api.update_status(status = phrase_reponse, in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)
                                local = time.localtime()
                                print("Tweet replied {}/{}/{} at {}:{} :".format(local.tm_mday, local.tm_mon, local.tm_year, local.tm_hour, local.tm_min))
                                print(tweet.text)
                                liste_id.append(str(tweet.id))
                                sauvegarde_tweets_id()
                                return(True)
    except tweepy.error.TweepError:
        api = tweepy.API(auth)
        time.sleep(30)
        recup_tweets
    return(False)


liste_id = import_tweets_id()

while 1:
    try:
        if recup_tweets():
            time.sleep(60*10)
        else:
            time.sleep(60*5)
    except tweepy.error.RateLimitError:
        time.sleep(5*60)







#
