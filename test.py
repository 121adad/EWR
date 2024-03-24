import requests

cookies = {
    'Hm_lvt_e57c2e187cc1668bba7f86d1784c0298': '1711118803',
    'openid': 'o7G9L5nqfvJ3EjLmPqSEVPTPrz58',
    'logintype': 'Njk0YzNkZDNiOWRjZDlhMDhlNDNiOGY2ZThlN2Y5OTU%3D',
    'login_time': '1711119100',
    'login_check': 'ZjhjMmRkOTIyMGRmOGNlOTUwMzM0ODgzMjE1MDMzYzY%3D',
    'userid': '1016222',
    'user_token': 'NDA3NzIyYTk3YTE1MDMwZTZhY2Y1NTg2MDUwNDNlYjE%3D',
    'Hm_lpvt_e57c2e187cc1668bba7f86d1784c0298': '1711120210',
}

headers = {
    'authority': 'img.sucai999.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'Hm_lvt_e57c2e187cc1668bba7f86d1784c0298=1711118803; openid=o7G9L5nqfvJ3EjLmPqSEVPTPrz58; logintype=Njk0YzNkZDNiOWRjZDlhMDhlNDNiOGY2ZThlN2Y5OTU%3D; login_time=1711119100; login_check=ZjhjMmRkOTIyMGRmOGNlOTUwMzM0ODgzMjE1MDMzYzY%3D; userid=1016222; user_token=NDA3NzIyYTk3YTE1MDMwZTZhY2Y1NTg2MDUwNDNlYjE%3D; Hm_lpvt_e57c2e187cc1668bba7f86d1784c0298=1711120210',
    'range': 'bytes=0-5048',
    'referer': 'https://www.sucai999.com/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'audio',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'If-None-Natch': '',
    'If-Modified-Since': '',
}

response = requests.get('https://img.sucai999.com/audio/20231230/Z9lopbBQ417pgcEzXKMrMdPBtLna2WQv.mp3', cookies=cookies,
                        headers=headers)
print(response.status_code)
with open('./radio.mp3', 'wb') as f:
    f.write(response.content)
