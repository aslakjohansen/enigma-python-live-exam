#!/usr/bin/env python3

import xlsxwriter
import json
from copy import deepcopy

prefix = '../var/data'

course_name = 'Python Introduktion'

daily_schedule = [
    '9:00',
    '9:20',
    '9:40',
    None, # 10 min break
    '10:10',
    '10:30',
    '10:50',
    None, # 10 min break
    '11:20',
    '11:40',
    '12:00',
    None, # 40 min break
    '13:00',
    '13:20',
    '13:40',
    None, # 10 min break
    '14:10',
    '14:30',
    '14:50',
    None, # 10 min break
    '15:20',
    '15:40',
    '16:00',
    None, # 10 min break
    '16:10',
    '16:30',
]

schedule = [
    {'name': 'Mandag den 3. Maj, 2021'  , 'schedule': daily_schedule},
    {'name': 'Tirsdag den 4. Maj, 2021' , 'schedule': daily_schedule},
    {'name': 'Onsdag den 5. Maj, 2021'  , 'schedule': daily_schedule},
    {'name': 'Torsdag den 6. Maj, 2021' , 'schedule': daily_schedule},
    {'name': 'Fredag den 7. Maj, 2021'  , 'schedule': daily_schedule},
    {'name': 'Mandag den 10. Maj, 2021' , 'schedule': daily_schedule},
    {'name': 'Tirsdag den 11. Maj, 2021', 'schedule': daily_schedule},
    {'name': 'Onsdag den 12. Maj, 2021' , 'schedule': daily_schedule},
    {'name': 'Torsdag den 13. Maj, 2021', 'schedule': daily_schedule},
    {'name': 'Fredag den 14. Maj, 2021' , 'schedule': daily_schedule},
]

###############################################################################
################################################################## file helpers

def read_file (filename):
    with open(filename) as fo:
        return fo.readlines()

def write_file (filename, lines):
    with open(filename, 'w') as fo:
        fo.writelines(lines)

###############################################################################
################################################################## data loaders

def load_classes (filename):
    lines = read_file(filename)
    classes = {}
    
    for line in map(lambda line: line.strip(), lines):
        elements = list(map(lambda e: e.strip(), line.split('\t')))
        classname = elements[0]
        groupname = 'Gruppe '+elements[1]
        if not classname in classes: classes[classname] = []
        classes[classname].append(groupname)
    
    return classes

def load_group_results (filename):
    return json.loads(''.join(read_file(filename)))

def load_groups (filename):
    lines = read_file(filename)
    groups = {}
    
    group = ''
    for line in map(lambda line: line.strip(), lines):
        if line=='':
            group = ''
        elif group=='':
            group = line
        else:
            if not group in groups: groups[group] = []
            groups[group].append(line)
    
    return groups

def load_students (filename):
    lines = read_file(filename)
    
    students = {}
    for line in lines:
        es = list(map(lambda e: e.strip(), line.split(';')))
        name  = es[1]
        email = es[2]
        students[email] = name
    
    return students

def load_test_results (filename):
    lines = read_file(filename)
    
    helements = list(map(lambda e: e.strip(), lines[0][1:].split(',')))
    lines = lines[1:]
    
    header = {}
    for i in range(len(helements)):
        header[helements[i]] = i
    
    results = {}
    for line in lines:
        es = list(map(lambda e: e.strip(), line.split(',')))
        results[es[header['name']]] = {
            'test1': es[header['test1']],
            'test2': es[header['test2']],
            'test3': es[header['test3']],
        }
    
    return results

def load_data ():
    classes       = load_classes('%s/Klasser.tsv' % prefix) # class ↦ group list
    group_results = load_group_results('%s/group_grades.json' % prefix) # group ↦ score
    groups        = load_groups('%s/Grupper.data' % prefix) # group ↦ email list
    students      = load_students('%s/students.csv' % prefix) # email ↦ name
    test_results  = load_test_results('%s/test_results.csv' % prefix) # name ↦ score map
    
    entries = []
    for classname in classes:
        for groupname in classes[classname]:
            groupscore = group_results[groupname]
            for email in groups[groupname]:
                name = students[email]
                scores = test_results[name]
                
                entries.append({
                    'class': classname,
                    'group': groupname,
                    'groupscore': groupscore,
                    'email': email,
                    'name': name,
                    'test1': scores['test1'],
                    'test2': scores['test2'],
                    'test3': scores['test3'],
                })
    
    return entries

