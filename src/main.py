### --------------------------- ###
### Import Essential Libraries  ###
### --------------------------- ###

import mysql.connector
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

print ("**************************************************************************")
print ("W E L C O M E   T O  I n v e n t o r y   M a n a g e m e n t   S y s t e m")
print ("**************************************************************************")

### ----------------------------- ###
### Establish Database connection ###
### ----------------------------- ###

my_conn = mysql.connector.connect(host="localhost",password="password",user="root",database = "ims",port="3306")
if my_conn.is_connected():
	print("Connection established")
my_cursor = my_conn.cursor()

### ------------------------------- ###
### Definition of modular functions ###
### ------------------------------- ###

def add_item():
    ino = int(input("Enter Item No"))
    iname = input ("Enter Item name")
    prate = float(input("Enter Purchase rate"))
    srate = float(input("Enter Sale rate"))
    qoh = int(input("Enter quantity on hand"))
    q="insert into items values({},'{}',{},{},{});".format(ino,iname,prate,srate,qoh)
    my_cursor.execute(q)
    my_conn.commit()
    print("****Item Added****")
def edit_item():
    ino=int(input("Enter Item No."))
    q="select * from items where item_no ={};".format(ino)
    my_cursor.execute(q)
    if my_cursor.fetchone():
        iname=input("Enter Item Name")
        my_cursor.execute("Update Items set item_desc = '{}' where item_no={};".format(iname,ino))
        my_conn.commit()
        print("****Item Edited****")
    else:
        print("****Item not Found****")
  
def fix_rate():
    ino=int(input("Enter Item No."))
    q="select * from items where item_no = {};".format(ino)
    my_cursor.execute(q)
    if my_cursor.fetchone():
        prate=int(input("Enter new purchase rate"))
        srate=int(input("Enter new Sale Rate"))
        my_cursor.execute("update items set cp={},sp={} where item_no={};".format(prate,srate,ino))
        my_conn.commit()
        print("****New Rate Applied****")
    else:
        print("****Item not Found****")

def search_item():
    ino=int(input("Enter Item No."))
    q="select * from items where item_no ={};".format(ino)
    my_cursor.execute(q)
    if my_cursor.fetchone():
       df=pd.read_sql(q,my_conn)
       print(tabulate(df,headers="keys",tablefmt="psql", showindex = False))
    else:
       print("Item not Found")
       
def add_customer():
    cid = int(input("Enter Customer ID"))
    cname = input ("Enter Customer name")
    cadd = input("Enter Address")
    mobile = input("Enter Mobile number")
    q="insert into customers values({},'{}','{}',{});".format(cid,cname,cadd,mobile)
    my_cursor.execute(q)
    my_conn.commit()	
    print("****Customer Added****")

def edit_customer():
    cid=int(input("Enter Customer ID"))
    q="select * from customers where cust_id ={};".format(cid)
    my_cursor.execute(q)
    if my_cursor.fetchone():
        cadd=input("Enter Customer Address")
        my_cursor.execute("Update customers set address = '{}' where cust_id={};".format(cadd,cid))
        my_conn.commit()
        print("****Customer Edited****")
    else:
        print("****Customer not Found****")

def delete_customer ():
    cid=int(input("Enter Customer ID"))
    q="select * from customers where cust_id={};".format(cid)
    my_cursor.execute(q)
    if my_cursor.fetchone():
        my_cursor.execute("delete from customers where cust_id={};".format(cid))
        my_conn.commit()
        print("****Customer Deleted****")
    else:
        print("****Customer not Found****")

def search_customer ():
    cname=input("Enter Customer Name")
    q="select * from customers where cust_name like '%{}%';".format(cname)
    my_cursor.execute(q)

    if my_cursor.fetchall():
       df=pd.read_sql(q,my_conn)
       print(tabulate(df,headers='keys',tablefmt='psql',showindex = False))
    else:
       print("Customer not Found")        
    
        
def add_supplier():
    sid = int(input("Enter Supplier ID"))
    sname = input ("Enter Supplier name")
    sadd = input("Enter Address")
    mobile = input("Enter Mobile number")
    q="insert into suppliers values({},'{}','{}',{});".format(sid,sname,sadd,mobile)
    my_cursor.execute(q)
    my_conn.commit()
    print("****Supplier Added****")

def edit_supplier():
    sid=int(input("Enter Supplier ID"))
    q="select * from suppliers where supp_id ={};".format(sid)
    my_cursor.execute(q)
    if my_cursor.fetchone():
        sadd=input("Enter Supplier Address")
        my_cursor.execute("Update Suppliers set address = '{}' where supp_id={};".format(sadd,sid))
        my_conn.commit()
        print("****Supplier Edited****")
    else:
        print("****Supplier not Found****")

