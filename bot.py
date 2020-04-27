import telepot , os , time , csv , datetime
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

file_compiti = "compiti.csv"
file_temp = "temp.txt"
file_video = "video_lezioni.csv"
file_log = "log.txt"
separatore = '----------------------'

TOKEN = '' 

def gruppo_n_compito(msg,from_id,mes):
    data , materia , compito = mes.split('#')
    materia = materia.upper()
    file = open(file_compiti,"a")
    file.write(f"{data};{materia};{compito}\n")
    file.close()
    bot.sendMessage(-464632146,"compito aggiunto")

def gruppo_n_lezione(msg,from_id,mes):
    data, ore , materia , link = mes.split('#')
    materia = materia.upper()
    file = open(file_video,"a")
    file.write(f'{data};{ore};{materia};{link}\n')
    file.close()
    bot.sendMessage(-464632146,"lezione aggiunto")

def bot_c_generale(msg,from_id,val='futuro'):
    data = datetime.datetime.today()
    lista , c = [] , 0
    with open(file_compiti, newline="") as filecsv:
        lettore = csv.reader(filecsv,delimiter=";")
        for i in lettore:
            lista.append(i)
    lista.sort()
    if val == 'futuro':
            for i in lista:
                if i[0] > data.strftime("%d/%m/%Y"):
                    c +=1
                    bot.sendMessage(from_id,f"data : {i[0]}\nmateria : {i[1]}\n\ncompito:\n{i[2]}")
    else:
        for i in lista:
            if i[0] == val:
                c +=1
                bot.sendMessage(from_id,f"data : {i[0]}\nmateria : {i[1]}\n\ncompito:\n{i[2]}")
    if c == 0:
        bot.sendMessage(from_id,f"nesun compito")

def bot_l_generale(msg,from_id,val):

    lista , stringa , c = [] , f'   Materia  : orario \n{separatore}\n' , 0
    with open(file_video, newline="") as filecsv:
        lettore = csv.reader(filecsv,delimiter=";")
        for i in lettore:
            lista.append(i)
    lista.sort()
    for i in lista:
        if i[0] == val:
            c += 1
            stringa += f"{i[2]}  :  {i[1]:5} \n"
    if c == 0:
        bot.sendMessage(from_id,f"nesuna video lezione")
    else:
        bot.sendMessage(from_id,f"{stringa}")

def u_lista_scarica_generale(msg,from_id,file_copia):
    bot.sendMessage(from_id,'aspetta un attimo')
    file = open(file_copia,"r")
    file2 = open(file_temp,"w")
    file2.write(file.read())
    file.close()
    file2.close()
    bot.sendDocument(from_id,open(file_temp,  'rb' ))
    os.remove(file_temp)

def u_cm(from_id):
        bottoni = InlineKeyboardMarkup(inline_keyboard=[
                         [InlineKeyboardButton(text='OGGI', callback_data='cm.oggi')],
                         [InlineKeyboardButton(text='DOMANI', callback_data='cm.domani')],
                         [InlineKeyboardButton(text='FUTURO', callback_data='cm.futuro')],
                         [InlineKeyboardButton(text='LEZIONI OGGI', callback_data='cm.l_oggi')],
                         [InlineKeyboardButton(text='LEZIONI DOMANI', callback_data='cm.l_domani')],
        ] )
        bot.sendMessage(from_id, f'COMANDI', reply_markup=bottoni)

def chat_gruppo(msg,from_id):
    mes = msg['text']
    if mes[:7] == '/gruppo':
        bot.sendMessage(-464632146,"COMANDI \n\n/ncompito : nuovo compito \nfortato : data(gg/mm/aa)#materia#compito \nes : /ncompito 23/03/20#italinao#stuiare \n\n/nlezione : nuova diceo lezione \nfortato : data(gg/mm/aa)#ora(oo:mm)#materia#link(in asenza boh) \nes : /nlezione 23/08/20#9:15#chimica#boh ")
    elif mes[:9] == '/ncompito':
        mes = mes[10:]
        gruppo_n_compito(msg,from_id,mes)
    elif mes[:9] == '/nlezione':
        mes = mes[10:]
        gruppo_n_lezione(msg,from_id,mes)

