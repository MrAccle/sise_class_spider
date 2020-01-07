# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests

# import mysql.connector
classUrL = list()
className = list()
# host_ = ''
# username_ = ''
# password_ =''
# database_ =''
# con = mysql.connector.connect(host=host_ ,user=username_, password=password_, database=database_, use_unicode=True)
successRow = 0

def GetClassList():  # No error
    print("this is GetClassList function")
    f = open('classList.html', 'w')
    ClassListUrl = "http://class.sise.com.cn:7001/sise/coursetemp/courseInfo.html"
    response = requests.get(ClassListUrl)
    response.encoding = 'gbk'
    htmlContent = response.text
    soup = BeautifulSoup(htmlContent)
    for i in soup.body.table:
        # i中存储的是课程div 开始解析tr
        classInfo = ""
        if hasattr(i, "contents"):
            for content in i.contents:
                # f.writelines(content)
                classInfo = content.string + ":" + classInfo
                # 判断是否是存在内容 防止其内容为'\n'报错
                if hasattr(content, "contents"):
                    # 这一层解析课程的url
                    if content.contents[0].next.contents[0].name == 'a':
                        className.append(classInfo)
                        f.writelines(classInfo + ":" + "http://class.sise.com.cn:7001/sise/coursetemp/" +
                                     content.contents[0].next.contents[0].attrs['href'] + "\n")
                        classUrL.append("http://class.sise.com.cn:7001/sise/coursetemp/" +
                                        content.contents[0].next.contents[0].attrs['href'])
                        print(classInfo)
                        classInfo = ""
    f.close()


def GetClassTime():
    # f = open('time.html','w')
    for name, url in zip(className, classUrL):
        response = requests.get(url)
        response.encoding = 'gbk'
        htmlContent = response.text
        soup = BeautifulSoup(htmlContent)
        table_node = soup.find_all('table')
        content_node = table_node[3].contents[3]
        timeStr = 65
        for i in range(0, 8):
            writeClassTime(name, timeStr, content_node)
            timeStr = timeStr + 1
            temp = content_node.contents[8]
            content_node = temp
            print(chr(timeStr))


def writeClassTime(classInfo, timeStr, node):
    f = open('t.html', 'a')
    for i in range(1, 8):
        # 节点值
        content = node.contents[i].text
        if content != '\xa0':
            print(content)
            f.writelines(classInfo + chr(timeStr) + ":" + str(i) + ":" + content + "\n")
    print("end of GetClassTime")
    f.close()


def analyClassInfos(filename):
    f = open(filename, 'r')
    f2 = open('finish.txt', 'w')
    datas = f.readlines()
    for data in datas:
        info = data.split(':')
        course_name = info[0]  # 课程名称
        course_id = info[2]  # 课程代码
        course_department = info[4]  # 开设系别
        course_time_encode = info[5] + info[6]  # 课程时间编码
        course_info = info[7].split(",")  # 课程信息
        # 注：其中分割课程的时候会有部分存在空格，所以导入数据库需要先提前清除空格
        # print(course_name+" "+course_id+" "+course_department+" "+course_time_encode)
        for course in course_info:
            if course[0] == ' ':
                course = course[1:]
            str = course.replace(' ', '|').replace('[', '|').replace('(', '|').replace(')', '').replace(']', '')
            info_list = str.split('|')
            course_code = info_list[0]
            course_teacher_name = info_list[1]
            course_class = info_list[-1].replace('\n', '')
            week_code = '00000000000000000'
            week_code_lsit = list(week_code)
            week_list = info_list[2:-1]
            list_len = len(week_list)
            week_list[list_len - 1] = week_list[list_len - 1].replace('周', '')
            for i in week_list:
                try:
                    index = int(i)
                    week_code_lsit[index - 1] = '1'
                except BaseException:
                    course_teacher_name = course_teacher_name + "," + i
            # print(course_code+" "+course_teacher_name+" "+course_class)
            week = ''.join(week_code_lsit)
            f2.writelines(
                course_id + " " + course_name + " " + course_department + " " + course_time_encode + " " + course_teacher_name + " " + course_code + " " + course_class + " " + week + "\n")
            # importToMysql(course_id,course_name,course_department,course_time_encode,course_teacher_name,course_code,course_class,week)
    f.close()
    f2.close()


#  可以导入数据库，数据库连接信息在头部修改
# def importToMysql(course_id,course_name,course_department,course_time_encode,course_teacher_name,course_code,course_class,course_week):
#
#     #print("importToMysql")
#     print(course_id+" "+course_name+" "+course_department+" "+course_time_encode+" "+course_teacher_name+" "+course_code+" "+course_class+" "+course_week)
#     sql="""
#     insert into course_info (course_id, course_name,course_department,course_time_encode,course_teacher_name,course_code,course_class,course_week)
#     values (%s, %s, %s, %s, %s, %s, %s, %s)
#     """
#     values=list()
#     values.append(course_id)
#     values.append(course_name)
#     values.append(course_department)
#     values.append(course_time_encode)
#     values.append(course_teacher_name)
#     values.append(course_code)
#     values.append(course_class)
#     values.append(course_week)
#     cursor = con.cursor()
#     cursor.execute(sql,values)
#     con.commit()
#     cursor.close()
# successRow = successRow + cursor.rowcount

if __name__ == "__main__":
    print("this is main function")
    GetClassList()
    GetClassTime()
    analyClassInfos('t.html')
    # con.close()
    # print("all finish successRow: %d " % successRow)
