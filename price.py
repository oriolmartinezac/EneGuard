import sys
import sender
import os
from datetime import datetime

TOTAL_ITEMS = sys.argv[1]

class Item:
    def __init__(self, id, threshold):
        self.id = id
        self.price = sys.float_info.max
        self.best = False
        self.threshold = float(threshold) 

    def set_price(self, price):
        self.price = price

    def get_price(self):
        return self.price

    def get_threshold(self):
        return self.threshold

    def get_best(self):
        return self.best

    def get_id(self):
        return self.id

#def price_per_unit(price, apex_coins):
#    return price/apex_coins

def check_threshold(item, first_value, url):
    if (first_value - item.get_price()) >= item.get_threshold():
        #SEND_EMAIL
        sender.send_email(item.get_id(), item.get_price(), url)

def save_price(item):
    original_path = "./min/"+str(item.get_id())+".txt"
    new_path = "./min/"+str(item.get_id())+"_copy.txt"

    with open(original_path, "r") as read_obj:
        previous_price = float(read_obj.readline().split("|")[1])
        previous_date = read_obj.readline().split("|")[1]
        url = read_obj.readline().split("|")[1]
        first_price = float(read_obj.readline().split("|")[1]) 
    read_obj.close()
    
    if item.get_price() < previous_price:
        #WRITE in the file the new price
        with open(new_path, "w") as write_obj:
            write_obj.write("PRICE|"+str(item.get_price())+"|\n")
            write_obj.write("DATE|"+datetime.today().strftime('%Y-%m-%d-%H:%M:%S')+"|\n")
            write_obj.write("URL|"+url+"|\n")
            write_obj.write("FIRSTPRICE|"+str(first_price)+"|")
        write_obj.close()
            
        #Check for the threshold to send and email
        check_threshold(item, first_price, url)    

        #Mv copy to original
        os.remove(original_path)
        os.rename(new_path, original_path)

def search_string(file, item):
    
    word_bool = False

    with open(file, "r") as read_obj:
        for line in read_obj:
            listS = line.split(" ")
            for word in listS:
                if word == 'itemProp="price"':
                    word_bool = True
                elif word_bool == True:
                    new_price = float(word.split('"')[1])
                    word_bool = False
                    if new_price < item.get_price():
                        item.set_price(new_price)
    read_obj.close()

if __name__ == "__main__":
   
    listItem = []
    threshold_list = sys.argv[2].split(" ")

    for i in range(int(TOTAL_ITEMS)):    
        #Creating objects with id and threshold
        listItem.append(Item(i, threshold_list[i]))
        search_string("./web-pages/"+str(i)+".html", listItem[i]) 
        save_price(listItem[i])

