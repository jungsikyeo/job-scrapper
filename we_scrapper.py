import requests
from bs4 import BeautifulSoup

def get_view_all_links(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    if soup.find("section", {"class": "jobs"}):
      sections = soup.find_all("section", {"class": "jobs"})
      view_all_links = []
      for section in sections:
        view_all_link = section.find("li", {"class": "view-all"}).find("a")['href']
        view_all_links.append(view_all_link)
      return view_all_links
    else:
      return [];


def extract_job(html):
    for contents in html.children:
      if contents.name == "a":
        title = ""
        company = ""
        location = ""
        job_link = ""
        image = ""
        if contents.find("span", {"class": "title"}):
          title = contents.find("span", {"class": "title"}).string
        if contents.find("span", {"class": "company"}):
          company = contents.find("span", {"class": "company"}).string
        if contents.find("span", {"class": "region company"}):
          location = contents.find("span", {"class": "region company"}).string
        if contents['href']:
          job_link = contents['href']
        if contents.find("div", {"class": "flag-logo"}):
          image = contents.find("div", {"class": "flag-logo"})['style'].split("?")[0].replace("background-image:url(", "")
        return {
            "title": title,
            "company": company,
            "location": location,
            "link": f"https://weworkremotely.com{job_link}",
            "image": image
        }


def extract_jobs(links):
    jobs = []
    for link in links:
      print(f"Scrapping WE: URL: {link}")
      result = requests.get(f"https://weworkremotely.com{link}")
      soup = BeautifulSoup(result.text, "html.parser")
      li_list = soup.find("section", {"class": "jobs"}).find("article").find("ul").find_all("li")
      for li in li_list[0:-2]:
        if li['class'] == None or "feature" in li['class']:
          job = extract_job(li)
          jobs.append(job)
    return jobs


def get_jobs(word):
  url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
  view_all_links = get_view_all_links(url)
  jobs = extract_jobs(view_all_links)
  return jobs

