import firebase_admin
from firebase_admin import credentials, storage

def link(file):
    if not firebase_admin._apps:
        cred = credentials.Certificate("credentials.json") 
        firebase_admin.initialize_app(cred, {'storageBucket': 'your-storage-bucket-name.appspot.com'})  # Replace with your bucket name
    bucket = storage.bucket(name='limble-30e8a.appspot.com')
    blob = bucket.blob(file.filename)
    blob.upload_from_string(file.read(), content_type=file.content_type)
    blob.make_public()
    return blob.public_url