def chat_bot(msg,from_id):
    mes = msg["text"].split()
    if mes[0] == '/start':
        bot.sendMessage(from_id,'Benvenuto in questo bot.\nTi consente di vedere i compiti e le video lezioni\nPer una lista di comnadi usa /help')
    elif mes[0] == '/help':
        bot.sendMessage(from_id,'     COMANDI\n/help : per richiamare quessta lista\n\n/cmt o cmt : list comandi essenziali testuali\n\n/cm o cm per i somnadi esenzili con i pulsanti')
        bot.sendMessage(from_id,'    --COMPITI--\n\n/c_oggi : per mostrare i compiti per oggi\n\n/c_domani : per mostrare i compiti per domani\n\n/c_futuro : per mostrare i compiti futuri\n\n/c_cerca data : permetter di cercare i compiti per data \nes : \c_cerca 14/05/20\n\n/c_lista : scarica i databese dei compiti')
        bot.sendMessage(from_id,'    --VIDEO LEZIONI--\n\n/l_oggi : video lezioni di oggi\n\n/l_domani : viedo lezioni di domani\n\n/l_lista : scarica i databese delle video lezioni')

    elif mes[0] == '/cmt' or mes[0] == 'cmt':
        bot.sendMessage(from_id,'/c_oggi\n/c_domani\n/c_futuro\n/c_cerca\n/l_oggi\n/l_domani')
    elif mes[0] == '/cm' or mes[0] == 'cm':
        u_cm(from_id)
    elif mes[0] == '/c_oggi':
        data = datetime.datetime.today()
        bot_c_generale(msg,from_id,data.strftime("%d/%m/%y"))
    elif mes[0] == '/c_domani':
        data = datetime.datetime.today() + datetime.timedelta(days=1)
        bot_c_generale(msg,from_id,data.strftime("%d/%m/%y"))
    elif mes[0] == '/c_futuro':
        bot_c_generale(msg,from_id,'futuro')
    elif mes[0] == '/c_cerca':
        if len(mes) == 2:
            bot_c_generale(msg,from_id,mes[1])
        else:
            bot.sendMessage(from_id,'devi metterci ache la data')
    elif mes[0] == '/l_oggi':
        data = datetime.datetime.today()
        bot_l_generale(msg,from_id,data.strftime("%d/%m/%y"))
    elif mes[0] == '/l_domani':
        data = datetime.datetime.today() + datetime.timedelta(days=1)
        bot_l_generale(msg,from_id,data.strftime("%d/%m/%y"))
    elif mes[0] == '/l_lista':
        u_lista_scarica_generale(msg,from_id,file_video)
    elif mes[0] == '/c_lista':
        u_lista_scarica_generale(msg,from_id,file_compiti)
    elif mes[0] == '/a_log':
        u_lista_scarica_generale(msg,from_id,file_log)

def on_chat_message(msg):
    content_type, chat_type, from_id = telepot.glance(msg)
    date , user , text  = datetime.datetime.now().strftime('%d/%m/%y | ora:%H:%M:%S') , msg['from']['first_name'] , msg['text']
    if content_type == "text":
        file = open(file_log,"a")
        file.write(f'chat id:{from_id:10} | username:{user:25} | data:{date} | mess:{text} \n')
        file.close()
        print(f'chat id:{from_id:10} | username:{user:25} | data:{date} | mess:{text} ')
        if  from_id == -464632146:
            chat_gruppo(msg,from_id)
        else:
            chat_bot(msg,from_id)

def on_callback_query(msg):
        query_id , from_id ,query_data = telepot.glance(msg , flavor= 'callback_query')
        date , user  = datetime.datetime.now().strftime('%d/%m/%y | ora:%H:%M:%S') , msg['from']['first_name'] ,
        file = open(file_log,"a")
        file.write(f'chat id:{from_id:10} | username:{user:25} | data:{date} | butt:{query_data} \n')
        file.close()
        print(f'chat id:{from_id:10} | username:{user:25} | data:{date} | butt:{query_data} ')
        menu , oggetto = query_data.split('.')
        if menu == 'cm':
            if oggetto == 'oggi':
                data = datetime.datetime.today()
                bot_c_generale(msg,from_id,data.strftime("%d/%m/%y"))
            elif oggetto == 'domani':
                data = datetime.datetime.today() + datetime.timedelta(days=1)
                bot_c_generale(msg,from_id,data.strftime("%d/%m/%y"))
            elif oggetto == 'futuro':
                bot_c_generale(msg,from_id,'futuro')
            elif oggetto == 'l_oggi':
                data = datetime.datetime.today()
                bot_l_generale(msg,from_id,data.strftime("%d/%m/%y"))
            elif oggetto == 'l_domani':
                data = datetime.datetime.today() + datetime.timedelta(days=1)
                bot_l_generale(msg,from_id,data.strftime("%d/%m/%y"))
            bot.sendMessage(from_id,separatore)




bot = telepot.Bot(TOKEN)
bot.message_loop({'chat':on_chat_message,'callback_query':on_callback_query})

print('Listening ...')

while 1:
    time.sleep(10)
