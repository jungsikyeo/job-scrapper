import csv

def save_to_file(total_jobs):
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["title", "company", "location", "apply_link"])
  for job in total_jobs['so']:
    writer.writerow(list(job.values())[0:4])
  for job in total_jobs['we']:
    writer.writerow(list(job.values())[0:4])
  for job in total_jobs['ok']:
    writer.writerow(list(job.values())[0:4])
  return