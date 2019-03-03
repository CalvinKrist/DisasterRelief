from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import api.models as models
from django.core import serializers
from datetime import datetime
from django.http import HttpResponse
from django.views.generic import ListView
from django.shortcuts import render

class AlertList(ListView):
    model = models.MediaAlert



    template_name = 'api/mediaalert_list.html'

    def get(self, request, *args, **kwargs):
        if request.body == b'':
            return HttpResponse({"detail": "Invalid request: empty request"})

        # Load request as a dict object
        json_request = None
        try:
            json_request = json.loads(request.body)
        except:
            return HttpResponse("<h1> Syntax Error: </h1></br></br><h3>Invalid JSON</h3>")

        try:
            query  = models.get_search_from_json(json_request)
            result = models.MediaAlert.objects.filter(query)

            list_result = list(result.values())

            # Replace geo_location objects with actual values. drop id
            for result in list_result:
                if "geo_location_id" in result:
                    try:
                        result["geo_location"] = models.GeoLocation.objects.get(id=result["geo_location_id"])
                        del result["geo_location_id"]
                    except:
                        pass

            context = {'alert_list' : list_result}

            print("rendinering")

            if len(list_result) == 0:
                return HttpResponse("<h1>No Results Found<h1>")
            return render(request, self.template_name, context)
        except models.MediaAlert.DoesNotExist as e:
            return HttpResponse( "MediaAlter Does not Exist: " + str(e) )
        except models.SyntaxException as e:
            return HttpResponse("<h1> Syntax Error: </h1></br></br><h3>" + str(e) + "</h3>")
    '''
    def post(self, request, *args, **kwargs):
        request.method = 'GET'
        return AlertList.as_view()(request)'''

    def post(self, request, *args, **kwargs):
        request.method = 'GET'
        return AlertList.as_view()(request)

# Used to search the database with JSON object
# Returns the objects as a JSON.
# For use by other developers
@api_view(['POST'])
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

    '''elif request.metod == 'GET':
        # Make sure query isn't empty
        if request.body == b'':
            return Response({"detail": "Invalid request: empty request"})

        return models.handle_search_from_string(request.body)'''

@api_view(['PUT'])
def add_to_database(request):
    # Make sure query isn't empty
    if request.body == b'':
        return Response({"detail": "Invalid request: empty request"})

    # Load request as a dict object
    json_request = None
    try:
        json_request = json.loads(request.body)
    except:
        return Response({"detail": "Invalid request: invalid JSON"})

    # Make sure required parameters exist
    if "source_type" not in json_request.keys():
        return Response({'detail' : "missing source_type"})
    if "url" not in json_request.keys():
        return Response({'detail' : "missing url"})
    if "disaster_type" not in json_request.keys():
        json["disaster_type"] = ""

    print("disatstor type: " + json_request["disaster_type"])
    # Save request to database
    alert = models.MediaAlert(source_type=json_request["source_type"],
                              url=json_request["url"], disaster_type=json_request["disaster_type"])

    # check for optional parameters
    if "date_created" in json_request.keys():
        # date in format in format 2018-12-19
        try:
            alert.date_created = datetime.strptime(json_request["date_created"], '%Y-%m-%d')
        except Exception as  e:
            print(json_request["date_created"])
            print("dateimte format " + json_request["date_created"] + " incorrect: " + str(e))
            return Response("dateimte format " + json_request["date_created"] + " incorrect: " + str(e))
    if "location_name" in json_request.keys():
        print("location_name found: " + json_request["location_name"])
        alert.location_name = json_request["location_name"]
    if "country" in json_request.keys():
        print("country found: " + json_request["country"])
        alert.country = json_request["country"]
    # Request in format "latitude,longitude"
    if "geo_location" in json_request.keys():
        print("geo_location found: " + json_request["geo_location"])
        points = json_request["geo_location"]
        geo_model = models.GeoLocation(latitude=points[0], longitude=points[1])
        geo_model.save()
        alert.geo_location = geo_model
    if "disaster_severity" in json_request.keys():
        print("disaster_severity found: " + json_request["disaster_severity"])
        alert.disaster_severity = json_request["disaster_severity"]
    if "tags" in json_request.keys():
        print("tags found: " + json_request["tags"])
        alert.tags = json_request["tags"]

    print("Entry saved to database.")
    alert.save()

    return Response("Success")

# Used to search the database with JSON object
# Retuns HTML. Intended to be used as a website page.
@api_view(['POST'])
def search_database_web(request):
    return HttpResponse(request.body)

def load_file(file_path):
    with open(file_path, 'rb') as file_obj:
        file = file_obj.read()

    return file

def load_web_resource(request, resource):
    file = load_file('website/' + resource)
    extension = resource.split(".")[-1]

    if extension == "png":
        return HttpResponse(file, content_type="image/png")
    elif extension == "jpg":
        return HttpResponse(file,content_type="image/jpg")
    elif extension == "svg":
        return HttpResponse(file,content_type="image/svg")
    elif extension == "css":
        return HttpResponse(file,content_type="text/css")

    return HttpResponse(file)

@api_view(['GET'])
def web_resource(request, resource):
    return load_web_resource(request, resource)

@api_view(['GET'])
def get_home(request):
    return load_web_resource(request, "index.html")

@api_view(['GET'])
def get_search(request):
    return load_web_resource(request, "search.html")