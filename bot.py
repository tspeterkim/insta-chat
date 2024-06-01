import requests
import gspread
import time


def get_long_token(short_token):
    app_id = '400706684811642'
    with open('FB_APP_SECRET', 'r') as file:
        app_secret = file.read().strip()
    url = 'https://graph.facebook.com/v12.0/oauth/access_token'
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_token
    }
    response = requests.get(url, params=params)
    return response.json()['access_token']


# Open fancy web app...google sheets
gc = gspread.service_account(filename='insta-chat-424606-14fbde4a9313.json')
sh = gc.open('insta-chat')

short_token = sh.sheet1.get('Z1').first()
page_id = sh.sheet1.get('Z2').first()
page_access_token = get_long_token(short_token)


def comments(post_id):
    url = f'https://graph.facebook.com/{post_id}/comments?fields=text,id&access_token={page_access_token}'
    response = requests.get(url)
    if response.status_code == 400: # ignore incorrect post ids
        return []
    return response.json()['data']


sent_cmt_ids = set()
while True:
    rows = sh.sheet1.get('A:C')[1:]
    for r in rows:
        if len(r) != 3: # can happen when my wife has not finished writing the row
            continue
        post_id, keywords, reply = r
        keywords = set(keywords.split(','))
        for cmt in comments(post_id):
            comment, comment_id = cmt['text'], cmt['id']
            if comment_id not in sent_cmt_ids and any(word in comment for word in keywords):
                params = {
                    'recipient': {'comment_id': comment_id},
                    'message': {'text': reply},
                    'access_token': page_access_token
                }
                url = f'https://graph.facebook.com/{page_id}/messages'
                response = requests.post(url, json=params).json()
                # set aside comments that we don't need to reply to again (avoids rate limiting from FB)
                if 'error' in response and response['error']['code'] == -1:
                    sent_cmt_ids.add(comment_id)
                print(response) # for sanity
    time.sleep(60) # don't need real-time replies
