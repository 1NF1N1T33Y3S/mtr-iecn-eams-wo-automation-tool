import pymongo

if __name__ == "__main__":
    url = r"mongodb+srv://camfurt_db_user:RDTYmfKDHRZp6Smp@cluster0.cmoqi6n.mongodb.net/?appName=Cluster0"
    client = pymongo.MongoClient(url)
    names = client.list_database_names()
    print(f"{names=}")
    print("done")
