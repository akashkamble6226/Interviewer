from os import remove
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from .models import InterviewData
from django.contrib import messages 


# Create your views here.

import pyttsx3
# text simmilarity
import spacy
import speech_recognition as sr
from small_files.preprocessing_of_file import doPreprocessing,doPreprocessingOfText
from small_files.visualization import visualize,visualize2
# below line is for avoiding error on reload
from django.views.decorators.csrf import csrf_exempt


# ----- login , register, logout .-------
@csrf_exempt
def login(request):
    Questions = InterviewData.objects.all()



    if request.method == 'POST':
        username = request.POST['phone'];
        password = request.POST['pass'];

        


        if(len(username) != 0 or len(password) != 0 ):
            user = auth.authenticate(username=username,password=password);
            if user is not None:
                auth.login(request, user)
                messages.success(request,"Welcome")

                for q in Questions:
                    # clearing the accuracy columns
                    InterviewData.objects.filter(id=q.id).update(accuracy_hundred = [])
                    InterviewData.objects.filter(id=q.id).update(accuracy_eighty = [])
                    # clearing the previus given ans 
                    InterviewData.objects.filter(id=q.id).update(given_answer = " ")



                return render(request, 'mainpage.html', {'Questions': Questions})
            else:
                messages.error(request,"User doesen'\t exists.")
                return render(request, 'login.html')
        else:
            messages.warning(request,"Fields cannot be empty.")
            return redirect('login')

    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['f_name']
        phone = request.POST['phone']
       
        password = request.POST['pass']
        con_pass = request.POST['c_pass']

        if (len(first_name) != 0 or len(phone) != 0 or len(password) != 0 or len(con_pass) != 0):
            if(password == con_pass):
                if(User.objects.filter(username=phone).exists()):
                    messages.info(request,"Phone already used.")
                    return redirect('register')
                else:
                    user = User.objects.create_user(username = phone, first_name=first_name,password=password)
                    user.save()
                    messages.success(request,"User Created Successfully !")
                    # print('User created successfully')
                    return redirect('login')
            else:
                messages.info(request,"Password and confirm password should be same.")
                # print("Password and confirm password should be same")
                return redirect('register')
        else:
            messages.warning(request,"Fields cannot be empty.")
            # print("Password and confirm password should be same")
            return redirect('register')

    else:
        return render(request, 'register.html')


    
def logout(request):
    auth.logout(request)
    messages.success(request,"Logout Successfull")
    return redirect("login")


def mainpage(request):
    Questions = InterviewData.objects.all()
    return render(request, 'mainpage.html', {'Questions': Questions})

    


# ----- admin question adding -------


def adminPanel(request):
    return render(request, 'adminPanel.html')



def addQuestion(request):
    if(request.method == "POST"):
        question = request.POST['q_name']
        answer = request.POST['q_answer']
        if(len(question) == 0 or len(answer) == 0 ):

            
            messages.error(request,"Fields cannot be empty.")
            return redirect("addQuestion")
            
        else:
            individual_items_list = doPreprocessing(answer)

            processed_predefined_ans = " "
            for item in individual_items_list:
                processed_predefined_ans = processed_predefined_ans + item + " "
               
                
            index = InterviewData.objects.count() + 1

            new_question = InterviewData(questions = question, answers = processed_predefined_ans, index_no = index, accuracy_hundred = [], accuracy_eighty=[]  )
            new_question.save()
            messages.success(request,"Question added successfully!")
            return redirect("adminPanel")

    else:
        return render(request, 'addQuestions.html')


def showQuestions(request):
    question = InterviewData.objects.all()
    # cnt = InterviewData.objects.count();
    # print(cnt)
    return render(request, 'allQuestions.html', {'question':question})


def edit_question(request, id):
   
    question = InterviewData.objects.get(id=id)
    
    return render(request, 'editQuestion.html', {'question': question})

            
def update_question(request,id):
    if(request.method == "POST"):
        question = request.POST['q_name']
        answer = request.POST['q_answer']
        if(len(question) != 0 or len(answer) != 0):
            InterviewData.objects.filter(id=id).update(questions=question,answers=answer)
            messages.success(request,"Question updated successfully!")
               
            return redirect("showQuestions")
        else:
            messages.error(request,"Fields cannot be empty.")
            return redirect("update_question")
    else:

        return render(request, 'editQuestion.html', {'question':question})

def store_users_given_answer(id,givenAnswer):
    InterviewData.objects.filter(id=id).update(given_answer=givenAnswer) 
    
    # return redirect("showQuestions")
    
    
def delete_question(request, id):
    question = InterviewData.objects.get(id=id)
    question.delete()
    messages.success(request,'Question deleted Successsfully')
    return redirect('showQuestions')
            