def delete_supplier ():
    sid=int(input("Enter supplier ID"))
    q="select * from suppliers where supp_id= {};".format(sid)
    my_cursor.execute(q)
    if my_cursor.fetchone():
        my_cursor.execute("delete from suppliers where supp_id = {};".format(sid))
        my_conn.rollback()
        print("****Supplier Deleted****")
    else:
        print("****Supplier not Found****")
        
def search_supplier ():
    sname=input("Enter Supplier Name")
    q="select * from suppliers where supp_name like '%{}%';".format(sname)
    my_cursor.execute(q)

    if my_cursor.fetchall():
       df=pd.read_sql(q,my_conn)
       print(tabulate(df,headers='keys',tablefmt='psql',showindex = False))
    else:
       print("Supplier not Found")        
    
def purchase():
    pur_id=0
    total=0
    grand=0
    l=[]
    ch='y'
    q= "select max(pur_id)as largest from purchase_master"
    my_cursor.execute(q)
    r=my_cursor.fetchone()[0]
    if r:
        pur_id=r+1
    else:
        pur_id=1
    print(pur_id)   
    pur_date=input("Enter Purchase Date")
    supp_id=int(input("Enter Supplier ID"))
    my_cursor.execute(("select * from suppliers where supp_id={};".format(supp_id)))
    if my_cursor.fetchone():
       print("Item Details")

       df=pd.read_sql("select * from items",my_conn)
       print("df done")
       print(tabulate(df,headers='keys',tablefmt='plsql',showindex=False))
       while(ch=='y'):              
       
               ino=int(input("Enter Item No."))
               my_cursor.execute("select * from items where item_no ={};".format(ino))
               r1=my_cursor.fetchone()
               if r1:
                       qty=int(input("Enter Quantity"))
                       rate= r1[2]
                       total=qty*rate
                       grand=grand+total
                       t=(pur_id,ino,qty,rate,total)
                       l.append(t)
               else:
                      print("Item not found")
               ch=input("Do you wish to add more items in the Bucket y/n")
       q1="insert into purchase_master values ({},'{}',{},{});".format(pur_id,pur_date,supp_id,grand)
       my_cursor.execute(q1)
       my_conn.commit()
       q2="insert into pur_dtls values(%s,%s,%s,%s,%s);"
       my_cursor.executemany(q2,l)
       my_conn.commit()
       my_cursor.executemany("insert into ptemp values(%s,%s,%s,%s,%s);",l)
       my_conn.commit()
       q3="update items join ptemp using(item_no) set items.qty = items.qty+ptemp.quantity"
       my_cursor.execute(q3)
       my_conn.commit()
       my_cursor.execute("delete from ptemp")
       my_conn.commit()
       print("Item purchased and added")
                      

def sale():
        saleid=0
        total=0
        grand=0
        l=[]
        ch='y'
        q= "select max(sale_id)as largest from sales_master"
        my_cursor.execute(q)
        r=my_cursor.fetchone()[0]
        if r:
                saleid=r+1
        else:
                saleid=1
        sdate=input("Enter Sale Date")
        cid=int(input("Enter Customer ID"))
        my_cursor.execute("select * from customers where cust_id ={};".format(cid))

        
        if my_cursor.fetchone():
                print("Item Details")
                df=pd.read_sql("select * from items",my_conn)
                print(tabulate(df,headers='keys',tablefmt='plsql',showindex=False))

                while(ch=='y'):
                     ino=int(input("Enter the item to be sold"))
                     my_cursor.execute("select * from items where item_no ={};".format(ino))
                     r1=my_cursor.fetchone()
                     if r1:
                            qty=int(input("Enter Quantity"))
                            rate = r1[3]
                            total=qty*rate
                            grand=grand+total
                            t=(saleid,ino,qty,rate,total)
                            l.append(t)
                     else:
                             print("Item not found")
                             ch=input("Do you wish to add more items in the Bucket y/n")
                q1="insert into sales_master values ({},'{}',{},{});".format(saleid,sdate,cid,grand)
                my_cursor.execute(q1)
                my_conn.commit()
                             
                q2="insert into sale_dtls values(%s,%s,%s,%s,%s);"
                my_cursor.executemany(q2,l)
                my_conn.commit()

                             
                q3="insert into stemp values(%s,%s,%s,%s,%s);"
                my_cursor.executemany(q3,l)
                my_conn.commit()

                q4="update items join stemp using(item_no) set items.qty = items.qty-stemp.quantity"
                my_cursor.execute (q4)
                my_conn.commit()
                my_cursor.execute("delete from stemp")
                my_conn.commit()
                print("Item sold to customer and deducted")

def show_sale():
    bdate=input("Enter sales beginnning date")
    edate=input("Enter sales End date")
    df=pd.read_sql("select * from sales_master where sale_date between '{}' and '{}';".format(bdate,edate),my_conn)
    print(tabulate(df,headers='keys', tablefmt='plsql',showindex=False))

