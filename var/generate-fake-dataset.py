#!/usr/bin/env python3

import json
import random

STUDENT_COUNT = 200
GROUP_SIZE = 5
CLASS_COUNT = 8

def load_lines (filename):
    with open(filename) as fo:
        return fo.readlines()

def write_lines (filename, lines):
    if type(lines)==str: lines = [lines]
    with open(filename, 'w') as fo:
        fo.writelines(lines)

def read_name_basics (filename):
    db = []
    lines = load_lines(filename)
    for line in lines[1:STUDENT_COUNT+1]:
        elements = line.strip().split('\t')
        identity = int(elements[0][2:])
        name     = elements[1]
        byear    = 2020 if elements[2]=='\\N' else int(elements[2])
        dyear    = 2020 if elements[3]=='\\N' else int(elements[3])
        prof     = len(elements[4])
        known    = sum(map(lambda title: int(title[2:]), elements[5].split(','))) % 200
        db.append({
            'id':    identity,
            'email': 'student%03d@du.dk' % identity,
            'name':  name,
            'birth': byear,
            'death': dyear,
            'prof':  prof,
            'known': known,
        })
    return db

def scale (db, key, scalemin, scalemax):
    minvalue = min(map(lambda entry: entry[key], db))
    maxvalue = max(map(lambda entry: entry[key], db))
    scaler = lambda inputvalue: scalemin + (inputvalue-minvalue)/(maxvalue-minvalue)*(scalemax-scalemin)
    for entry in db:
        entry[key] = scaler(entry[key])

def produce_group_file (db, filename):
    groups = {}
    for i in range(len(db)):
        entry = db[i]
        groupid = 'Gruppe %d' % (i//GROUP_SIZE+1)
        if not groupid in groups: groups[groupid] = []
        groups[groupid].append(entry['email'])
        entry['group'] = groupid
    
    group_names = list(groups.keys())
    random.shuffle(group_names)
    
    lines = []
    for group_name in group_names:
        lines.append('%s\n' % group_name)
        for email in groups[group_name]:
            lines.append('%s\n' % email)
        lines.append('\n')
    write_lines(filename, lines)

def produce_class_file (db, filename):
    groups = list(set(map(lambda entry: entry['group'], db)))
    classes = list(map(lambda i: [], range(CLASS_COUNT)))
    for i in range(len(groups)):
        group = groups[i]
        classes[i%CLASS_COUNT].append(group)
    
    lines = []
    for i in range(len(classes)):
        groups = classes[i]
        for group in groups:
            lines.append('Klasse %d\t%s\n' % (i, group.split(' ')[1]))
    write_lines(filename, lines)

def produce_group_grade_file (db, filename):
    groups = list(set(map(lambda entry: entry['group'], db)))
    
    data = {}
    for group in groups:
        members = list(filter(lambda entry: entry['group']==group, db))
        score = int(sum(map(lambda entry: entry['known'], members))/len(members))
        data[group] = score
    
    write_lines(filename, json.dumps(data))

def produce_test_result_file (db, filename):
    lines = ['# name, test2, test1, test3\n']
    for entry in db:
        name  = entry['name']
        test1 = entry['birth']
        test2 = entry['death']
        test3 = entry['prof']
        lines.append('%s ,%f, %f, %f\n' % (name, test2, test1, test3))
    
    write_lines(filename, lines)

db = read_name_basics('name.basics.tsv')

scale(db, 'birth', 0, 100)
scale(db, 'death', 0, 100)
scale(db, 'prof', 0, 50)
scale(db, 'known', 0, 100)

random.seed(42) # ensure consistent order
random.shuffle(db)

for entry in db:
    print('%3d %20s %3d %3d %3d %3d' % (entry['id'], entry['name'], entry['birth'], entry['death'], entry['prof'], entry['known']))

produce_group_file(db, 'data/Grupper.data')
produce_class_file(db, 'data/Klasser.tsv')
produce_group_grade_file(db, 'data/group_grades.json')
produce_test_result_file(db, 'data/test_results.csv')

