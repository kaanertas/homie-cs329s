from pymongo import MongoClient
from model import Model

connection_string = 'mongodb+srv://max:max_is_a_b3ast@cs329s.gefiw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'



def getData():
    client = MongoClient(connection_string)
    db = client.cs329s
    misclassifieds = db.misclassifieds.find({})
    return misclassifieds

def format_data(old_model, misclassifieds):
    print(misclassifieds)
    input()

def main():
    misclassifieds = getData()
    old_model = Model()
    ft_data = format_data(old_model, misclassifieds)
    finetune(old_model, misclassifieds)

if __name__ == '__main__':
    main()