###############################################################################
####################################################################### compose

def compose_day (worksheet, formats, row, day, schedule, slotcount, handouts):
    global entries
    
    weight = lambda r: '=0.3*2*D%d+0.1*G%d+0.1*H%d+0.1*2*I%d+0.5*J%d' % (r+1, r+1, r+1, r+1, r+1)
    final = lambda r: '=IF(K%d<20,-3,IF(K%d<45,0,IF(K%d<56.75,2,IF(K%d<68,4,IF(K%d<81.5,7,IF(K%d<92.75,10,12))))))' % (r+1, r+1, r+1, r+1, r+1, r+1)
    '=12'
    
    worksheet.write(row, 0, day, formats['date'])
    row += 1
    
    # header
    worksheet.write(row, 0, 'Time', formats['bold'])
    worksheet.write(row, 1, 'Klasse', formats['bold'])
    worksheet.write(row, 2, 'Gruppe', formats['bold'])
    if not handouts:
        worksheet.write(row, 3, 'Gruppe Resultat', formats['bold'])
    worksheet.write(row, 4, 'Email', formats['bold'])
    worksheet.write(row, 5, 'Navn', formats['bold'])
    if not handouts:
        worksheet.write(row, 6, 'Test 1 Resultat', formats['bold'])
        worksheet.write(row, 7, 'Test 2 Resultat', formats['bold'])
        worksheet.write(row, 8, 'Test 3 Resultat', formats['bold'])
        worksheet.write(row, 9, 'Mundligt Resultat', formats['bold'])
        worksheet.write(row, 10, 'Vægtet Resultat', formats['bold'])
        worksheet.write(row, 11, '7-Trins Skala Resultat', formats['bold'])
    row += 1
    
    # schedule
    i = 0
    for index in range(len(schedule)):
        time = schedule[index]
        if time==None:
            worksheet.write(row, 0, '<pause>')
            row += 1
            continue
        if i>=len(entries): break
        entry = entries[i]
        
        worksheet.write(row, 0, schedule[index])
        worksheet.write(row, 1, entry['class'])
        worksheet.write(row, 2, entry['group'])
        if not handouts:
            worksheet.write(row, 3, entry['groupscore'])
        worksheet.write(row, 4, entry['email'])
        worksheet.write(row, 5, entry['name'])
        if not handouts:
            worksheet.write(row, 6, entry['test1'])
            worksheet.write(row, 7, entry['test2'])
            worksheet.write(row, 8, entry['test3'])
            worksheet.write(row, 9, '')
            worksheet.write(row, 10, weight(row))
            worksheet.write(row, 11, final(row), formats['bold'])
        
        row += 1
        i += 1
    
    entries = entries[slotcount:]
    return row

def compose (filename, handouts=False):
    # initialize
    workbook  = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    formats = {
        'bold':  workbook.add_format({'bold': True}),
        'date':  workbook.add_format({'bold': True, 'font_size': 14}),
        'title': workbook.add_format({'bold': True, 'font_size': 16}),
    }
    
    # title
    worksheet.write(0, 0, course_name, formats['title'])
    
    row = 2
    for i in range(len(schedule)):
        entry = schedule[i]
        n = entry['name']
        s = entry['schedule']
        slotcount = len(list(filter(lambda slot: slot!=None, s)))
        
        row = compose_day(worksheet, formats, row, n, s, slotcount, handouts)
        row += 1
    
    # finalize
    workbook.close()

###############################################################################
########################################################################## main

entries = load_data()
backup = deepcopy(entries)
compose('schedule.xlsx', False)
entries = backup
compose('schedule_handouts.xlsx', True)

