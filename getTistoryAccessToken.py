import requests
import json
import re

g_client_id = {App ID}
g_redirect_uri = {CallBack}
g_oauth_url = "https://www.tistory.com/oauth/authorize?client_id="+g_client_id+"&redirect_uri="+g_redirect_uri+"&response_type=token"
g_user_id = {TISTORY ID}
g_password = {TISTORY PASSWORD}

print(g_oauth_url)
res = requests.get(g_oauth_url)
print(res.status_code)
print(res.headers['Set-Cookie'])
kakao_cookie = res.headers['Set-Cookie'].replace("; path=/",'')
print(kakao_cookie)
print(res.url)
headers = {
    'Accept' : 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language' : 'ko, en-US; q=0.8, en; q=0.6, zh-Hans-CN; q=0.4, zh-Hans; q=0.2',
    'Cache-Control' :  'no-cache',
    'Connection' : 'Keep-Alive',
    'Content-Type' : 'application/x-www-form-urlencoded',
    'Cookie' : kakao_cookie,
    'Host' : 'www.tistory.com',
    'Referer' : res.url,
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}
login_data = {
    'fp' : 'a668ac102f81b86f521c07dfb6dc992c',
    'keepLogin' : 'on',
    'loginId' : g_user_id,
    'password' : g_password,
    'redirectUrl' : res.url
    }
res = requests.post('https://www.tistory.com/auth/login', headers=headers, data=login_data)
print(res.url)
match = re.match('(.*?)access_token=(?P<access_token>.*?)&state=', res.url)
gd = match.groupdict()
access_token = gd['access_token']
print(access_token)
