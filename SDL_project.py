'''Quiz Maker - Make an application which takes various questions from a file, picked randomly, and puts together a quiz for students. 
Each quiz can be different and then reads a key to grade the quizzes.
noqif (int) - No of questions in Quiz_que
noqiq (int) -No of questions in quiz
qu_li (list) -List of question numbers
'''
#things to add:
#1] skip question functionality
#2] send score of contestant to our mail
#3] display timer on terminal
#--------------------------------------------------------------------------
##Notes:
##use printout(string,color) to display colourful output [color:- RED,GREEN,BLUE,etc]
##Install at for timer on ubuntu
#-----------------------------------------------Imports---------------------------------------
from termios import tcflush, TCIFLUSH
import signal
import sys
import os
from time import sleep
from random import randint
import smtplib
from email.mime.multipart import MIMEMultipart	#for sending more described mail
from email.mime.text import MIMEText		#for sending more described mail
#------------------------------------Global variable declaration-----------------------
noqif=15			#Enter no in Quiz_que file here
noqiq=5		#Enter no of que you wanna ask here [noqiq must be less than noqif]
qu_li=[]
an_li=[]
for i in range(0,noqiq):
	an_li.append('S')
#---------------------------------------------------------
t_que=0		#no of technical Que	->varies Branchwise
nt_que=0	#no of non technical Que ->varies Branchwise
#---------------------------------------------------------Note e_que+m_que+d_que must be equal to noqiq
	# Also e_que< C___E and N___E and m_que< C___M and N___M and d_que< C___D and N___D for crash free result
e_que=2		#no of easy Que	->constant
m_que=2		#no of medium que ->constant
d_que=1		#no of difficult que ->constant
#-------------------------------------------------------------
p_id=0
email=""
branch=""
#-------------------------------FUnction for displaying colourful output------------------------------------
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
#following from Python cookbook, #475186
def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)
def printout(text, colour=WHITE):
        if has_colours:
                seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
                sys.stdout.write(seq)
        else:
                sys.stdout.write(text)
#--------------------------------------------Check Function--------------------------------------
def check():
	c_an_li=[]
	f=open("Quiz_ans")
	for i in qu_li:
		f.seek(0)
		for line in f:
			if int(line[:3])==i:
				c_an_li.append(line[4:5].upper())
	score=0
	print("\t+---------------+")
	for i in range(0,len(an_li)):
		if an_li[i]==c_an_li[i]:
			print("\t| ",i+1,"] Correct\t|")
			score=score+1
		elif an_li[i]=='S':
			print("\t| ",i+1,"] NA\t|")
		else:
			print("\t| ",i+1,"] Wrong\t|")
	print("\t+---------------+")
	print("\nYour Score is :::: ",score)
	if score>0:
		print("\nCongratulations!!!!")
	else:
		print("\nDont participate in such events again")
	f.close()
	return score
#--------------------------------------------sendMail Function-----------------------------------
def sendMail(sender_id,receiver_id,email_body,sub):
	fromaddr = sender_id
	toaddr = receiver_id
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = sub
	body = email_body	#Enter message body here 
	msg.attach(MIMEText(body, 'plain'))
	# creates SMTP session
	server = smtplib.SMTP('smtp.gmail.com', 587)
	# start TLS for security
	server.starttls()
	# Authentication
	server.login("anantya2k17.quizophile@gmail.com","8124##strong")
	text = msg.as_string()
	# sending the mail
	server.sendmail(fromaddr, toaddr, text)
	# terminating the session
	server.quit()
#----------------------------------------GenerateSolution Function---------------------------------
def GenerateSolution():
	f=open("Quiz_que")
	str=" "
	sol=" "
	for qn in qu_li:			#questions inside sets
		f.seek(0)
		for line in f:
			if int(line[1:4])==qn :
				str=str+line+"\n"		#prints question
				for line in f:
					if line[:3]=="___":
						str=str+line+"\n"
						break
					else:
						str=str+line+"\n"
			else:	
				for line in f:
					if line[:3]=="___":
						break
	f.close()			
	return str	
#--------------------------------------EndofQuiz----------------------------
def end_of_quiz():
	os.system('clear')
	print("\n<><><><><><><><><><> END OF QUIZ  <><><><><><><><><><>\n\n")
	j=0
	for i in range(0,noqiq):
		if an_li[i]=='S':
			j=j+1
	if j>0:
		print(j,'Questions are not attempted')
	while True:
		print("\n\n\n\t\t\t0-> Edit Responses")
		print("\n\n\t\t\t1-> Submit Test")
		res=input("\n\n\t\t\tEnter Choise :");
		if res=='0':
			quiz()		#add functionality here
		elif res=='1':
			dec=input("\n\t\t\tAre You sure (yes/no) : ")
			dec=dec.upper()
			if dec=='YES':
				postQuiz()
		else:
			print('bad choise')
