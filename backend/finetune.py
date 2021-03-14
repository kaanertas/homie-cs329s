from pymongo import MongoClient
from model import Model

connection_string = 'mongodb+srv://max:max_is_a_b3ast@cs329s.gefiw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'



def getData():
    client = MongoClient(connection_string)
    db = client.cs329s
    misclassifieds = db.misclassifieds.find({})
    properties = db.properties({})
    return misclassifieds, properties

def format_data(old_model, misclassifieds, properties):
    property_map = {p['_id']: p for p in properties}
    for example in misclassifieds:
        property_id = example['property']
        prop = property_map[property_id]

    input()

def main():
    misclassifieds, properties = getData()
    old_model = Model()
    ft_data = format_data(old_model, misclassifieds, properties)
    finetune(old_model, misclassifieds)

if __name__ == '__main__':
    main()
