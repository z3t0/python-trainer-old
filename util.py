from os.path import isdir
import os
import sys

import json

import runner

config_path = 'config.json'
config = {
    'lesson_dir': 'lessons',
    'current_lesson': '',
}


def set_dir():
    lesson_dir = ''

    while not isdir(lesson_dir):
        lesson_dir = input("Please enter the path to the lessons: ")

    return lesson_dir


def setup():
    config['lesson_dir'] = set_dir()

    print("Setup was successful")
    print("Lessons directory: " + config['lesson_dir'])

    print("Run ./trainer.py to begin")

    save()


def init():
    global config

    # Load config
    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
    except EnvironmentError:
        print("Config is missing, please run ./trainer.py setup")


def save():
    try:
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file)
    except EnvironmentError:
        print("Could not find config")


def select(index):
    path = config['lesson_dir']

    lessons = next(os.walk(path))[1]

    lesson_dir = path + '/' + lessons[index]

    try:
        with open(lesson_dir + '/info.md') as f:
            lesson = f.read().strip()

        import mdvl
        mdvl.main(lesson)

        config['current_lesson'] = lesson_dir
    except EnvironmentError:
        print('Lesson is incorrectly structured')

    save()

def test():
    lesson = config['current_lesson']
    if not lesson:
        print('No lesson has been selected...')
        print('Please add lessons')

        return

    sys.path.insert(0, lesson)
    runner.run_test(lesson)
