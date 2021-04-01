import requests
from bs4 import BeautifulSoup

def extract_job(html):
  result = html.find("td", {"class": "company position company_and_position"})
  title = ""
  company = ""
  location = ""
  job_link = ""
  image = ""
  if result.find("h2", {"itemprop": "title"}):
    title = result.find("h2", {"itemprop": "title"}).string
  if result.find("h3", {"itemprop": "name"}):
    company = result.find("h3", {"itemprop": "name"}).string
  if result.find("div", {"class": "location"}):
    location = result.find("div", {"class": "location"}).string
  if result.find("a", {"class": "preventLink"}):
    job_link = result.find("a", {"class": "preventLink"})['href']
  if html.find("td", {"class": "image has-logo"}).find("img", {"class": "logo"}):
    image = html.find("td", {"class": "image has-logo"}).find("img", {"class": "logo"})['src']
  return {
      "title": title,
      "company": company,
      "location": location,
      "link": f"https://remoteok.io{job_link}",
      "image": image
  }

def extract_jobs(url):
    jobs = []
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    jobsboard = soup.find("table", {"id": "jobsboard"})
    print(f"Scrapping OK: URL: {url}")
    if jobsboard:
      trs = jobsboard.find_all("tr", class_="job")
      for tr in trs:
        time = tr.find("td", {"class": "time"})
        if time and "d" in time.string:
          job = extract_job(tr)
          jobs.append(job)
    return jobs


def get_jobs(word):
  url = f"https://remoteok.io/remote-{word}-jobs"
  jobs = extract_jobs(url)
  return jobs