def show_purchase():
    bdate=input("Enter purchase beginnning date")
    edate=input("Enter purchase End date")
    df=pd.read_sql("select * from purchase_master where pur_date between '{}' and '{}';".format(bdate,edate),my_conn)
    print(tabulate(df,headers='keys', tablefmt='plsql',showindex=False))

def best_product():
   s=input("Enter start date")
   e=input("Enter End date")
   q="select s2.item_no,sum(s2.quantity) as total from sales_master s1 , sale_dtls s2\
     where s1.sale_id = s2.sale_id and s1.sale_date between '{}' and '{}'\
     group by s2.item_no;".format(s,e)
   df=pd.read_sql(q,my_conn)
   print(tabulate(df,headers='keys', tablefmt='plsql',showindex=False))
   plt.bar(df.item_no,df.total)
   plt.xlabel("Item code")
   plt.ylabel("Qty")
   plt.title("Best Selling Product")
   plt.xticks(df.item_no)
   plt.show()

def sale_performance():
    y=input("Enter year")
    q="select month(sdate) as month,sum(total)\
    as total from smaster where year(sdate) = '{}'\
    group by month(sdate);".format(y)
    df=pd.read_sql(q,my_conn)
    print(tabulate(df,headers='keys', tablefmt='psql',showindex=False))
    plt.plot(df.month,df.total)
    plt.xlabel("Month")
    plt.ylabel("Total Sale")
    plt.xticks(df.month)
    plt.show()
##########----------------------------------------------------##########
##########   M A I N   P R O G R A M   S T A R T S   H E R E  ##########
##########----------------------------------------------------##########


while(True):
    print("\nEnter your choice\n1. Setup\n2. Transactions\n3. View Reports\n4. Exit")
    ch=int(input())
    if ch==1:
            print ("Y O U  H A V E  C H O S E N  S E T U P")
            print("\nEnter your choice\n  1.Item Addition \n  2.Item Update \n  3.Fix Rate \n  4.Customer Addition \n  5.Customer Edit \n  6.Customer Delete \n  7.Supplier Addition\n  8.Edit Supplier \n  9.Delete Supplier\n 10.Exit")
            ch1=int(input())
            if (ch1==1):
                    print ("  I T E M    A D D I T I O N")
                    add_item()
            elif (ch1==2):
                    print ("     I T E M   U P D A T E")
                    edit_item()
            elif (ch1==3):
                    print ("     F I X   I T E M   R A T E")
                    fix_rate()
            elif (ch1==4):
                    print ("     C U S T O M E R   A D D I T I O N")
                    add_customer()
            elif (ch1==5):
                    print ("     E D I T   C U S T O M E R")
                    edit_customer()
            elif (ch1==6):
                    print ("     D E L E T E   C U S T O M E R")
                    delete_customer()

                    
            elif (ch1==7):
                    print ("     S U P P L I E R   A D D I T I O N")
                    add_supplier()
            elif (ch1==8):
                    print ("     E D I T   S U P P L I E R")
                    edit_supplier()
            elif (ch1==9):
                    print ("     D E L E T E   S U P P L I E R")
                    delete_supplier()
            elif (ch1==10):
                    print ("     E X I T")
                    break
    elif ch==2:
            print ("Y O U   H A V E   C H O S E N  Transactions")
            print("\nEnter your choice\n     1.Purchase of an item \n     2.Sale of an item")
            ch2=int(input())
            if (ch2==1):
                    print ("    P U R C H A S E   OF   A N   I T E M")
                    purchase()
            elif (ch2==2):
                    print ("     S A L E   O F   A N   I T E M")
                    sale()
            elif (ch2==4):
                    print ("     E X I T")
                    break
            
    elif ch==3:
            print ("Y O U   H A V E   C H O S E N  View Reports")
            print("\nEnter your choice\n1. Item search \n2. Customer search\n3. Supplier search\n4. Show Sales \n5. Show Purchase \n6. Best Product")
            ch3=int(input())
            if (ch3==1):
                    print ("    I T E M   S E A R C H" )
                    search_item()
            elif (ch3==2):
                    print ("    C U S T O M E R   S E A R C H")
                    search_customer()
            elif (ch3==3):
                    print ("    S U P P L I E R    S E A R C H")
                    search_supplier()
            elif (ch3==4):
                    print ("    S H O W  S A L E S")
                    show_sale()
            elif (ch3==5):
                    print ("    S H O W  P U R C H A S E")
                    show_purchase()
            elif (ch3==6):
                    print ("    B E S T  P R O D U C T")
                    best_product()
                    
            elif (ch3==7):
                    print ("    E X I T")
                    break
    elif ch==4:
            print ("Program Exiting")
            break
print("----------------")