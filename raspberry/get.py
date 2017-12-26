#import urllib.request
import requests

def user_reg(user_id):
    user_url = 'http://smartbin35.ru.mastertest.ru/api/checkuser?cardCode=' + user_id
    #response = urllib.request.urlopen(user_url)
    response = requests.get(user_url)
    user_status = response.text
    if user_status == b'true':
        return True
    else:
        return False


def reward(user_id, trash_type):
    reward_url = 'http://smartbin35.ru.mastertest.ru/api/bonus?cardCode=' + user_id
    reward_url = reward_url + '&trashType=' + trash_type + '&trashId=2'
    #urllib.request.urlopen(reward_url)
    response = requests.get(reward_url)

print(user_reg('5605B8DF7642'))
reward('5605B8DF7642', 'pet')
