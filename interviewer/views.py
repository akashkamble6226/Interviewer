from os import remove
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from nltk.util import pr
from numpy.lib.function_base import append
from .models import InterviewData
from django.contrib import messages 
import json as simplejson


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
                    InterviewData.objects.filter(id=q.id).update(marks_in_perc = 0)
                    InterviewData.objects.filter(id=q.id).update(accuracy_eighty_words = [])
                    InterviewData.objects.filter(id=q.id).update(accuracy_zero_words = [])
                    InterviewData.objects.filter(id=q.id).update(accuracy_hundred_words = [])



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

            new_question = InterviewData(questions = question, answers = processed_predefined_ans, index_no = index, accuracy_hundred = [], accuracy_eighty=[], marks_in_perc=0, accuracy_eighty_words=[],accuracy_hundred_words=[],accuracy_zero_words=[] )
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
        audio = r.record(source,duration = 8)

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
    word_0_acc = []
    word_80_acc = []
    word_100_acc = []


    ex1 = nlp(question.given_answer)
    ex2 = nlp(question.answers)
    for token1 in ex1:
        for token2 in ex2:    
            if(token1.similarity(token2) == 1.0):
                if(token1.text != " "):
                    lst1.append(token1.text)
                    word_100_acc.append(token1.text)

                
            elif(token1.similarity(token2) >= 0.50 and token1.similarity(token2) < 1.0):
                if(token1.text != " "):
                    lst2.append(token1.text)
                    word_80_acc.append(token1.text)
            
            else:
                if(token1.text != " "):
                    word_0_acc.append(token1.text)

               
            

    # finally sending for updating the accuracy
                
    update_accuracy(question.id,True,lst1)
    update_accuracy(question.id,False,lst2)
    update_all_words(question.id,word_0_acc,word_80_acc,word_100_acc)


def update_all_words(id, zero, eighty, hundred):
    Questions = InterviewData.objects.all()
    question =  Questions.get(id=id)

    # just removing duplicate items
    seen = set()
    result_0= []
    for item in zero:
       if item not in eighty:
           if item not in hundred:
               if item not in question.answers:
                   seen.add(item)
                   result_0.append(item)

    InterviewData.objects.filter(id=question.id).update(accuracy_zero_words =result_0,accuracy_eighty_words=eighty,accuracy_hundred_words =hundred)



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

# comming to this function when a submit button is clicked 
def isAnsGiven(request, id):
    
    Questions = InterviewData.objects.all()
    question =  Questions.get(id=id)
    ansLen = len(question.given_answer)
    if(ansLen == 0 or question.given_answer == " "):
        messages.warning(request,"Please answer the question first before submitting.")
    else:

        calculate_percentage(id)
        
        messages.success(request,"Answer submitted successfully")
    return render(request, 'mainpage.html', {'Questions': Questions})


def calculate_percentage(id):
    Questions = InterviewData.objects.all()
    question =  Questions.get(id=id)
    # checking the word count from the stored ans  
    stored_ans_cnt = question.answers.split()

    combined_accuracy_list = []

    for a in question.accuracy_hundred:
        if a != " ":
            combined_accuracy_list.append(a)
    for b in question.accuracy_eighty:
        if b != " ":
            combined_accuracy_list.append(b)

    marks_for_question = 0

    for acc in combined_accuracy_list:
        if(acc == 0.80 or acc == 0.8):
            marks_for_question+= 80
        else:
            marks_for_question+= 100

    
    # below line is becuase we dont know how many line of answer we store it is variabel(changabel)
    out_of =  len(stored_ans_cnt) * 100
    quotient = (marks_for_question) / (out_of)

    marks_perc = quotient * 100
    # finally returning percentage value to calling function to store into databse 
    InterviewData.objects.filter(id=id).update(marks_in_perc=marks_perc)


def showReport(request):
    Questions = InterviewData.objects.all()
    Questions_cnt = InterviewData.objects.count()

    print(Questions_cnt)
    answerdQuestionsCount = 0
    answerdQuestions = []
    finalScore = 0
    for q in Questions:
        if(len(q.given_answer) != 0 and q.given_answer != " "):
            answerdQuestions.append(q)
            answerdQuestionsCount = answerdQuestionsCount + 1
            finalScore+= q.marks_in_perc
    print(answerdQuestionsCount)
    
    if(answerdQuestionsCount!= 0 and Questions_cnt != 0 and answerdQuestionsCount == Questions_cnt):
        out_of = 100 * Questions_cnt
        quotient = finalScore / out_of
        final_score_perc = quotient * 100

        
        print(final_score_perc)
        return render(request, 'myReport.html', {'answerdQuestions':answerdQuestions, 'final_score_perc':final_score_perc})

    # at least one question should be answerd
    if(answerdQuestionsCount >= 1):
        # i have answerd all the questions
        return render(request, 'myReport.html', {'answerdQuestions':answerdQuestions,'finalScore':finalScore})
    else:
        # I dident 
        messages.warning(request,"Please answer at least one questions to generate report.")
        return render(request, 'myReport.html')

    

# def calculate_final_score(Questions_cnt):
#     Questions = InterviewData.objects.all()
#     all_ques_per = 0
#     for q in Questions_cnt:
#         all_ques_per += Questions[q].marks_in_perc
    
#     return all_ques_per

    

def showAnaysis(request):
    labels, data = showBarChart()
    label_list = simplejson.dumps(labels)
    data_list =  simplejson.dumps(data)
    print(len(labels))
    print(len(data))
    if(len(labels) == 0 or len(data) ==0):
        messages.warning(request,"Please answer at least one questions to analys your performance.")

    return render(request, 'analysis.html',{'label_list':label_list, 'data_list':data_list})

def showBarChart():
   Questions = InterviewData.objects.all()
   
   labels = []

   s = 1
   for q in Questions:
       if(q.marks_in_perc != 0):
           labels.append('Question No '+ str(s))
           s = s + 1
 

   data = []
   index = 1
   for q in Questions:
       if(q.marks_in_perc != 0):
           accuracy = q.marks_in_perc
           data.append(accuracy)
           index += 1  
    
   return labels, data


           
   
   

    

   