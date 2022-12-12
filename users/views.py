import json

from rest_framework.response import Response
from rest_framework.views import APIView


class FileReadWriteService:
    _file_name = None


    @classmethod
    def load_users(cls):
        try:
            with open(cls._file_name) as file:
                return json.load(file)
        except (Exception):
            return []

    @classmethod
    def save_users(cls, data):
        try:
            with open(cls._file_name, 'w') as file:
                json.dump(data, file)

        except Exception as err:
            return str(err)


class MyAPIView(APIView, FileReadWriteService):
    _file_name = 'users.json'
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.users = self.load_users()


class UsersListCreateView(MyAPIView):
    def get(self, *args, **kwargs):
        return Response(self.users)
    def post(self, *args, **kwargs):

        data = self.request.data

        data['id'] = self.users[-1]['id']+1 if self.users else 1
        self.users.append(data)
        self.save_users(self.users)
        return Response(data)

class UserRetrieveUpdataDestroyView(MyAPIView):

    def get(self, *args, **kwargs):
        pk = kwargs.get('pk')
        user =  self._get_user_by_pk(pk)
        if user is None:
           return Response('Not fo')

        return Response(user)

    def put(self, *args, **kwargs):

        pk = kwargs.get('pk')
        user = self._get_user_by_pk(pk)

        if user is None:
           return Response('Not found')

        data = self.request.data

        if data.get('id'):
            del data['id']


        user |= data
        self.save_users(self.users)
        return Response(user)

    def delete(self,*args, **kwargs):
        pk = kwargs.get('pk')
        index = next((i for i, v in enumerate(self.users) if v['id'] == pk), None)
        if index is None:
            return Response('Not found')

        del self.users[index]
        self.save_users(self.users)
        return Response('deleted')







    def _get_user_by_pk(self, pk):
        user = next((user for user in self.users if user['id'] ==pk), None)