#-------------------------------------------------------------------------------
def timeout_end_of_quiz():
	signal.alarm(0)
	os.system('clear')
	#print("\n<><><><><><><><><><> END OF QUIZ  <><><><><><><><><><>\n\n")
	print("\n\n\n\nSubmittiong your Test....")
	sleep(3)
	postQuiz()
#--------------------------------------------------------------------------------------------
def signal_handler(signum, frame):
    raise Exception("Timed out!")
#------------------------------------------------------------------------
def create_quiz():
	global branch
	global qu_li
	global an_li
	branch=branch.upper()
	if branch[:2]=='CS'or branch[:1]=='IT' or branch[:1]=='EC':
		t_que=3			#This should be less than no of que tagged as C in file
		nt_que=2		#This should be less than no of que tagged as N in file
	else:
		t_que=0
		nt_que=5
	f=open('Quiz_que')
	count=0;
	t_count=0
	nt_count=0
	e_count=0
	m_count=0
	d_count=0
	while t_count!=t_que or nt_count!=nt_que:	#terminates when  t_count==t_que and nt_count==nt_que
		f.seek(0)			#set file pointer to begining of file
		qn=randint(1,noqif)
		#print(qn)#testing
		flag=1
		for j in qu_li:	
			if j==qn:		#This means that que is already taken
				flag=0
		if flag==1:
			for line in f:
				#print(line[:5])#testing
				if line[0]=='C' and int(line[1:4])==qn:
					if t_count<t_que:
						if line[4]=='E':
							if e_count<e_que:
								e_count=e_count+1
								t_count=t_count+1
								qu_li.append(qn)
								break
						elif line[4]=='M':
							if m_count<m_que:
								m_count=m_count+1
								t_count=t_count+1
								qu_li.append(qn)
								break
						elif line[4]=='D':
							if d_count<d_que:
								d_count=d_count+1
								t_count=t_count+1
								qu_li.append(qn)
								break
				elif line[0]=='N' and int(line[1:4])==qn:
					if nt_count<nt_que:
						if line[4]=='E':
							if e_count<e_que:
								e_count=e_count+1
								nt_count=nt_count+1
								qu_li.append(qn)
								break
						elif line[4]=='M':
							if m_count<m_que:
								m_count=m_count+1
								nt_count=nt_count+1
								qu_li.append(qn)
								break
						elif line[4]=='D':
							if d_count<d_que:
								d_count=d_count+1
								nt_count=nt_count+1
								qu_li.append(qn)
								break
				for line in f:
					if line[:3]=="___":
						break
	f.close()

def quiz():
	os.system('clear')
	f=open('Quiz_que')
	#print(qu_li)#testing
	#print(len(qu_li))#testing
	#print(type(qu_li[0]))#testing
	#print(type(qu_li[1]))#testing
	#print(type(qu_li[2]))#testing
	#print(type(qu_li[3]))#testing
	i=0
	while i <noqiq:
		f.seek(0)			#set file pointer to begining of file
		flag=1
		bit=0
		for line in f:
				#print(line[1:4])#testing
				if int(line[1:4])==qu_li[i] :
					#print('in if')#testing
					#print(line[1:4])#testing
					flag=0
					os.system('clear')
					print("<><><><><><><><><><> QUIZ CONSOLE <><><><><><><><><><>\n\n")
					print(i+1,"]",line[6:])		#prints question
					for line in f:
						if line[:3]=="---":
							break
						else:
							print(line)
					for line in f:				#prints options
						if line[0:3]=="---":
							if an_li[i]=='S':
								printout("Status : Not Attempted ",YELLOW)
							else:
								printout("Status : Attempted [",YELLOW)
								printout(an_li[i],YELLOW);
								printout("]",YELLOW);
							print()
							printout("Enter S/s to skip this Question",GREEN) 
							break
						else:
							print(line)
					for line in f:				#skips explanation
						if line[0:3]=="___":
							break
					while True:
						an=input("\nEnter Your Answer : ")
						an=an.upper() 		#convert to uppercase
						if an>="A" and an<="D":
							lock=input("Submit (y/n) : ")
							if lock=='y':				 
								print("\nSaving your response ...\n")
								sleep(1)
								an_li[i]=an
								i=i+1
								break
							else:
								continue
						elif an=="S":
							bit=1
							while True:
								print("\n\t\t\t1->previous que")
								print("\t\t\t2->stay on same que")
								print("\t\t\t3->next que")
								print("\t\t\t4->Display all questions")
								print("\t\t\t5->SUBMIT QUIZ")
								choise=input('\n\n\t\t\tEnter your Choise :')
								if choise=='1':
									if i==0:
										os.system('clear')
										print('\n\n\n\n\t\t\tthis is First Question')
										sleep(1)
									else:
										i=i-1
									break
								elif choise=='2':
									break
								elif choise=='3':
									if i==noqiq-1:
										os.system('clear')
										print('\n\n\n\n\t\t\tthis is Last Question')
										sleep(1)
									else:
										i=i+1
									break
								elif choise=='4':
									print()
									for j in range(0,noqiq):
										if an_li[j]=='S':
											print("\t\t\t",j+1,"\t->","Not Answered")
										else:
											print("\t\t\t",j+1,"\t->",an_li[j])
									j=input("\n\t\t\tJump to Question No : ")
									if j>'0' and j<=str(noqiq):
										i=int(j)-1
									else:
										printout("Question number is Out of Range",RED)
										print()
										sleep(1)
									#some action  here
									break
								elif choise=='5':
									end_of_quiz()
								else:
									print("\n\t\t\t")
									printout("Bad choise Try Again",RED);
									continue
						else :
							printout("Bad choise Try Again",RED);
						if bit==1:
							break
				else:
					#print('in else')#testing
					#print(line[1:4])#testing
					for line in f:
						if line[:3]=="___":
							break	
				if flag==0:
					break
	f.close()
