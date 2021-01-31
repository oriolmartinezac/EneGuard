import sys
import os
from datetime import datetime

TOTAL_ITEMS = sys.argv[1]

class Item:
    def __init__(self, id):
        self.id = id
        self.price = sys.float_info.max

    def set_price(self, price):
        self.price = price

    def get_price(self):
        return self.price

    def get_id(self):
        return self.id

def save_price(item):
    original_path = "./min/"+str(item.get_id())+".txt"
    new_path = "./min/"+str(item.get_id())+"_copy.txt"

    with open(original_path, "r") as read_obj:
        #Get old content of the file
        lines = read_obj.readlines()
    read_obj.close()
    
    with open(new_path, "w") as write_obj:
        #Generate the new content
        write_obj.write("PRICE|"+str(item.get_price())+"|\n") 
        write_obj.write("DATE|"+datetime.today().strftime('%Y-%m-%d-%H:%M:%S')+"|\n")
        write_obj.write(lines[2])
        write_obj.write("FIRSTPRICE|"+str(item.get_price())+"|\n")
    write_obj.close()

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
    
    for i in range(int(TOTAL_ITEMS)):   
        #Creating objects with id and threshold
        listItem.append(Item(i))
        search_string('./web-pages/'+str(i)+'.html', listItem[i])
        save_price(listItem[i])
