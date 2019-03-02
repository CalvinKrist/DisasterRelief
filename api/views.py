from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import api.models as models

# Used to search the database with JSON object
@api_view(['POST', 'GET'])
def search_database(request):
    # Make sure query isn't empty
    if request.body == b'':
        return Response( {"detail" : "Invalid request: empty request"} )

    if request.method == 'POST':
        # Load request as a dict object
        json_request = None
        try:
            json_request = json.loads(request.body)
        except:
            return Response( {"detail" : "Invalid request: invalid JSON"} )

        return models.handle_search_from_json(json_request)

    elif request.metod == 'GET':
        # Make sure query isn't empty
        if request.body == b'':
            return Response({"detail": "Invalid request: empty request"})

        return models.handle_search_from_string(request.body)
