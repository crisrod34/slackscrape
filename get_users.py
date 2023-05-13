import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from json_utils import load_json, dump_json

config = load_json('./env.json')

client = WebClient(token=config['token'])
logger = logging.getLogger("logger")

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory

members_path = ensure_dir('./output/users/members')

users_store = {}
# Put users into the dict
def save_users(users_array):
    for user in users_array:
        # Key user info on their unique user ID
        user_id = user["id"]
        # Store the entire user object (you may not need all of the info)
        users_store[user_id] = user
    print(users_store)
    dump_json('{}/members.json'.format(members_path), users_store)

try:
    response = client.users_list()
    save_users(response["members"])
except SlackApiError as e:
    logger.error("Error creating conversation: {}".format(e))


