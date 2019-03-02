from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def search_database(request):
    print("in the function!!!")
    return Response()