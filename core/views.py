from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

# TODO convert activation from post to get request


class TempUserActivationView(APIView):
    def get(self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/auth/users/activation/"

        post_data = {'uid': uid, 'token': token}

        headers = {
            'Content-Type': 'application/json',
        }

        try:
            result = requests.post(post_url, json=post_data, headers=headers)
            result.raise_for_status()
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        content = result.text
        return Response(content)
