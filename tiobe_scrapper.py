import requests
from bs4 import BeautifulSoup

def get_tiobe_top20():
  top20 = []

  result = requests.get("https://www.tiobe.com/tiobe-index/")
  soup = BeautifulSoup(result.text, "html.parser")
  top20_table = soup.find("table", {"id": "top20"})
  top20_ths = top20_table.find("thead").find("tr").find_all("th")
  ths_list = []
  for th in top20_ths:
    ths_list.append(th.string)
  top20.append({
    "current yyyymm": ths_list[0],
    "before yyyymm": ths_list[1],
    "Change_img": ths_list[2],
    "Programming Language": ths_list[3],
    "Ratings": ths_list[4],
    "Change": ths_list[5]
  })
  top20_trs = top20_table.find("tbody").find_all("tr")
  for tr in top20_trs:
    if tr.contents[2].find("img"):
      change_img_url = "https://www.tiobe.com"+tr.contents[2].find("img")['src']
    else:
      change_img_url = ""
    top20.append({
      "current yyyymm": tr.contents[0].string,
      "before yyyymm": tr.contents[1].string,
      "Change_img": change_img_url,
      "Programming Language": tr.contents[3].string,
      "Ratings": tr.contents[4].string,
      "Change": tr.contents[5].string
    })
  return top20
