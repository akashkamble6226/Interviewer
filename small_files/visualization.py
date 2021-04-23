import pylab as plt




def visualize(dataList):
    
    frequencyOfWord = []

    wordFreq1 = 1.0
    for b in dataList:
        frequencyOfWord.append(wordFreq1)

   

    numberOfWords = []

    cnt = 0
    for a in dataList:
        cnt = cnt + 1
        numberOfWords.append(cnt)
    
    

    LABELS = []

    for w in dataList:
        LABELS.append(w)
    
    
  
    fig = plt.figure()
    fig.suptitle('Analysis Of The INTRUE')
    
    plt.xlabel("Words")
    plt.ylabel("Frequenncy Of Words")
    plt.bar(numberOfWords, frequencyOfWord, align='center')
    plt.xticks(numberOfWords, LABELS)
    plt.show()


def visualize2(dataList,dataList2):
    
    frequencyOfWord = []

    wordFreq1 = 1.0
    for b in dataList:
        frequencyOfWord.append(wordFreq1)
    
    wordFreq0 = 0.8
    for c in dataList2:
        frequencyOfWord.append(wordFreq0)

   

    numberOfWords = []

    cnt = 0
    for a in dataList:
        cnt = cnt + 1
        numberOfWords.append(cnt)
    
    for s in dataList2:
        cnt = cnt + 1
        numberOfWords.append(cnt)
    
    

    LABELS = []

    for w in dataList:
        LABELS.append(w)
    
    for q in dataList2:
        LABELS.append(q)

    
    
  
    fig = plt.figure()
    fig.suptitle('Analysis Of The INTRUE')
    
    plt.xlabel("Words")
    plt.ylabel("Frequenncy Of Words")
    plt.bar(numberOfWords, frequencyOfWord, align='center')
    plt.xticks(numberOfWords, LABELS)
    plt.show()