# below is main logic of answer checking 
# asking question 

def askQuestion(request, id):

    Questions = InterviewData.objects.all()
    question =  Questions.get(id=id)

    engine = pyttsx3.init()
    engine.say(question.questions)
    engine.runAndWait()
    engine.startLoop(False) 
    engine.endLoop()
    engine.stop()
    return render(request, 'mainpage.html', {'Questions': Questions})
    
def giveAnswer(request, id):

    Questions = InterviewData.objects.all()
    question  =  Questions.get(id=id)

    # deleting preious answer if any available
    InterviewData.objects.filter(id=question.id).update(accuracy_hundred = [])
    InterviewData.objects.filter(id=question.id).update(accuracy_eighty = [])

   
            
    r = sr.Recognizer()
    Given_ans = " "


    with sr.Microphone() as source:
        audio = r.record(source,duration = 5)

        try:
            givenAns = r.recognize_google(audio)

            ProcessedAnsList = doPreprocessingOfText(givenAns)

            for item in ProcessedAnsList:
                Given_ans = Given_ans + item + " "
            
            # storing users given answer into database
            store_users_given_answer(question.id,Given_ans)
 
        except:
                messages.info(request,"Sorry could not listen your voice.")
        
    #preparing for updating accuracy
    prpare_for_updating_accuracy(question.id)
    return render(request, 'mainpage.html', {'Questions': Questions})

def prpare_for_updating_accuracy(questionId):
    Questions = InterviewData.objects.all()
    question =  Questions.get(id=questionId)

    nlp = spacy.load("en_core_web_md")
    
    lst1 = []
    lst2 = []
    

    ex1 = nlp(question.given_answer)
    ex2 = nlp(question.answers)
    for token1 in ex1:
        for token2 in ex2:    
            if(token1.similarity(token2) == 1.0):
                lst1.append(token1.text)
            if(token1.similarity(token2) >= 0.80 and token1.similarity(token2) < 1.0):
                lst2.append(token1.text)
            

    # finally sending for updating the accuracy
                
    update_accuracy(question.id,True,lst1)
    update_accuracy(question.id,False,lst2)


def update_accuracy(questionId, isHundered, accuracyTypeList):
    print(len(accuracyTypeList))
    Questions = InterviewData.objects.all()
    question =  Questions.get(id=questionId)
    if(isHundered):
        if(len(accuracyTypeList) >= 1):
            
            frequencyOfWord = []
            
            wordFreq1 = 1.0

            # removing the duplicates if any 
            
            accuracyTypeList = list(set(accuracyTypeList))
            for b in accuracyTypeList:
                if(b != " "):
                    frequencyOfWord.append(wordFreq1)
           
            if(len(question.accuracy_hundred) != 0):  
                question.accuracy_hundred.clear()
                InterviewData.objects.filter(id=question.id).update(accuracy_hundred = frequencyOfWord)        
         
            else:
                InterviewData.objects.filter(id=question.id).update(accuracy_hundred = frequencyOfWord)
  
            frequencyOfWord.clear()
           # //below clearing the previus score from that field
        else:
            print("accuracy 100 list is empty")

    else:
        if(len(accuracyTypeList) != 0):
            frequencyOfWord2 = []
            wordFreq2 = 0.8
            for b in accuracyTypeList:
                if(b!=" "):
                    frequencyOfWord2.append(wordFreq2)
            InterviewData.objects.filter(id=questionId).update(accuracy_eighty = frequencyOfWord2)
            frequencyOfWord2.clear()
        else:
            print("accuracy 80 list is empty")


def isAnsGiven(request, id):
    
    Questions = InterviewData.objects.all()
    question =  Questions.get(id=id)
    ansLen = len(question.given_answer)
    if(ansLen == 0 or question.given_answer == " "):
        messages.warning(request,"Please answer the question first before submitting.")
    else:
        messages.success(request,"Answer submitted successfully")
    return render(request, 'mainpage.html', {'Questions': Questions})





def showReport(request):
    Questions = InterviewData.objects.all()
    Questions_cnt = InterviewData.objects.count()

    answerdQuestions = 0
    for q in Questions:
        if(len(q.given_answer) != 0 and q.given_answer != " "):
            answerdQuestions = answerdQuestions + 1
    
    print(answerdQuestions)
    print(Questions_cnt)
    
    if(answerdQuestions == Questions_cnt):
        # i have answerd all the questions
        return render(request, 'myReport.html', {'Questions': Questions})
    else:
        # I dident 
        messages.warning(request,"Please answer all the questions to generate report.")
        return render(request, 'myReport.html')

    



