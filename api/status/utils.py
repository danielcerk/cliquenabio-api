import requests

class GetAttributes:

    url = 'https://api.github.com/repos/danielcerk/CliqueNaBio/contributors'

    def __init__(self):

        pass

    def get_contribuitors(self):

        response = requests.get(self.url)

        if response.status_code == 200:

            contribuitors = {}

            for i in response.json():

                contribuitors[i['login']] = i['avatar_url']

            return contribuitors

        else:

            return 'Um erro inesperado ocorreu, Tente novamente mais tarde!'
        
    def get_status_app(self):

        pass

    def get_status_db(self):

        pass