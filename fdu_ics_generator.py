import re
import datetime
from bs4 import BeautifulSoup
from ics import Calendar, Event


class generator:
    soup = None
    c = Calendar()
    info = []
    map = ['一','二','三','四','五','六','日']

    start_h = (0,8,8,9,10,11,13,14,15,16,17,18,19,20)
    end_h = (0,8,9,10,11,12,14,15,16,17,18,19,20,21)
    start_m = (0,0,55,55,50,45,30,25,25,20,15,30,25,20)
    end_m = (0,45,40,40,35,30,15,10,10,5,0,15,10,5)

    term_start_time = datetime.datetime.strptime('2020-09-14 00:00:00+0800',
                                             '%Y-%m-%d %H:%M:%S%z')

    def __init__(self):
        with open("课程表.html", "rb") as f:
            html = f.read().decode("utf8")
            f.close()
        self.soup = BeautifulSoup(html, "html.parser")
        

    def parser(self):
        spt = str(self.soup.findAll('script'))
        sem = re.findall(r"var semesterIds = \[.+\]",spt)[0].lstrip('var semesterIds = [').rstrip(']').split(',')
        print('检测到如下学期，请选择(1-%d):'%len(sem))
        print(sem)
        choose = int(input())
        rows = self.soup.findAll('div', id=('list-'+sem[choose-1][1:-1]))
        for row in rows:
            columns = row.findAll('tr')
            for column in columns:
                courses = column.findAll('td')
                for course in courses:
                    course = str(course)
                    self.info.append(course)
                    #course = course.lstrip(str(re.search(r'<td>|<td rowspan=\"\d\">',course))).rstrip('</td>')
                    #print(course)
    def write_into_ics(self):
        x = 0
        while x<len(self.info):
            if "rowspan" in self.info[x]:
                num = re.findall(r"\d+",self.info[x])
                repeat = int(num[0])
                course_name = self.info[x+1].lstrip(str(re.search(r'<td>|<td rowspan=\"\d\">',self.info[x+1]))).rstrip('</td>')
                x+=2
                while repeat>0:
                    self.add_course(course_name,x)
                    x+=4
                    repeat-=1
                    
            else :
                course_name = self.info[x+1].lstrip(str(re.search(r'<td>|<td rowspan=\"\d\">',self.info[x+1]))).rstrip('</td>')
                x+=2
                self.add_course(course_name,x)
                x+=4
        
        with open('fdu.ics', 'w', encoding='utf-8') as my_file:
            my_file.writelines(self.c)
    
    def add_course(self,course_name,start):
        local = self.info[start].lstrip(str(re.search(r'<td>|<td rowspan=\"\d\">',self.info[start]))).rstrip('</td>')
        weekday = re.findall(r"星期.",self.info[start+1])[0].lstrip('星期')
        weekday = self.map.index(weekday)
        time = re.findall(r"\d+",self.info[start+1])
        week = self.info[start+2].lstrip('</td>第').rstrip('周</td>')
        remark = self.info[start+3].lstrip('</td>').rstrip('</td>')
        
        e = Event()
        if('-' in week):
            week = week.split('-')
            #print(week)
            week_cur = int(week[0])
            week_end = int(week[1])
            while week_cur <= week_end:
                e = Event()
                e.name = course_name
                e.location = local
                e.description = remark
                offset = datetime.timedelta(days=(week_cur-1)*7+weekday,hours=self.start_h[int(time[0])],minutes=self.start_m[int(time[0])])
                e.begin = self.term_start_time + offset
                offset = datetime.timedelta(days=(week_cur-1)*7+weekday,hours=self.end_h[int(time[1])],minutes=self.end_m[int(time[1])])
                e.end = self.term_start_time + offset
                week_cur+=1
                self.c.events.add(e)
        else:
            week = week.split(',')
            #print(week)
            for we in week:
                e = Event()
                e.name = course_name
                e.location = local
                e.description = remark
                offset = datetime.timedelta(days=(int(we)-1)*7+weekday,hours=self.start_h[int(time[0])],minutes=self.start_m[int(time[0])])
                e.begin = self.term_start_time + offset
                offset = datetime.timedelta(days=(int(we)-1)*7+weekday,hours=self.end_h[int(time[1])],minutes=self.end_m[int(time[1])])
                e.end = self.term_start_time + offset
                self.c.events.add(e)


def main():
    g = generator()
    g.parser()
    g.write_into_ics()

if __name__ == '__main__':
    main()

