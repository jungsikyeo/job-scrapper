"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

from flask import Flask, render_template, request, redirect, send_file
from so_scrapper import get_jobs as get_so_jobs
from we_scrapper import get_jobs as get_we_jobs
from ok_scrapper import get_jobs as get_ok_jobs
from tiobe_scrapper import get_tiobe_top20
from export import save_to_file
app = Flask("SuperScrapper")

db = {}
ranking_db = {}

@app.route("/")
def home():
  top20 = get_tiobe_top20()
  return render_template("index.html", top20=top20)

@app.route("/report")
def report():
  word = request.args.get("word")
  total_jobs = {}
  resultsNumber = 0
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      total_jobs = existingJobs
    else:
      so_jobs = get_so_jobs(word)
      resultsNumber = resultsNumber + len(so_jobs)
      we_jobs = get_we_jobs(word)
      resultsNumber = resultsNumber + len(we_jobs)
      ok_jobs = get_ok_jobs(word)
      resultsNumber = resultsNumber + len(ok_jobs)
      total_jobs = {"so": so_jobs, "we": we_jobs, "ok": ok_jobs, "resultsNumber": resultsNumber}
      db[word] = total_jobs
  else:
      return redirect("/")
  return render_template("report.html", searchingBy=word, total_jobs=total_jobs)

@app.route("/export")
def export():
  try:
    word = request.args.get("word")
    if not word:
      raise Exception()
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      total_jobs = existingJobs
    else:
      so_jobs = get_so_jobs(word)
      we_jobs = get_we_jobs(word)
      ok_jobs = get_ok_jobs(word)
      total_jobs = {"so": so_jobs, "we": we_jobs, "ok": ok_jobs}
      db[word] = total_jobs
    print(total_jobs)
    save_to_file(total_jobs)
    return send_file("jobs.csv")
  except:
      return redirect("/")

@app.route("/tiobe")
def tiobe():
  top20 = get_tiobe_top20()
  return render_template("tiobe.html", top20=top20)

app.run(host="0.0.0.0")