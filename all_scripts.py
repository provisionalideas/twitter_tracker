import pandas as pd
import tweepy
import os
import datetime

# Import credentials
yaml_loc = os.path.expanduser('~') + # INSERT PATH TO YAML FILE HERE
access_yaml = open(yaml_loc + "access.yml","r+")
access_yaml = json.loads(access_yaml.read())

consumer_key = access_yaml['consumer_key']
consumer_secret = access_yaml['consumer_secret']
access_token = access_yaml['access_token']
access_secret = access_yaml['access_secret']

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)

# Pull current followers
names = []
screen_names = []
followers_count = []

for follower in followers_ids:
    try:
        user = api.get_user(follower)
    except:
        user = -1
        
    if user != -1:
        names.append(user.name)
        screen_names.append(user.screen_name)
        followers_count.append(user.followers_count)
    else:
        names.append("DNE")
        screen_names.append("DNE")
        followers_count.append("DNE")

follower_df = pd.DataFrame({'id':followers_ids,\
                            'username':names,\
                            'screen_name':screen_names,\
                            'num_followers':followers_count})
                            
# NOTE: If you have over 900 followers, it will mark the rest off as DNE. You'll need to 
# wait ~15 min and run it again with this second piece to fill in the gaps for each next set of
# 900. There's a way to automate the wait time, but I'm too lazy to add that in right now
# (even though it's just a sleep(15 minutes) for every ~900 followers).

for follower in follower_df.loc[follower_df['username'] == 'DNE'].iterrows():
    try:
        user = api.get_user(follower[1].id)
    except:
        user = -1
        
    if user != -1:
        follower_df.at[follower[0],'username'] = user.name
        follower_df.at[follower[0],'screen_name'] = user.screen_name
        follower_df.at[follower[0],'num_followers'] = user.followers_count
    else:
        follower_df.at[follower[0],'username'] = 'DNE'
        follower_df.at[follower[0],'screen_name'] = 'DNE'
        follower_df.at[follower[0],'num_followers'] = 'DNE'

# Here's how you export as a csv:
output_file = # INSERT DIRECTORY OF OUTPUT FILE HERE
follower_df.to_csv(output_file + "/followers-" + str(datetime.date.today()) + ".csv")

# Once you have a list of prior followers, here's how you compare against current followers:
my_account = #INSERT ACCOUNT_NAME HERE
followers_ids = api.followers_ids(my_account)
followers_old = pd.read_csv(### INSERT LINK TO YOUR LAST FOLLOWER TABLE HERE ###)

# See who unfollowed you since the last pull:
new_unfollowers = followers_old.loc[followers_old['id'].isin(\
                  set(followers_old['id']) - set(followers_ids))]
