from datetime import datetime as dt
# import requests
import json

week=17
weekday=dt.now().isoweekday()

# cookies={'SESSION':'','__pstsid__':''}

# r=requests.get('https://eams.tjzhic.edu.cn/student/for-std/course-table/semester/41/print-data?semesterId=41&hasExperiment=true',cookies=cookies)
# data=json.loads(r.text)['studentTableVms'][0]['activities']
with open('data.json','r')as f:
	data=json.loads(f.read())['studentTableVms'][0]['activities']
lesson_data=[]
for d in data:
	lesson_data.append({'课程代码':d['courseCode'],'课程名称':d['courseName'],'上课周':d['weekIndexes'],'上课周数':str(d['periodInfo']['weeks']),'教室':d['room'],'教学楼':d['building'],'校区':d['campus'],'星期':d['weekday'],'老师':d['teachers'],'课程类型':d['courseType']['nameZh'],'学分':str(d['credits']),'课时':str(d['periodInfo']['total']),'上课时间':d['startTime'],'下课时间':d['endTime']})

def get_today(weekday=weekday,week=week):
	today=[]
	for dd in lesson_data:
		if (week in dd['上课周']) and (weekday==dd['星期']):
			today.append(dd)
	return today