#-------------------------------------------------------------------------------------
def postQuiz():
	signal.alarm(0)
	#print(qu_li)#testing
	#print(an_li)#testing
	os.system('clear')
	print("\t\t\t",end="")	
	printout("Score Card",GREEN)
	print("\n\nPreparing Your Score Card.........\n\n") 
	sleep(2)
	score=check()
	sleep(10)
	os.system('clear')
	print("\t\t\t",end="")	
	printout("Final Steps",GREEN)
	print("\n\nplease wait......")
	tcflush(sys.stdin, TCIFLUSH)
	sendMail(email,"anantya2k17.quizophile@gmail.com",p_id+" | "+str(score)+" | "+email,"ScoreCard") 
										#send score of contestant to our mail
	print("\n\n\t\t\t",end="")	
	printout("Your Score is succesfully submitted ",MAGENTA)
	email_body=GenerateSolution()
	print("\nOne step more......")
	tcflush(sys.stdin, TCIFLUSH)			#imp
	sendMail("anantya2k17.quizophile@gmail.com",email,email_body,"Solution Of Questions that you solved in Quiz-O-phile Round 1")
									#send solutions to contestant from our mail
	print("\n\n\t\t\t",end="")	
	printout("Answer Key is sent to "+email,MAGENTA)
	print("\n\n\nThank you for your participation , You are great player !!! ")
	print("Have a nice Day")
	print("\n\n\n\n<><><><><><><><><><> END OF QUIZ <><><><><><><><><><>\n\n\n\n")

while True:
	os.system('clear')
	print("\n\n\n\t\t\t",end="")
	printout('+----------------------+',RED)
	print("\n\t\t\t\t",end="")
	printout('Quiz-o-Phile',YELLOW)
	print("\n\t\t\t",end="")
	printout('+----------------------+',RED)
	print("\n\n\n\t\t\t",end="")
	printout('Enter Details',GREEN)
	print("\n\n\t\t\t",end="")
	printout('Participant Id :',BLUE)
	p_id=input()			#
	while True:
		print("\n\t\t\t",end="")
		printout('Email id : ',BLUE)
		email1=input()
		print("\n\t\t\t",end="")
		printout('Confirm Email id : ',BLUE)
		email2=input()
		if email1==email2:
			email=email1		#
			break
		else:
			print("\n\t\t\t",end="")
			printout('Id doesnt match.',RED)
			print("\n\t\t\t",end="")
			printout('Enter Again',RED)
	print("\n\t\t\t",end="")
	printout('Branch : ',BLUE)
	branch=input()			#
	print("\n\n\t\t",end="")
	name=email.split('@')
	printout('Welcome '+str(name[0])+' Are you Ready??(y/n) : ',GREEN)
	yn=input()
	if yn=='y' or yn=='Y':
		break
	else:
		print("\n\t\t\t",end="")
		printout('You seem nervous...',YELLOW)
os.system('clear')
print('\n\n\n\t\t\t',end="")
printout('  Breathe in Breathe out',YELLOW)
print('\n\n\t\t\t  Creating Quiz For You\n\n\n')
for i in range(21):			#code to display progressbar
    sys.stdout.write('\r')
    sys.stdout.write("\t\t\t[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)

#--------------------------------------------------------------------------------

create_quiz()
#quiz()
#end_of_quiz()

#---------------------------Logic for Limited Time----------------------------	
signal.signal(signal.SIGALRM, signal_handler)
signal.alarm(20)   # Enter Desired Time
try:
    	quiz()
except Exception:
	print("\n\n\n")
	printout("Timed out!",RED)
	timeout_end_of_quiz()
else:
	end_of_quiz()
#------------------------------Finishing Quiz----------------------------------
#quiz()
#postQuiz()
