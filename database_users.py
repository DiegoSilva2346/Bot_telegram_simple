          
import datetime             
import operator       
import random           
import psycopg2        
"""El sistema de base de datos consiste en :      
-Tabla USUARIOS + NUMERO ID_CHAT , donde se almacena toda la informacion de cada chat grupal(numeros id_de los participanetes, nombres,comentarios, fecha del momento en que se realizo el  comentario)         
-Tabla CHAT_ID  donde se alamcena todos los numeros de  id_chat de todos los grupos donde esta el bot"""     
 
 
#Funcion decoradora que realiza multiples consultas sql.           
def select_decorator(punto=False):
  def crud_decorator(function):          
   def conexion_database(*args, **kwargs):         
      
    conect=psycopg2.connect(database="name_database",user="postgres",password="your_password",host="localhost",port=866)     
    micursor=conect.cursor()                        
                                        
    try:             
                     
       if punto==True:         
         sentencia_sql=function(*args,**kwargs)               
                    
                
         micursor.execute(sentencia_sql[0])           
         lista=micursor.fetchall()       
         if len(lista)>3000:           
           micursor.execute(sentencia_sql[1])         
           conect.commit()         
             

         conect.commit()               
                         
       else:                  
         sentencia_sql=function(*args,**kwargs)             
         micursor.execute(sentencia_sql)               
         conect.commit()           
       micursor.close() 
       conect.close()        
    except:            
       print("la tabla ya existe")
   return conexion_database             
  return crud_decorator
@select_decorator(punto=False)       
def create_table_chat_id():       
   try:          
     sentencia_sql="CREATE TABLE CHAT_ID (CHAT_ID VARCHAR(100) UNIQUE)  "              
  
   except:         
       print("La tabla CHAT_ID  ya existe, pasando a la siguiente ejecucion")               
   return sentencia_sql                  
            


@select_decorator(punto=False)         
def create_table_data_chat(chat_id):              
   try:            
    chat_id=str(chat_id).replace("-","")           
    sentencia_sql="CREATE TABLE USUARIOS"+chat_id+" (ID_USER INTEGER ,NOMBRE_USUARIO VARCHAR(60), COMENTARIO VARCHAR(2350),fecha date)"     
   except:         
       pass           
   return sentencia_sql                 
@select_decorator(punto=False) 
def append_user(data_user,chat_id):              
   print(data_user)                
   chat_id=str(chat_id).replace("-","")          
   sentencia_sql="INSERT INTO "+"USUARIOS"+chat_id+ " VALUES"+str(data_user)      
   return sentencia_sql 
@select_decorator(punto=True)           
def select_user_and_delete(chat_id):            
   chat_id=str(chat_id).replace("-","")               
   chat_id=str(chat_id)           
   sentencias_sql=["SELECT * FROM USUARIOS"+str(chat_id),"DELETE FROM USUARIOS"+str(chat_id),]     
   
   return sentencias_sql
@select_decorator(punto=False)        
def insert_chat_id(chat_id):                  
  try:     
   print("Estoy en insert chat id")               
   chat_id=str(chat_id).replace("-","")           
   sentencia_sql="""INSERT INTO CHAT_ID  VALUES ("""+str(chat_id)+""")"""          
 
  except:      
     pass 
  return sentencia_sql                   

@select_decorator(punto=False)           
def update_user(name_user,id_user,chat_id):          
  chat_id=str(chat_id).replace("-","")      
  name_user=name_user             
  sentencia_sql=("UPDATE USUARIOS"+str(chat_id)+" SET NOMBRE_USUARIO='{name_user}' "+" WHERE ID_USER="+str(id_user)).format(name_user=name_user)            
  return sentencia_sql        
       

