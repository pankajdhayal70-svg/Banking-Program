import random
import datetime
import json

accounts={}

class Bank:

    def __init__(self,name,user_id,password):
        self.name=name
        self.user_id=user_id
        self.password=password
        self.balance=0
        self.block=[False,0]
        self.history=["   Date    | Time  | Balance | Description"]
        data=datetime.datetime.now().strftime(f"%d-%m-%Y | %H:%M | ${self.balance:<6} | account created")
        self.history.append(data)

    def __str__(self):
        return f"Name : {self.name}\nUser id : {self.user_id}\nBalance : {self.balance}"

    @classmethod
    def new_user(cls):
        print("To return to login page press 1")
        name=input("Name : ")
        if name=='1':
            return
        while not name.replace(" ","").isalpha():
            name=input("Enter a valid name : ")
        user_id=random.randint(1001,10000)
        while user_id in accounts:
            user_id=random.randint(1001,10000)
        user_id=str(user_id)
        print(f"User id : {user_id}")
        password=input("Password : ")
        user=Bank(name,user_id,password)
        accounts[user_id]=user

    def update_information(self):
        self.name=input("Name : ")
        self.change_password()

    def change_password(self):
        for i in range(3):
            old_password=input("Old Password : ")
            if old_password==self.password:
                break
            elif i==2:
                print("Too many attempts")
                return
            
        self.password=input("New Password : ")
        print("Password Updated")

    def deposit(self):
        is_running=True
        while is_running:
            amount=input("Amount : ")
            if not amount.isdigit():
                print("Invalid amount")
                continue
            amount=int(amount)
            if amount<=0:
                print("Invalid amount")
                continue
            is_running=False
        self.balance+=amount
        time=datetime.datetime.now().strftime(f"%d-%m-%Y | %H:%M | ")
        self.history.append(f"{time}${self.balance:<6} | {amount} deposited to account")
        print(f"Balance : {self.balance}")

    def withdraw(self):
        if self.balance==0:
            print("No amount to withdraw")
            print(f"Balance : {self.balance}")
            return
        is_running=True
        while is_running:
            amount=input("Amount : ")
            if not amount.isdigit():
                print("Invalid amount")
                continue
            amount=int(amount)
            if amount<=0 | amount>self.balance:
                print("Invalid amount")
                continue
            is_running=False
        self.balance-=amount
        time=datetime.datetime.now().strftime(f"%d-%m-%Y | %H:%M | ")
        self.history.append(f"{time}${self.balance:<6} | {amount} withdrawal from account")
        print(f"Balance : {self.balance}")


    def transfer(self):
        if self.balance==0:
            print("No amount to transfer.")
            print(f"Balance : {self.balance}")
            return
        receiver_id=input("Receiver's uid : ")
        while not(receiver_id in accounts):
            print("NO such user id")
            receiver_id=input("Receiver's uid : ")
        while receiver_id==self.user_id:
            print("Enter receiver's id not yours.")
            receiver_id=input("Recivier's uid : ")
        receiver=accounts[receiver_id]
        is_running=True
        while is_running:
            amount=input("Amount : ")
            if not amount.isdigit():
                print("Invalid amount")
                continue
            amount=int(amount)
            if amount<=0 | amount>self.balance:
                print("Invalid amount")
                continue
            is_running=False
        self.balance-=amount
        receiver.balance+=amount
        time=datetime.datetime.now().strftime(f"%d-%m-%Y | %H:%M | ")
        self.history.append(f"{time}${self.balance:<6} | {amount} transferred to {receiver.name}")
        receiver.history.append(f"{time}${receiver.balance:<6} | {amount} received from {self.name}")

    def show_history(self):
        for i in self.history:
            print(i)

def load_data():
    try:
        with open("account_details.json",'r') as file:
            data=json.load(file)
            for user_id,user_data in data.items():
                user=Bank(user_data["name"],user_data["user_id"],user_data["password"])
                user.history=user_data["history"]
                user.block=user_data["block"]
                user.balance=user_data["balance"]
                accounts[user_id]=user
    except FileNotFoundError:
        pass
    except Exception as e:
        print(e)

load_data()

def login():
    user_id=input("user_id : ")
    if not(user_id in accounts):
        print("Wrong user id")
        return None
    user=accounts[user_id]
    if user.block[0]:
        now=datetime.datetime.now()
        unblock_time=datetime.datetime.strptime(user.block[1],"%d-%m-%Y %H:%M")
        if unblock_time>now:
            print(f"Account is blocked")
            print(f"Curent Time : {now.strftime('%d-%m-%Y %H:%M')}")
            print(f"unblock Time : {unblock_time.strftime('%d-%m-%Y %H:%M')}")
            print(f"Total time left : {str(unblock_time-now).split('.')[0]}")
            return None
        else:
            user.block=[False,0]
            save_data()

    password=input("Password : ")
    n=1
    while not(password==user.password) :
        if n==3:
            print("Account blocked for 1hr(Try AFTER 1H).")
            time=datetime.datetime.now().strftime(f"%d-%m-%Y | %H:%M | ")
            user.history.append(f"{time}${user.balance:<5} | Account blocked for 1H.")
            block_user(user)
            return None

        print(f"Wrong Password({3-n} attempts left)")
        password=input("Password : ")
        n+=1
    return user

def block_user(user):
    block_time=datetime.datetime.now()
    unblock_time=block_time+datetime.timedelta(hours=1)
    user.block=[True,unblock_time.strftime("%d-%m-%Y %H:%M")]

def show_menu():
    print("************************")
    print("1.Account Information")
    print("2.Deposit")
    print("3.Withdraw")
    print("4.Transfer")
    print("5.History")
    print("6 Edit account information")
    print("7.Return to login")
    print("************************")

def save_data():
    data={}
    with open("account_details.json",'w') as file:
        for uid,user in accounts.items():
            data[uid]={"name":user.name,
                       "user_id":user.user_id,
                       "password":user.password,
                       "balance":user.balance,
                       "block":user.block,
                       "history":user.history}
            
        json.dump(data,file,indent=4)


def main():
    is_running1=True
    while is_running1:
        print("1.Create account\n2.Login\n3.Exit Program")
        n=input()
        if n=='1':
            Bank.new_user()
        elif n=='2':
            user=login()
            if user==None:
                save_data()
                continue
            is_running2=True
            while is_running2:
                show_menu()
                op=input()
                if op=='1':
                    print(user)
                elif op=='2':
                    user.deposit()
                elif op=='3':
                    user.withdraw()
                elif op=='4':
                    user.transfer()
                elif op=='5':
                    user.show_history()
                elif op=='6':
                    user.update_information()
                elif op=='7':
                    is_running2=False
                else:
                    print("Not in options")
                save_data()
        elif n=='3':
            is_running1=False
        else:
            print("Invalid option.Please choose from menu")
        save_data()

if __name__=="__main__":
    main()