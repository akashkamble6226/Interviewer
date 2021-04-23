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
                print(processed_predefined_ans)
                
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

    # deleting preious answer 
    
    InterviewData.objects.filter(id=question.id).update(accuracy_hundred = [])
    InterviewData.objects.filter(id=question.id).update(accuracy_eighty = [])

    nlp = spacy.load("en_core_web_md")
            
    r = sr.Recognizer()

    lst1 = []
    lst2 = []


    with sr.Microphone() as source:
        audio = r.listen(source,timeout=1)

        try:
            givenAns = r.recognize_google(audio)

            ProcessedAnsList = doPreprocessingOfText(givenAns)

            #storing answer to givenAnswer txt file

            Given_ans = " "

            for item in ProcessedAnsList:
                Given_ans = Given_ans + item + " "
                   
                store_users_given_answer(question.id,Given_ans)


                ex1 = nlp(question.given_answer)
                ex2 = nlp(question.answers)

                # inserting words which are commen as per given condition 
                for token1 in ex1:
                    for token2 in ex2:
                        if(token1.similarity(token2) == 1.0):
                            if(len(token1) != 0 and len(token2) != 0):
                                
                                lst1.append(token1.text)
   
                            elif(token1.similarity(token2) >= 0.80):
                                
                                lst2.append(token1.text)
    
                # removing unwanted first element which is space
                if(len(lst1) >= 1):
                    {
                        lst1.pop(0)

                    }
                       
        except:
                #or i can simply speak the message
                messages.info(request,"Sorry could not listen your voice.")
                    
       
        update_accuracy(question.id,True,lst1)
        update_accuracy(question.id,False,lst2)
     

        # print(len(lst1))
        # print(len(lst2))

        

        # InterviewData.objects.filter(id=question.id).update(accuracy_hundred = lst1)
        # InterviewData.objects.filter(id=question.id).update(accuracy_eighty = lst2)






        # if(len(lst1) == 0):
        #     messages.info(request,"Sorry could not listen your voice.")
        #     print("Say Something please.......")
                
       

        # if(len(lst2) == 0):
        #     {
            # visualize(lst1)
        #     }

        # else:
        #     {
        #     visualize2(lst1,lst2)
        # }
    return render(request, 'mainpage.html', {'Questions': Questions})
    



def update_accuracy(questionId, isHundered, accuracyTypeList):
    Questions = InterviewData.objects.all()
    question =  Questions.get(id=questionId)
    if(isHundered):
        if(len(accuracyTypeList) != 0):
            
            frequencyOfWord = []
            wordFreq1 = 1.0
            
            for b in accuracyTypeList:  
                frequencyOfWord.append(wordFreq1)
            InterviewData.objects.filter(id=question.id).update(accuracy_hundred = frequencyOfWord)
            frequencyOfWord.clear()
            # //below clearing the previus score from that field


    else:
        if(len(accuracyTypeList) != 0):
            
            frequencyOfWord2 = []
            wordFreq2 = 0.8
            
            for b in accuracyTypeList:
                print(b)
                frequencyOfWord2.append(wordFreq2)
            InterviewData.objects.filter(id=question.id).update(accuracy_eighty = frequencyOfWord2)
            frequencyOfWord2.clear()
