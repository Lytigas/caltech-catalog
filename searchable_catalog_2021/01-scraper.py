import requests
import json
from bs4 import BeautifulSoup
from multiprocessing import Pool
from collections import namedtuple, defaultdict

Course = namedtuple(
    "Course",
    [
        "label",
        "title",
        "units",
        "terms",
        "description",
        "instructors",
        "full_text",
        "offered",
    ],
)


def process(url):
    print(f"scraping {url}")
    r = requests.get(url)
    r.raise_for_status()
    html = r.text
    s = BeautifulSoup(html, features="html.parser")
    print("parsed response")
    course_descriptions = s.find_all("div", class_="course-description")

    def course_from_desc(desc):
        def extract_key(key):
            span = desc.find("span", class_=key)
            if not span:
                return None
            return span.get_text()

        return Course(
            label=extract_key("course-description__label"),
            title=extract_key("course-description__title"),
            units=extract_key("course-description__units"),
            terms=extract_key("course-description__terms"),
            description=extract_key("course-description__description"),
            instructors=extract_key("course-description__instructors"),
            full_text=desc.get_text(),
            offered=bool("course-description--not-offered" not in desc["class"]),
        )

    print("iterating courses")
    courses = []
    for desc in course_descriptions:
        courses.append(course_from_desc(desc))
    return courses


def dedup_by_label(catalog):
    # merge courses by code, prefering the longer descriptions
    index = defaultdict(list)
    for course in catalog:
        index[course.label].append(course)
    new_catalog = []
    for courses in index.values():
        new_entry = max(courses, key=lambda c: len(c.full_text))
        new_catalog.append(new_entry)
    return new_catalog


if __name__ == "__main__":
    urls = json.load(open("00-catalog_urls.json"))
    with Pool(10) as p:
        dept_courses = p.map_async(process, urls).get()
    flat_courses = [course for dept in dept_courses for course in dept]
    catalog = dedup_by_label(flat_courses)
    catalog_dicts = [c._asdict() for c in catalog]
    with open("02-all_courses_scraped.json", "w") as f:
        json.dump(catalog_dicts, f)
