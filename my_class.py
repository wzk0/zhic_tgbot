import json


def refresh():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())['studentTableVms'][0]
    return data


def get_user():
    data = refresh()
    return {'department': data['department'], 'major': data['major'], 'adminclass': data['adminclass'],
            'code': data['code'], 'name': data['name']}


def search(week, weekday):
    info = []
    for d in refresh()['activities']:
        info.append({'name': d['courseName'], 'week': d['weekIndexes'], 'weekday': d['weekday'],
                     'room': '%s %s' % (d['building'], d['room']),
                     'lesson_number': '%s-%s' % (d['startUnit'], d['endUnit']),
                     'lesson_time': '%s-%s' % (d['startTime'], d['endTime']), 'index': d['startUnit']})
    if weekday % 7 == 0:
        weekday = 7
    else:
        weekday = weekday % 7
    result = []
    for i in info:
        if week in i['week']:
            if weekday == i['weekday']:
                result.append(i)
    return sorted(result, key=lambda r: r['index']), {'week': week, 'weekday': weekday}
