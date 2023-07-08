from http.cookies import SimpleCookie
import json

def parse_raw_cookie(cookie_file):
    '''
    How to get cookie_file?
    - Use Cookie-Editor extension on Chrome to get the raw cookie and save it to a text file, for example: cookie.txt
    - Extension link: https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm

    :param cookie_file: cookie.txt
    :return: cookies as dict
    '''
    with open(cookie_file, 'r') as f:
        raw_cookie = f.read()
    try:
        cookie = json.loads(raw_cookie)
        cookies = {item['name']:item['value'] for item in cookie}
    except:
        cookie = SimpleCookie()
        cookie.load(raw_cookie)
        cookies = {key:value.value for key,value in cookie.items()}
    return cookies

if __name__ == '__main__':
    cookies = parse_raw_cookie(cookie_file='cookie.txt')
    print(cookies)