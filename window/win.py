import tkinter
import main
from tkinter import messagebox

win = tkinter.Tk()


def getClassList_btn_fun():
    # print("fun")
    main.GetClassList()
    messagebox.showinfo("获取成功", "课程列表:classList.html ")


def getClassTime_btn_fun():
    main.GetClassTime()
    messagebox.showinfo("获取课程时间段完成", "课程时间段:t.hmtl")


def ClassAnalysis_btn_fun():
    main.analyClassInfos('t.html')
    messagebox.showinfo("课表整理分析完成", "课程整理分析:finish.txt")


def initWindow():
    win.title("一键下载sise所有课程")
    win.geometry('300x90')

    getClassList_btn = tkinter.Button(win, text="获取课程列表", command=getClassList_btn_fun, bg="red")
    getClassTime = tkinter.Button(win, text="获取课程时间段", command=getClassTime_btn_fun, bg="yellow")
    ClassAnalysis = tkinter.Button(win, text="课表整理分析", command=ClassAnalysis_btn_fun, bg="pink")
    getClassList_btn.pack(fill=tkinter.X)
    getClassTime.pack(fill=tkinter.X)
    ClassAnalysis.pack(fill=tkinter.X)
    win.mainloop()


if __name__ == '__main__':
    initWindow()