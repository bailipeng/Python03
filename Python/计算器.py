import tkinter
import math
class Calc:

    def __init__(self):
        #初始化界面

        self.isop = False      #判断是否按下了运算符
        self.iseqaul = False   #判断是否按下了等于号=
        self.numlists = []      #用于接收运算式的列表
        self.tkwindow() #初始化界面函数
    def tkwindow(self):  #就是它
        root=tkinter.Tk()
        root.title('小路计算器')
        root.minsize(330,460)
        root.maxsize(330,460)
        #计算器显示框
        self.num = tkinter.StringVar()
        self.num.set(0)
        label = tkinter.Label(root,textvariable=self.num,font=('微软雅黑',30),bg='white',anchor='e')

        label.place(x=10,y=10,width=310,height=50)

        '''======================================================运算符号部分========================================================='''
        #运算按钮
        #符号%
        btnys1 = tkinter.Button(root,text='%',bd=1,font=('微软雅黑',15),command=lambda:self.Operation('%')).place(x=10,y=70,width=70,height=55)

        #符号√
        btnys2 = tkinter.Button(root,text='√',bd=1,font=('微软雅黑',15),command=lambda:self.srqtnum(self.num.get())).place(x=90,y=70,width=70,height=55)

        #符号x²
        btnys3 = tkinter.Button(root,text='x²',bd=1,font=('微软雅黑',15),command=lambda:self.Operation('**')).place(x=170,y=70,width=70,height=55)

        #符号1/x
        btnys4 = tkinter.Button(root,text='1/x',bd=1,font=('微软雅黑',15),command=lambda:self.grade()).place(x=250,y=70,width=70,height=55)

        #符号CE
        btnys5 = tkinter.Button(root,text='CE',bd=1,font=('微软雅黑',15),command=lambda:self.clearnum()).place(x=10,y=135,width=70,height=55)

        #符号C
        btnys6 = tkinter.Button(root,text='C',bd=1,font=('微软雅黑',15),command=lambda:self.clearnum()).place(x=90,y=135,width=70,height=55)

        #符号删除
        btnys6 = tkinter.Button(root,text='Del',bd=1,font=('微软雅黑',15),command=lambda:self.Dellists()).place(x=170,y=135,width=70,height=55)

        #符号除法
        btnys6 = tkinter.Button(root,text='÷',bd=1,font=('微软雅黑',15),command=lambda:self.Operation('/')).place(x=250,y=135,width=70,height=55)

        #符号乘法
        btnys6 = tkinter.Button(root,text='X',bd=1,font=('微软雅黑',15),command=lambda:self.Operation('*')).place(x=250,y=200,width=70,height=55)

        #符号减法
        btnys6 = tkinter.Button(root,text='－',bd=1,font=('微软雅黑',20),command=lambda:self.Operation('-')).place(x=250,y=265,width=70,height=55)

        #符号加法
        btnys6 = tkinter.Button(root,text='＋',bd=1,font=('微软雅黑',20),command=lambda:self.Operation('+')).place(x=250,y=330,width=70,height=55)

        #符号等于
        btnys6 = tkinter.Button(root,text='=',bd=1,font=('微软雅黑',15),command=lambda:self.result()).place(x=250,y=395,width=70,height=55)

        #符号正负号
        btnys6 = tkinter.Button(root,text='±',bd=1,font=('微软雅黑',15),command=lambda:self.mathsign()).place(x=10,y=395,width=70,height=55)

        '''======================================================数字部分========================================================='''

        #数字按钮
        #符号.
        btnys6 = tkinter.Button(root,text='.',bd=1,font=('微软雅黑',20,'bold'),command=lambda:self.shownnum('.')).place(x=170,y=395,width=70,height=55)
        #按钮0
        btn0 = tkinter.Button(root,text='0',bd=1,font=('微软雅黑',20),command=lambda:self.shownnum('0')).place(x=90,y=395,width=70,height=55)

        #按钮1
        btn1 = tkinter.Button(root,text='1',bd=1,font=('微软雅黑',20),command=lambda:self.shownnum('1')).place(x=10,y=330,width=70,height=55)

        #按钮2
        btn2 = tkinter.Button(root,text='2',bd=1,font=('微软雅黑',20),command=lambda:self.shownnum('2')).place(x=90,y=330,width=70,height=55)

        #按钮3
        btn3 = tkinter.Button(root,text='3',bd=1,font=('微软雅黑',20),command=lambda:self.shownnum('3')).place(x=170,y=330,width=70,height=55)

        #按钮4
        btn4 = tkinter.Button(root,text='4',bd=1,font=('微软雅黑',20),command=lambda:self.shownnum('4')).place(x=10,y=265,width=70,height=55)

        #按钮5
        btn5 = tkinter.Button(root,text='5',bd=1,font=('微软雅黑',20),command=lambda:self.shownnum('5')).place(x=90,y=265,width=70,height=55)

        #按钮6
        btn6 = tkinter.Button(root,text='6',bd=1,font=('微软雅黑',20),command=lambda:self.shownnum('6')).place(x=170,y=265,width=70,height=55)

        #按钮7
        btn7 = tkinter.Button(root,text='7',bd=1,font=('微软雅黑',20),command=lambda:self.shownnum('7')).place(x=10,y=200,width=70,height=55)

        #按钮8
        btn8 = tkinter.Button(root,text='8',bd=1,font=('微软雅黑',20),command=lambda:self.shownnum('8')).place(x=90,y=200,width=70,height=55)

        #按钮9
        btn9 = tkinter.Button(root,text='9',bd=1,font=('微软雅黑',20),command=lambda:self.shownnum('9')).place(x=170,y=200,width=70,height=55)
        
    #将用户输入的数字显示到屏幕中
    def shownnum(self,inputnum):

        if self.iseqaul == True or self.isop==True or (self.num.get()=='0' and inputnum !='.'):   #按下了运算符，等号，显示界面为0 ，不为小数点的情况下
            self.num.set(inputnum)
            self.iseqaul = False      #将等号复位
            self.isop=False           #将运算符复位       
        else:
            showstr = self.num.get()+inputnum
            if showstr.count('.')>1:   #判断小数点.的数量，若大于1取消输入
                pass
            else:                  
                self.num.set(self.num.get()+inputnum)#将用户输入的信息和原有的信息一起显示       
    #运算按钮
    def Operation(self,sign):
        self.isop = True
        self.numlists.append(self.num.get())     #按下运算按钮之后，将显示框目前的数字存入列表
        if self.numlists[-1] != sign:
            self.numlists.append(sign)          #将运算符号存入列表
        print(self.numlists)

            
    #输出结果
    def result(self):
        self.iseqaul = True #按下了等于

        self.numlists.append(self.num.get())     #将运算符之后的数字加入列表
        a = eval(''.join(self.numlists))
        b = '{:.6}'.format(str(a))               #将结果的精度限制为小数点后4位
        if b.endswith('0')==True and '.' in b :     #末尾是零且有.  将0去掉
            b=b.rstrip('0')

        if b.endswith('.')==True:     #如果且末尾是.   将.去掉
            b=b.rstrip('.')      
        if b=='':      #如果结果为空 ,将结果显示为0
            b='0'            
        self.num.set(b)
        self.numlists=[]    #将列表清零
    #清零操作
    def clearnum(self):
        self.num.set(0)    #将显示框显示为0
        self.numlists.clear()  #将列表清空
        self.iseqaul = False
    #开平方操作
    def srqtnum(self,num):
        result1 = '{:.5}'.format(str(math.sqrt(float(self.num.get()))))
        self.num.set(result1)
    #1/x 操作
    def grade(self):

        result1 = '{:.5}'.format(str(1/(float(self.num.get()))))
            
        self.num.set(result1)
    #删除操作
    def Dellists(self):
        numlist1 = list(self.num.get())
        if len(numlist1)>1:
                
            numlist1.pop()
            numlist1 =''.join(numlist1)
            self.num.set(numlist1)
                
        elif len(numlist1)==1:
                
            self.num.set(0)

    #正负号操作
    def mathsign(self):
        strsign=str(self.num.get())
        if strsign.startswith('-')==True or strsign=='0':
            self.num.set(strsign.lstrip('-'))
            
        else:
            self.num.set('-'+strsign)
        
calc=Calc()   
    


'''======================================================绑定事件，改变颜色========================================================='''
'''
#改变背景色的方法
def chbg(evt):
    
    evt.widget['bg'] = 'white'
    
def backbg(evt):

    evt.widget['bg'] = '#f0f0f0'
    
btn9.bind_class('Button','<Leave>',backbg)
btn9.bind_class('Button','<Enter>',chbg)
'''
#root.mainloop()
