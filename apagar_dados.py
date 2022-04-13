import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["dados_abertos"]
mycol = mydb["gastos_por_unidade"]

mycol.delete_many({})
