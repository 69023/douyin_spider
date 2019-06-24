import requests
import re
import os

from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError

headers = {
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    "user-agent": "Aweme 3.1.0 rv:31006 (iPhone; iOS 12.0; zh_CN) Cronet"
}

share_page_url = "https://www.iesdouyin.com/share/user/{}"
share_id_ = "102554130029"
share_video_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?user_id={}&count=21&max_cursor=0&aid=1128&_signature={}&dytk={}"


def get_tac_dk(share_id):
    conn = requests.get(
        url=share_page_url.format(share_id),
        headers=headers
    )
    content = conn.text

    tac = re.search("<script>tac='(.*?)'</script>", content).group(1)
    dtk = re.search("dytk: '(.*?)'", content).group(1)

    with open("template.js", 'r', encoding="utf-8") as f:
        template_js = f.read()
    with open("crack.js", 'w', encoding="utf-8") as f2:
        template_js = template_js.replace("^^^^", share_id)
        template_js = template_js.replace("&&&&", tac)
        template_js = template_js.replace("#####", dtk)
        f2.write(template_js)

    signature = os.popen("node crack.js").readlines()[0].strip()

    return dtk, signature


def handle_request(url):
    conn = requests.get(
        url=url,
        # proxies={
        #     "http": "http://t2:t2@111.231.162.224:1111"
        # },
        headers=headers
    )
    return conn.json()


def get_user_video_info(share_id):
    dtk, signature = get_tac_dk(share_id)

    print(dtk)
    print(signature)

    # params = {
    #     "user_id": share_id,
    #     "count": "21",
    #     "max_cursor": "0",
    #     "aid": "1128",
    #     "_signature": signature,
    #     "dytk": dtk,
    # }

    url = share_video_url.format(share_id, signature, dtk)
    print("current url is:", url)

    for i in range(5):
        conn = handle_request(url=url)
        if conn.get('aweme_list') != []:
            print(conn)
            break
    else:
        print("没有拿到数据")


if __name__ == '__main__':
    get_user_video_info(share_id_)
