import firebase_admin
from firebase_admin import credentials, storage
from io import BytesIO

from app.firebase_config import firebase_config

class FirebaseManager:

    _instance = None

    def __new__(cls, *args, **kwargs):

        if not cls._instance:

            if not firebase_admin._apps:

                #cred = credentials.Certificate("firebase-config.json")
                cred = credentials.Certificate(firebase_config)
                firebase_admin.initialize_app(cred, {
                    'storageBucket': 'exponere-ec67d.appspot.com'
                })

                cls._instance = super(FirebaseManager, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def upload_image_to_storage(self, image_data, destination_blob_name):

        try:

            bucket = storage.bucket()

            image_file = BytesIO(image_data)

            blob = bucket.blob(destination_blob_name)
            blob.upload_from_file(image_file)
            blob.make_public()

            image_url = blob.public_url

            if not image_url:

                raise Exception('URL pública da imagem não encontrada')
            
            return image_url
        
        except Exception as e:

            print(f'Erro ao enviar imagem para o Firebase Storage: {e}')
            
            return None