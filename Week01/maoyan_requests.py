import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "Cookie": 'uuid_n_v=v1; uuid=0D4275A0FCDE11EA8DE53FC79079ED948506EF224D0747679E0B9E053375C1FF; _csrf=f2a525c94fbf80bc158b93190f21678145f07fdc58f84223a6f95d797a3d75f7; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1600784127; _lxsdk_cuid=174b62b546c3c-0097a5e493b218-6313f69-100200-174b62b5471c8; _lxsdk=0D4275A0FCDE11EA8DE53FC79079ED948506EF224D0747679E0B9E053375C1FF; mojo-uuid=cb0813231b0f8fa6a55020547af2aab3; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1600865779; __mta=44414363.1600784127259.1600865395874.1600865779337.4; _lxsdk_s=174bb3093d9-0d8-572-475%7C%7C1',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.100 Safari/537.36",
}
url = "https://maoyan.com/films?showType=3"

response = requests.get(url=url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
dl_data = soup.find_all('dd')[: 10]
save_data = []
for item in dl_data:
    name = item.find('span', attrs={"class": "name"}).text
    tag = item.find("div", attrs={"class": 'movie-hover-info'}).select("div")[1].get_text().replace('类型:', '').replace(' ', '').replace('\n', '')
    release = item.find("div", attrs={"class": 'movie-hover-info'}).select("div")[3].get_text().replace('上映时间:', '').replace(' ', '').replace('\n', '')
    row = [name, tag, release]
    print(row)
    save_data.append(row)

save_df = pd.DataFrame(save_data, columns=["电影名", "类型", "上映时间"])
save_df.to_csv("./movies_requests.csv", index=False)


