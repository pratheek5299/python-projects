"""
Program Details: 
    1. Fetch users data from the api and store it in the database.
    2. Get the users data from the database and fetch the posts corresponding to user from the api.
    3. Store the posts data in the database.
Author: Sai Pratheek Reddy Kasarla
Database: Firebase

"""
import os
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def fetch_data():
    users = []
    path = os.getcwd()
    certificate_file_name = 'fetch-data-cc5c5-firebase-adminsdk-o0txv-cfe57f3666.json'
    certificate_file_path = os.path.join(path, certificate_file_name)
    cred = credentials.Certificate(certificate_file_path)
    firebase_admin.initialize_app(cred)
    print('Fetching Users data...')
    req1 = requests.get('https://dummyapi.io/data/v1/user?page=0&limit=50', headers={'app-id': '65f3d46ab01ec36df14e005e'})
    req2 = requests.get('https://dummyapi.io/data/v1/user?page=1&limit=50', headers={'app-id': '65f3d46ab01ec36df14e005e'})
    users.extend(req1.json()['data'])
    users.extend(req2.json()['data'])
    print('Users data fetched !!!')
    db = firestore.client()

    print('Uploading Users to the database...')
    for user in users:
        doc_ref = db.collection('users').document()
        doc_ref.set(user)
    print('Users data uploaded to the database !!!')
    print('')
    print('Getting users data from the database....')
    users_from_db = []
    docs = db.collection('users').stream()
    for doc in docs:
        users_from_db.append(doc.to_dict())
    print('Users data retreived from the database!!!')
    for user in users_from_db:
        print('Fetching the posts of user==>', user['id'], '...')
        post_req = requests.get(f'https://dummyapi.io/data/v1/user/{user['id']}/post?limit=50', headers={'app-id': '65f3d46ab01ec36df14e005e'})  
        print('Posts Fetched!!!')
        print('Uploading Posts into database...')
        for post in post_req.json()['data']:
            doc_ref = db.collection('user' + user['id']).document()
            doc_ref.set(post)
        print('Posts data uploaded to the database!!!')
        
if __name__ == '__main__':
    fetch_data()