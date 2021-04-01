import requests
from bs4 import BeautifulSoup

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    if soup.find("div", {"class": "s-pagination"}):
      pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
      last_page = pages[-2].get_text(strip=True)
      return int(last_page)
    else:
      return 0;


def extract_job(html):
    title = html.find("a", {"class": "s-link"})["title"]
    company, location = html.find("h3").find_all("span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True).strip("-").strip("\n")
    job_id = html['data-jobid']
    image = ""
    if html.find("div", {"class": "grid--cell fl-shrink mr12 w48 h48"}):
      image = html.find("div", {"class": "grid--cell fl-shrink mr12 w48 h48"}).find("img")['src']
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://stackoverflow.com/jobs/{job_id}",
        "image": image
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: Page: {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
  url = f"https://stackoverflow.com/jobs?q={word}&sort=i"
  last_page = get_last_page(url)
  if last_page > 0:
    jobs = extract_jobs(last_page, url)
    return jobs
  else:
    return []
