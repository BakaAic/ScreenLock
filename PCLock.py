#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Tkinter import *
import tkFont
from ttk import *
import random
import ConfigParser
import codecs
import threading
import socket
import ctypes,inspect


class CodeStream():
	def __init__(self):
		self.CurCodeStream=[]
		self.ConfigPath='UserConfig.ini'
		self.SparkState=False
		self.CurBeanForward=random.choice(['left','right','up','down'])
		self.BeanM=self.BeanDone(self.CurBeanForward)
		self.MouthState=True
		self.MouthStep=0
		self.Lock=True
		self.SafeAccount='Aikko'
		self.SafePassword='00000000'
		self.AccountState=False
		self.UserList=[]
		self.PassList=[]
		self.AccountList={}
		self.GetConfig()
		#=====FaceCheck=====#
		self.root4exist=False
		self.GetLink=self.GetLinkByCheckServer(self)
		self.GetLink()
		self.Debug=False
	class GetLinkByCheckServer():
		def __call__(self):
			self.tmp=threading.Thread(target=self.Loop)
			self.tmp.start()
		def __init__(self,root):
			self.root=root
			self.Host = '0.0.0.0'
			self.Port = 10911
			self.state = True
		def End(self):
			try:
				stop_thread(self.tmp)
			except Exception,e:
				print e
		def Loop(self):
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.bind((self.Host,self.Port))
			while True:
				data, addr = s.recvfrom(1024)
				if data=='True':
					self.CallUnlock()
		def CallUnlock(self):
			if self.root.root4exist:
				self.root.FaceUnlock()
	def __call__(self):
		self.Main()
	def GetConfig(self):
		self.conf=ConfigParser.ConfigParser()
		try:
			self.conf.readfp(codecs.open(self.ConfigPath,'r','utf-8-sig'))
		except Exception,e:
			print('ErrorConfigGet')
			print(e)
			return False
		else:
			try:
				self.UserList=self.conf.sections()
				self.PassList=[]
				for u in self.UserList:
					self.PassList.append(self.conf.get(u,'Password'))
				self.AccountList=dict(zip(self.UserList,self.PassList))
			except:
				self.UserList=[]
				self.PassList=[]
				self.AccountList={}
				print('ErrorReading')
				return False
		return True
	def BinCodeWindow(self):
		self.root=Tk()
		self.root.wm_title('Hack')
		self.root.attributes("-toolwindow", 1)
		self.root.wm_attributes("-topmost", 1)
		self.root.resizable(False,False)
		self.root.overrideredirect(True)
		self.root.attributes("-alpha", 0.80)
		# self.root.geometry('400x500+120+100')
		self.root.geometry(str(self.root.winfo_screenwidth())+'x'+str(self.root.winfo_screenheight())+'+0+0')
		self.root['background']='black'
		self.root.protocol('WM_DELETE_WINDOW',self.MainGUIExit)
		self.L1=Label(self.root,background='black',foreground='green',text='')
		self.L1.pack(fill=BOTH)
		self.root.bind_all('<Button-1>',self.DestoryAccountWindows)
		self.root.after(60,self.RunCode)
	def WarnningWindows(self):
		self.root2=Tk()
		self.font = tkFont.Font(self.root2,family = 'System',size = 20)
		self.root2.wm_title('Warnning')
		self.root2.resizable(False,False)
		self.root2.attributes("-toolwindow", 1)
		self.root2.wm_attributes("-topmost", 1)
		self.root2.overrideredirect(True)
		self.root2.attributes("-alpha", 0.70)
		self.root2.geometry('240x80+'+str((self.root2.winfo_screenwidth()-240)/2)+'+'+str((self.root2.winfo_screenheight()-80)/2))
		self.root2['background']='black'
		self.root2.protocol('WM_DELETE_WINDOW',self.MainGUIExit)
		self.WarnningText=Label(self.root2,background='black',foreground='red',text='Account Refuse',font=self.font)
		self.WarnningText.place(rely=0.5,relx=0.5,anchor=CENTER)
		self.root2.bind_all('<Button-1>',self.AccountWindows)
		self.root2.after(500,self.WarnningSpark)
		# self.root2.withdraw()
		# self.root2.deiconify()
	def DestoryAccountWindows(self,event):
		if self.Lock:
			self.root4exist=False
			try:
				self.root4.destroy()
			except:
				pass
	def BeanWindows(self):
		self.root3=Tk()
		self.root3.wm_title('Bean')
		self.root3.resizable(False,False)
		self.root3.attributes("-toolwindow", 1)
		self.root3.wm_attributes("-topmost", 1)
		self.root3.overrideredirect(True)
		self.root3.attributes("-alpha", 0.70)
		self.root3.geometry('80x80')
		self.cv_root3=Canvas(self.root3,width=80,height=80,background='black',highlightbackground='black')
		self.cv_root3.pack(fill=BOTH,anchor=CENTER)
		self.cv_root3.create_oval((10,10,70,70),fill = 'yellow')
		self.cv_root3.create_arc((10,10,70,70),style = PIESLICE,start = 269,extent = 3,fill = 'black',tag='BeanMouth')
		self.root3['background']='black'
		self.root3.after(10,self.BeanMove)
	def AccountWindows(self,event):
		if not self.root4exist:
			self.root4=Tk()
			self.root4exist=True
			self.font = tkFont.Font(self.root4,family = 'System',size = 15)
			self.root4.wm_title('Account Login')
			self.root4.resizable(False,False)
			self.root4.attributes("-toolwindow", 1)
			self.root4.wm_attributes("-topmost", 1)
			self.root4.attributes("-alpha", 0.8)
			self.root4.geometry('400x200+120+100')
			self.root4['background']='black'
			self.root4.protocol('WM_DELETE_WINDOW',self.Root4Check)
			from Tkinter import Entry
			self.TextTmp1=Label(self.root4,text='Account:',foreground='red',background='black',font=self.font)
			self.TextTmp1.place(anchor=W,relx=0.04,rely=0.13)
			self.TextTmp2=Label(self.root4,text='Password:',foreground='red',background='black',font=self.font)
			self.TextTmp2.place(anchor=W,relx=0.04,rely=0.25)
			self.User_Root4=Entry(self.root4,width=30,foreground='red',background='black',font=self.font,insertbackground='white',relief='flat')
			self.User_Root4.place(anchor=W,relx=0.27,rely=0.13)
			self.Psd_Root4=Entry(self.root4,width=30,foreground='red',background='black',font=self.font,insertbackground='white',relief='flat',show='*')
			self.Psd_Root4.place(anchor=W,relx=0.27,rely=0.25)
			self.User_Root4.bind('<Key>',self.InputDeal_U)
			self.Psd_Root4.bind('<Key>',self.InputDeal_P)
			self.ShowResult=Label(self.root4,text='',background='black',foreground='red',font=self.font)
			self.ShowResult.place(anchor=CENTER,relx=0.5,rely=0.57)
			self.User_Root4.focus_set()
			self.root4.wm_attributes("-topmost", 1)
	def Root4Check(self):
		self.root4exist=False
		try:
			self.root4.destroy()
		except:
			pass
	def InputDeal_U(self,event):
		if self.Lock:
			self.ShowResult['text']=''
		if event.keycode==13 or event.keycode==40:
			self.Psd_Root4.focus_set()
	def InputDeal_P(self,event):
		if self.Lock:
			self.ShowResult['text']=''
		if event.keycode==13:
			Tmp_User=self.User_Root4.get()
			Tmp_Psd=self.Psd_Root4.get()
			if self.AccountCheck(Tmp_User,Tmp_Psd):
				self.AccountSuccess()
			else:
				self.User_Root4.delete(0,END)
				self.Psd_Root4.delete(0,END)
				self.ShowResult['text']='Account Error'
				self.User_Root4.focus_set()
		if event.keycode==38:
			self.User_Root4.focus_set()
	def FaceUnlock(self):
		self.ShowResult['foreground']='green'
		self.ShowResult['text']='Welcome Back,Sir'
		self.User_Root4.unbind('<Key>')
		self.Psd_Root4.unbind('<Key>')
		self.TextTmp1['text']=''
		self.User_Root4.delete(0,END)
		self.TextTmp2['text']=''
		self.Psd_Root4.delete(0,END)
		self.L1['foreground']='red'
		self.Lock=False
		self.root4.after(5000,self.ProgramEnd)
		self.AccountState=True
	def AccountCheck(self,User,Pass):
		if User==self.SafeAccount and Pass==self.SafePassword:
			return True
		if User in self.AccountList:
			if Pass==self.AccountList[User]:
				return True
		return False
	def AccountSuccess(self):
		self.User_Root4.unbind('<Key>')
		self.Psd_Root4.unbind('<Key>')
		self.ShowResult['foreground']='green'
		self.ShowResult['text']='Account Correct'
		# self.User_Root4['state']='disabled'
		self.TextTmp1['foreground']='green'
		self.User_Root4['foreground']='green'
		# self.Psd_Root4['state']='disabled'
		self.TextTmp2['foreground']='green'
		self.Psd_Root4['foreground']='green'
		self.L1['foreground']='red'
		self.Lock=False
		self.root4.after(5000,self.ProgramEnd)
		self.AccountState=True
	def ProgramEnd(self):
		self.root.destroy()
		try:
			self.root2.destroy()
		except:
			pass
		try:
			self.root3.destroy()
		except:
			pass
		try:
			self.root4.destroy()
		except:
			pass
		try:
			self.GetLink.End()
		except Exception,e:
			print e
	def CleanInput(self,word):
		tmp_word=word.replace(' ','')
		return tmp_word
	def Main(self):		
		self.BinCodeWindow()
		self.WarnningWindows()
		self.BeanWindows()
		# self.AccountWindows()
		self.root2.mainloop()
	def MainGUIExit(self):
		if not self.Lock:
			try:
				self.root.destroy()
			except:
				pass
			try:
				exit()
			except:
				pass
	class BeanDone():
		def __init__(self,Forwards):
			self.Step=0
			self.MaxS=self._GetMaxS()
		def __call__(self,Forwards):
			return self.Callback(Forwards)
		def _GetMaxS(self):
			return random.randint(50,280)
		def ExceptForwards(self,Forwards):
			F_List=['up','down','left','right']
			F_List.remove(Forwards)
			return F_List
		def Callback(self,Forwards):
			if self.Step>=self.MaxS:
				self.Step=0
				self.MaxS=self._GetMaxS()
				return random.choice(self.ExceptForwards(Forwards))
			else:
				self.Step+=1
				return Forwards
		def Collision(self,Forwards):
			self.Step=0
			self.MaxS=self._GetMaxS()
			return random.choice(self.ExceptForwards(Forwards))
	def BeanMove(self):
		if self.CurBeanForward=='left':
			if self.root3.winfo_x()<=0:
				self.CurBeanForward=self.BeanM.Collision('left')
			else:
				self._B_Move(-10,0)
				self.CurBeanForward=self.BeanM('left')
		elif self.CurBeanForward=='right':
			if self.root3.winfo_x()+self.root3.winfo_width()>=self.root3.winfo_screenwidth():
				self.CurBeanForward=self.BeanM.Collision('right')
			else:
				self._B_Move(10,0)
				self.CurBeanForward=self.BeanM('right')
		elif self.CurBeanForward=='up':
			if self.root3.winfo_y()<=0:
				self.CurBeanForward=self.BeanM.Collision('up')
			else:
				self._B_Move(0,-10)
				self.CurBeanForward=self.BeanM('up')
		elif self.CurBeanForward=='down':
			if self.root3.winfo_y()+self.root3.winfo_height()>=self.root3.winfo_screenheight():
				self.CurBeanForward=self.BeanM.Collision('down')
			else:
				self._B_Move(0,10)
				self.CurBeanForward=self.BeanM('down')
		if self.MouthStep>15:
			self.root3.wm_attributes("-topmost", 1)
			self.MouthStep=0
			self.MouthState=not self.MouthState
		else:
			self.MouthStep+=1
		self.BeanAction()
		self.root3.after(10,self.BeanMove)
	def _B_Move(self,PosX,PosY,Absolute=False):
		if Absolute:
			self.root3.geometry('80x80+'+str(PosX)+'+'+str(PosY))
			self.root3.update()
		else:
			self.root3.geometry('80x80+'+str(self.root3.winfo_x()+PosX)+'+'+str(self.root3.winfo_y()+PosY))
			self.root3.update()
	def BeanAction(self):
		if self.MouthState:
			self.cv_root3.delete('BeanMouth')
			self.cv_root3.create_arc((10,10,70,70),style = PIESLICE,start = self.BeanForwards()[1],extent = 3,fill = 'black',tag='BeanMouth')
		else:
			self.cv_root3.delete('BeanMouth')
			self.cv_root3.create_arc((10,10,70,70),style = PIESLICE,start = self.BeanForwards()[0],extent = 60,fill = 'black',tag='BeanMouth')
	def BeanForwards(self):
		if self.CurBeanForward=='left':
			return (150,179)
		elif self.CurBeanForward=='right':
			return (330,359)
		elif self.CurBeanForward=='up':
			return (60,89)
		elif self.CurBeanForward=='down':
			return (240,269)
		else:
			raise
	def WarnningSpark(self):
		if not self.AccountState:
			self.root2.wm_attributes("-topmost", 1)
			self.SparkState = not self.SparkState
			if self.SparkState:
				self.root2['background']='red'
				self.WarnningText['background']='red'
				self.WarnningText['foreground']='yellow'
			else:
				self.root2['background']='black'
				self.WarnningText['background']='black'
				self.WarnningText['foreground']='red'
			self.root2.after(500,self.WarnningSpark)
		else:
			self.root2['background']='green'
			self.WarnningText['background']='green'
			self.WarnningText['foreground']='white'
			self.WarnningText['text']='Account Pass'
		
	def _ReturnRandomCode(self,aLen):
		aString=''
		c=['0','1']
		for x in range(aLen):
			aString+=random.choice(c)
		aString+='\n'
		return aString
	def RunCode(self):
		self.CurCodeStream.insert(0,self._ReturnRandomCode(int(self.root.winfo_screenwidth()/6)-1))
		if len(self.CurCodeStream)>int(self.root.winfo_screenheight()/15):
			self.CurCodeStream.pop(-1)
		tmp_string=''
		for i in self.CurCodeStream:
			tmp_string+=i
		self.L1['text']=tmp_string
		self.root.after(60,self.RunCode)


def _async_raise(tid, exctype):
	"""raises the exception, performs cleanup if needed"""
	tid = ctypes.c_long(tid)
	if not inspect.isclass(exctype):
		exctype = type(exctype)
	res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
	if res == 0:
		raise ValueError("invalid thread id")
	elif res != 1:
		# """if it returns a number greater than one, you're in trouble,
		# and you should call it again with exc=NULL to revert the effect"""
		ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
		raise SystemError("PyThreadState_SetAsyncExc failed")
def stop_thread(thread):
	_async_raise(thread.ident, SystemExit)


aCode=CodeStream()
aCode()
