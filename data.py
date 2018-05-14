import json
from git import Repo
from uuid import uuid4
from os.path import join
import os

DATA_PATH = ".data/"
CACHE_PATH = DATA_PATH + "cache.json"

cache = {
    'lesson_books': [],
    'completed_lesson_books': [],
    'completed_lessons': [],
    'current_lesson_book': None,
    'current_lesson': None,
    }

def load():
    global cache

    # Load config
    try:
        with open(CACHE_PATH) as c:
            cache = json.load(c)
    except EnvironmentError:
        print("Cache is missing")


def save():
    try:
        with open(CACHE_PATH, 'w') as c:
            json.dump(cache, c)
    except EnvironmentError:
        print("Could not find cache")


def get_lesson_books():
    """return a list of lessons"""
    return cache['lesson_books']

def get_lesson_books_lst():
    l = cache['lesson_books']
    lst = []

    for le in l:
        with open(le['path'] + '/lesson_book.md') as info:
            title = info.readline()

        def action():
            return le['lessons']

        lst.append({
            'string': title,
            'action': action
        })

    return lst


def add_lesson(repo_url):

    uuid = str(uuid4())
    path = join(DATA_PATH + "lesson_books/" + str(uuid))

    try:
        Repo.clone_from(repo_url, path)

        lessons = next(os.walk(path))[1]

        cache['lesson_books'].append({
            'id': uuid,
            'path': path,
            'lessons': lessons
        })

    except:
        raise("Failed to clone lesson book repository")


    save()

def main():
    add_lesson("https://github.com/z3t0/python-trainer-sample-lesson-book")


load()

if __name__ == "__main__":
    main()
