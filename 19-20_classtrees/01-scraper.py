import requests
import json
from bs4 import BeautifulSoup
from multiprocessing import Pool

urls = json.load(open("00-catalog_urls.json"))


def process(url):
    print(f"scraping {url}")
    r = requests.get(url)
    r.raise_for_status()
    html = r.text
    s = BeautifulSoup(html, features="html.parser")
    print("parsed response")
    course_block = s.find_all("div", class_="rich-text")[1]
    course_p = course_block.find_all("p")
    print("iterating courses")
    courses = []
    for p in course_p:
        ems = p.find_all("em")
        title_block = p.find("strong")
        if title_block is None:
            continue
        courses.append(
            {
                "title": p.find("strong").get_text(),
                "schedule": ems[0].get_text() if len(ems) > 0 else None,
                "prereq": ems[1].get_text() if len(ems) > 1 else None,
                "desc": str(p.contents[-1]),
            }
        )
        print(f"appended f{courses[-1]}")
    return courses


with Pool(10) as p:
    dept_courses = p.map_async(process, urls).get()
flat_courses = [course for dept in dept_courses for course in dept]

with open("02-all_courses_scraped.json", "w") as f:
    json.dump(flat_courses, f)
