process=""
brust=0
arrive=0
Wt=[]
Rt=[]
Ct=[]
tat=[]
procesos=[]
procesosdes=[]
reloj=0
dif=0
temporg=0
temppro=[]
#promedios
prowt=0
prort=0
proct=0
protat=0




def abrirarchivo():
    
    with open("procesos.txt") as file:
        global procesos
        global procesosdes
        global process
        global brust
        global arrive

        next(file)
        for linea in file:
            parts = linea.strip().split()
            process = parts [0]
            arrive = int(parts[1])
            brust = int(parts[2])
            procesosdes.append([process, arrive, brust])

    global temporg
    global temppro
        
    procesosdes.sort(key=lambda x: (x[1], x[0]))
    procesos.append(procesosdes[0])
    procesosdes= procesosdes[1:]
    procesosdes.sort(key=lambda x: (x[2], x[0]))
    temporg=procesos[0][2]


    while len(procesos) < len(procesosdes)+1:
        for i in range(len(procesosdes)):     
            if procesosdes[i] is not None and procesosdes[i][1]<=temporg:
                temppro.append(procesosdes[i])

        if temppro:
            temppro.sort(key=lambda x: (x[2], x[0]))
            procesos.append(temppro[0])

        temporg+=temppro[0][2]
        for i in range (len(procesosdes)):
            if procesosdes[i] is not None and procesosdes[i][0]==temppro[0][0]:
                procesosdes[i]=None
        temppro=[]
 


def reloj_WT():
    global reloj
    
    temp=0
    
    for i in range(len(procesos)-1):
        Wt.append(temp-procesos[i][1])
        Ct.append(temp+procesos[i][2])
        Rt.append(temp) 
        temp+=procesos[i][2]
        if procesos[i+1][1]>temp:
            dif=procesos[i+1][1]-procesos[i][2]
            temp+=dif       
        #print(temp)
    #añado el ultimo dato    
    Wt.append(temp-procesos[-1][1])
    Ct.append(temp+procesos[-1][2])
    Rt.append(temp)
    temp+=procesos[len(procesos)-1][2]
    reloj=temp

def turnaroundtime():    
    for i in range(len(procesos)):
        tat.append(Ct[i]-procesos[i][1])

def promedios():
    global prowt, prort, proct, protat
    for i in range(len(procesos)):
        prowt+=Wt[i]
        prort+=Rt[i]
        proct+=Ct[i]
        protat+=tat[i]
    prowt = prowt/len(procesos)
    prort = prort/len(procesos)
    proct = proct/len(procesos)
    protat = protat/len(procesos)

abrirarchivo()
reloj_WT()
turnaroundtime()
promedios()

print("Procesos\tArrival time\tburst time\tCT\tWT\tRT\tTAT")
for i in range(len(procesos)):
    print(procesos[i][0],"\t\t" ,procesos[i][1],"\t\t" , procesos[i][2],"\t\t" , Ct[i],"\t" , Wt[i],"\t" , Rt[i] ,"\t" , tat[i])

print("PROMEDIOS:\nPromedio CT:", proct,
      "\nPromedio WT:", prowt,
      "\nPromedio RT:", prort,
      "\nPromedio TAT:", protat)
