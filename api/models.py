from django.db import models
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime
from django.core import serializers
import math
import json

class GeoLocation(models.Model):
    latitude  = models.FloatField()
    longitude = models.FloatField()

# An alert of a disaster of some kind generated from a social media post
class MediaAlert(models.Model):
    # Required fields
    source_type       = models.CharField(max_length=255)
    url               = models.URLField()
    disaster_type     = models.CharField(max_length=255) # cannot be blank: label 'unknown' if not known

    # Optional fields (not guarunteed to exist)
    date_created      = models.DateTimeField(blank=True)
    location_name     = models.CharField(max_length=255, blank=True)
    country           = models.CharField(max_length=255, blank=True)
    geo_location      = models.OneToOneField(GeoLocation, on_delete=models.SET_NULL, blank=True,
                                             related_name='geo_location', null=True)
    disaster_severity = models.CharField(max_length=255, blank=True) # low, medium, high -- we ignore 'none' as best we can
    tags              = models.TextField(blank=True)

# Custom exception type so we can return parsing errors to user
class SyntaxException(Exception):
    pass

class SearchTree:
    OPERATORS  = ["and", "or", "not"]
    PARAMETERS = ["source_type", "url", "disaster_type", "date_created", "location_name", "country", "geo_location",
                  "disaster_severity", "tags"]
    ARGUMENTS  = ["matches", "contains", "within", "precision"]

    def __init__(self, search_query):
        self.root = self.__init_tree(search_query)

    # Returns a 'Q' object that enables the query requested
    # Takes in a dict, search_query
    def __init_tree(self, search_query):
        # Check if we're a parent node
        if "queries" in search_query:
            # Make sure we have a valid 'operator' keyword
            if "operator" not in search_query:
                raise SyntaxException("no operator in parent node")
            operator = search_query["operator"]
            if operator not in self.OPERATORS:
                raise SyntaxException(operator + " not an operator")

            # Handle child searches. Each one is a 'Q' object make from child nodes in dict
            child_searches = []
            for sub_search in search_query["queries"]:
                child_searches.append(self.__init_tree(sub_search))

            if len(child_searches) == 0:
                raise SyntaxException("no child searches in parent node")

            # Verify special syntax for 'not' operator
            if operator == "not" and len(child_searches) > 1:
                raise SyntaxException("'not' operator can only have one child")

            # Compose query of Q objects
            query = child_searches.pop()
            if operator == "and":
                while(len(child_searches) > 0):
                    query = query & child_searches.pop()
            elif operator == "or":
                while (len(child_searches) > 0):
                    query = query | child_searches.pop()
            elif operator == "not":
                return ~query
            else:
                raise SyntaxException("PANIC SHOULDN'T BE HERE PARENT NODE")

            return query

        # Else in child node
        # Verify syntax for child node
        if len(search_query.keys()) > 1:
            raise SyntaxException("Malformed child node: can only have one parameter")
        if len(search_query.keys()) == 0:
            raise SyntaxException("Child node has no members")
        if list(search_query.keys())[0] not in self.PARAMETERS:
            raise SyntaxException("Child node parameter not valid")

        parameter  = list(search_query.keys())[0]
        param_args = search_query[parameter]
        if type(param_args) is not dict:
            raise SyntaxException("parameter '" + parameter + "' arguments are not a seperate JSON object")

        if len(list(param_args.keys())) == 0:
            raise SyntaxException("Child parameter has no arguments")

        if   parameter == "source_type":
            if "matches" not in param_args:
                raise SyntaxException("No 'matches' argument in 'source_type' parameter")
            matches_val = param_args["matches"]
            if "operator" in param_args:
                operator = param_args["operator"]
                if operator not in self.OPERATORS:
                    raise SyntaxException("invalid oeprator " + operator + " in 'source_type'")

                if type(matches_val) is not list:
                    raise SyntaxException("'matches' is not a list in 'source_type' parameter with operator")

                # Handle 'not' operater speratly bcause it can only have one child
                if operator == "not":
                    if len(matches_val) != 1:
                        raise SyntaxException("error in 'source_type' child node: 'not' operator used with more than one value")
                    return ~Q(source_type__iexact=matches_val[0])

                # Handle other operators
                query = Q(source_type__iexact=matches_val[0])
                for i in range (1, len(matches_val)):
                    if operator == "and":
                        query = query & Q(source_type__iexact=matches_val[i])
                    elif operator == "or":
                        query = query | Q(source_type__iexact=matches_val[i])
                return query
            else:
                if type(matches_val) is list:
                    raise SyntaxException("'matches' is a list in 'source_type' parameter without operator")
                return Q(source_type__iexact=matches_val)
        elif parameter == "url":
            if "matches" not in param_args:
                raise SyntaxException("No 'matches' argument in 'url' parameter")
            matches_val = param_args["matches"]
            if "operator" in param_args:
                operator = param_args["operator"]
                if operator not in self.OPERATORS:
                    raise SyntaxException("invalid operator " + operator + " in 'url'")

                if type(matches_val) is not list:
                    raise SyntaxException("'matches' is not a list in 'url' parameter with operator")

                # Handle 'not' operater speratly bcause it can only have one child
                if operator == "not":
                    if len(matches_val) != 1:
                        raise SyntaxException(
                            "error in 'url' child node: 'not' operator used with more than one value")
                    return ~Q(url=matches_val[0])

                # Handle other operators
                query = Q(url=matches_val[0])
                for i in range(1, len(matches_val)):
                    if operator == "and":
                        query = query & Q(url=matches_val[i])
                    elif operator == "or":
                        query = query | Q(url=matches_val[i])
                return query
            else:
                if type(matches_val) is list:
                    raise SyntaxException("'matches' is a list in 'url' parameter without operator")
                return Q(url=matches_val)
        elif parameter == "disaster_type":
            if "matches" not in param_args:
                raise SyntaxException("No 'matches' argument in 'disaster_type' parameter")
            matches_val = param_args["matches"]
            if "operator" in param_args:
                operator = param_args["operator"]
                if operator not in self.OPERATORS:
                    raise SyntaxException("invalid operator " + operator + " in 'disaster_type'")

                if type(matches_val) is not list:
                    raise SyntaxException("'matches' is not a list in 'disaster_type' parameter with operator")

                # Handle 'not' operater speratly bcause it can only have one child
                if operator == "not":
                    if len(matches_val) != 1:
                        raise SyntaxException(
                            "error in 'disaster_type' child node: 'not' operator used with more than one value")
                    return ~Q(disaster_type__iexact=matches_val[0])

                # Handle other operators
                query = Q(disaster_type__iexact=matches_val[0])
                for i in range(1, len(matches_val)):
                    if operator == "and":
                        query = query & Q(disaster_type__iexact=matches_val[i])
                    elif operator == "or":
                        query = query | Q(disaster_type__iexact=matches_val[i])
                return query
            else:
                if type(matches_val) is list:
                    raise SyntaxException("'matches' is a list in 'disaster_type' parameter without operator")
                return Q(disaster_type__iexact=matches_val)
        elif parameter == "date_created":
            arg = "matches"
            if arg not in param_args:
                raise SyntaxException("No 'matches' or 'within' argument in 'date_created' parameter")
            matches_val = param_args[arg]
            if "operator" in param_args:
                operator = param_args["operator"]

                # Ensure the operator is valid
                if operator not in self.OPERATORS:
                    raise SyntaxException("invalid operator " + operator + " in 'date_created'")

                if type(matches_val) is not list:
                    raise SyntaxException("'" + arg + "' is not a list in 'date_created' parameter with operator")

                # Handle 'not' operater speratly bcause it can only have one child
                if operator == "not":
                    if len(matches_val) != 1:
                        raise SyntaxException(
                            "error in 'location_name' child node: 'not' operator used with more than one value")
                    return ~Q(location_name=matches_val[0]) if arg == "matches" else ~Q(
                        location_name__icontains=matches_val[0])

                # Handle other operators
                dt = datetime.strptime(matches_val[0], '%Y-%m-%d')
                query = Q(date_created_day=dt.day, date_created_month=dt.month, date_created_year=dt.year)
                for i in range(1, len(matches_val)):
                    dt = datetime.strptime(matches_val[i], '%Y-%m-%d')
                    q = Q(date_created_day=dt.day, date_created_month=dt.month, date_created_year=dt.year)
                    if operator == "and":
                        query = query & q
                    elif operator == "or":
                        query = query | q
                return query
            else:
                if type(matches_val) is list:
                    raise SyntaxException("'" + arg + "' is a list in 'location_name' parameter without operator")

                dt = datetime.strptime(matches_val, '%Y-%m-%d')
                return Q(date_created_day=dt.day, date_created_month=dt.month, date_created_year=dt.year)
        elif parameter == "location_name":
            arg = "matches"
            if arg not in param_args:
                arg = "contains"
                if arg not in param_args:
                    raise SyntaxException("No 'matches' or 'contains' argument in 'location_name' parameter")
            matches_val = param_args[arg]
            if "operator" in param_args:
                operator = param_args["operator"]
                if operator not in self.OPERATORS:
                    raise SyntaxException("invalid operator " + operator + " in 'location_name'")

                if type(matches_val) is not list:
                    raise SyntaxException("'" + arg + "' is not a list in 'location_name' parameter with operator")

                # Handle 'not' operater speratly bcause it can only have one child
                if operator == "not":
                    if len(matches_val) != 1:
                        raise SyntaxException(
                            "error in 'location_name' child node: 'not' operator used with more than one value")
                    return ~Q(location_name=matches_val[0]) if arg == "matches" else ~Q(location_name__icontains=matches_val[0])

                # Handle other operators
                query = (Q(location_name=matches_val[0]) if arg == "matches" else Q(location_name__icontains=matches_val[0]))
                for i in range(1, len(matches_val)):
                    if operator == "and":
                        if arg == "matches":
                            query = query & Q(location_name=matches_val[i])
                        else:
                            query = query & Q(location_name__icontains=matches_val[i])
                    elif operator == "or":
                        if arg == "matches":
                            query = query | Q(location_name=matches_val[i])
                        else:
                            query = query | Q(location_name__icontains=matches_val[i])
                return query
            else:
                if type(matches_val) is list:
                    raise SyntaxException("'" + arg + "' is a list in 'location_name' parameter without operator")
                return Q(location_name=matches_val) if arg == "matches" else Q(location_name__icontains=matches_val)
        elif parameter == "country":
            if "matches" not in param_args:
                raise SyntaxException("No 'matches' argument in 'country' parameter")
            matches_val = param_args["matches"]
            if "operator" in param_args:
                operator = param_args["operator"]
                if operator not in self.OPERATORS:
                    raise SyntaxException("invalid operator " + operator + " in 'country'")

                if type(matches_val) is not list:
                    raise SyntaxException("'matches' is not a list in 'country' parameter with operator")

                # Handle 'not' operater speratly bcause it can only have one child
                if operator == "not":
                    if len(matches_val) != 1:
                        raise SyntaxException(
                            "error in 'country' child node: 'not' operator used with more than one value")
                    return ~Q(country=matches_val[0])

                # Handle other operators
                query = Q(country=matches_val[0])
                for i in range(1, len(matches_val)):
                    if operator == "and":
                        query = query & Q(country=matches_val[i])
                    elif operator == "or":
                        query = query | Q(country=matches_val[i])
                return query
            else:
                if type(matches_val) is list:
                    raise SyntaxException("'matches' is a list in 'country' parameter without operator")
                return Q(country=matches_val)
        elif parameter == "geo_location":
            # for geolocation, use geo_location_latitude > ...
            if "precision" not in param_args:
                raise SyntaxException("No 'precision' argument in 'geo_location' parameter")
            precision = param_args["precision"]
            if "matches" not in param_args:
                raise SyntaxException("No 'matches' argument in 'geo_location' parameter")
            matches_val = param_args["matches"]
            if "operator" in param_args:
                operator = param_args["operator"]
                if operator not in self.OPERATORS:
                    raise SyntaxException("invalid oeprator " + operator + " in 'geo_location'")

                if type(matches_val) is not list:
                    raise SyntaxException("'matches' is not a list in 'geo_location' parameter with operator")

                if type(matches_val[0]) is not tuple or type(matches_val[0][0]) is not float:
                    raise SyntaxException("values of GPS points in 'geo_location' invalid")

                # Handle 'not' operater speratly bcause it can only have one child
                if operator == "not":
                    if len(matches_val) != 1:
                        raise SyntaxException("error in 'source_type' child node: 'not' operator used with more than one value")
                    latitude = matches_val[0][0]
                    longitude = matches_val[0][1]

                    latitude_floor = math.floor(latitude * 10 ** (precision - 1)) / (10 ** (precision - 1))
                    latitude_ceil = math.ceil(latitude * 10 ** (precision - 1)) / (10 ** (precision - 1))

                    longitude_floor = math.floor(longitude * 10 ** (precision - 1)) / (10 ** (precision - 1))
                    longitude_ceil = math.ceil(longitude * 10 ** (precision - 1)) / (10 ** (precision - 1))

                    query = Q(geo_location_latitude_gte=latitude_floor) & Q(geo_location_latitude_lte=latitude_ceil) & \
                            Q(geo_location_longitude_gte=longitude_floor) & Q(geo_location_longitude_lte=longitude_ceil)
                    return ~query

                # Handle other operators
                latitude = matches_val[0][0]
                longitude = matches_val[0][1]

                latitude_floor = math.floor(latitude * 10 ** (precision - 1)) / (10 ** (precision - 1))
                latitude_ceil = math.ceil(latitude * 10 ** (precision - 1)) / (10 ** (precision - 1))

                longitude_floor = math.floor(longitude * 10 ** (precision - 1)) / (10 ** (precision - 1))
                longitude_ceil = math.ceil(longitude * 10 ** (precision - 1)) / (10 ** (precision - 1))
                query = Q(geo_location__latitude__gte=latitude_floor) & Q(geo_location__latitude_lte=latitude_ceil) &\
                       Q(geo_location__longitude__gte=longitude_floor) & Q(geo_location__longitude_lte=longitude_ceil)
                for i in range (1, len(matches_val)):
                    latitude = matches_val[i][0]
                    longitude = matches_val[i][1]

                    latitude_floor = math.floor(latitude * 10 ** (precision - 1)) / (10 ** (precision - 1))
                    latitude_ceil = math.ceil(latitude * 10 ** (precision - 1)) / (10 ** (precision - 1))

                    longitude_floor = math.floor(longitude * 10 ** (precision - 1)) / (10 ** (precision - 1))
                    longitude_ceil = math.ceil(longitude * 10 ** (precision - 1)) / (10 ** (precision - 1))

                    q = Q(geo_location__latitude__gte=latitude_floor) & Q(geo_location__latitude__lte=latitude_ceil) &\
                       Q(geo_location__longitude__gte=longitude_floor) & Q(geo_location__longitude__lte=longitude_ceil)
                    if operator == "and":
                        query = query & q
                    elif operator == "or":
                        query = query | q
                return query
            else:
                if type(matches_val) is not list:
                    raise SyntaxException("latitude and longitude in 'geo_location' must be in a list")
                if type(matches_val[0]) is not float and type(matches_val[0]) is not int:
                    raise SyntaxException("values of GPS points in 'geo_location' must be floats")
                if len(matches_val) is not 2:
                    raise SyntaxException("must be two values for GPS point in 'geo_location'")

                latitude  = matches_val[0]
                longitude = matches_val[1]

                latitude_floor  = math.floor(latitude * 10**(precision - 1)) / (10**(precision - 1))
                latitude_ceil = math.ceil(latitude * 10 ** (precision - 1)) / (10 ** (precision - 1))

                longitude_floor = math.floor(longitude * 10 ** (precision - 1)) / (10 ** (precision - 1))
                longitude_ceil  = math.ceil(longitude * 10 ** (precision - 1)) / (10 ** (precision - 1))
                return Q(geo_location__latitude__gte=latitude_floor) & Q(geo_location__latitude__lte=latitude_ceil) &\
                       Q(geo_location__longitude__gte=longitude_floor) & Q(geo_location__longitude__lte=longitude_ceil)
        elif parameter == "disaster_severity":
            if "matches" not in param_args:
                raise SyntaxException("No 'matches' argument in 'disaster_severity' parameter")
            matches_val = param_args["matches"]
            if "operator" in param_args:
                operator = param_args["operator"]
                if operator not in self.OPERATORS:
                    raise SyntaxException("invalid operator " + operator + " in 'disaster_severity'")

                if type(matches_val) is not list:
                    raise SyntaxException("'matches' is not a list in 'disaster_severity' parameter with operator")

                # Handle 'not' operater speratly bcause it can only have one child
                if operator == "not":
                    if len(matches_val) != 1:
                        raise SyntaxException("error in 'disaster_severity' child node: 'not' operator used with more than one value")
                    return ~Q(disaster_severity=matches_val[0])

                # Handle other operators
                query = Q(disaster_severity=matches_val[0])
                for i in range(1, len(matches_val)):
                    if operator == "and":
                        query = query & Q(disaster_severity=matches_val[i])
                    elif operator == "or":
                        query = query | Q(disaster_severity=matches_val[i])
                return query
            else:
                if type(matches_val) is list:
                    raise SyntaxException("'matches' is a list in 'disaster_severity' parameter without operator")
                return Q(disaster_severity=matches_val)
        elif parameter == "tags":
            arg = "matches"
            if arg not in param_args:
                arg = "contains"
                if arg not in param_args:
                    raise SyntaxException("No 'matches' or 'contains' argument in 'tags' parameter")
            matches_val = param_args[arg]
            if "operator" in param_args:
                operator = param_args["operator"]
                if operator not in self.OPERATORS:
                    raise SyntaxException("invalid operator " + operator + " in 'tags'")

                if type(matches_val) is not list:
                    raise SyntaxException("'" + arg + "' is not a list in 'tags' parameter with operator")

                # Handle 'not' operater speratly bcause it can only have one child
                if operator == "not":
                    if len(matches_val) != 1:
                        raise SyntaxException(
                            "error in 'tags' child node: 'not' operator used with more than one value")
                    return ~Q(tags=matches_val[0]) if arg == "matches" else ~Q(tags__icontains=matches_val[0])

                # Handle other operators
                query = (Q(tags=matches_val[0]) if arg == "matches" else Q(tags__icontains=matches_val[0]))
                for i in range(1, len(matches_val)):
                    if operator == "and":
                        if arg == "matches":
                            query = query & Q(tags=matches_val[i])
                        else:
                            query = query & Q(tags__icontains=matches_val[i])
                    elif operator == "or":
                        if arg == "matches":
                            query = query | Q(tags=matches_val[i])
                        else:
                            query = query | Q(tags__icontains=matches_val[i])
                return query
            else:
                if type(matches_val) is list:
                    raise SyntaxException("'" + arg + "' is a list in 'tags' parameter without operator")
                return Q(tags=matches_val) if arg == "matches" else Q(tags__icontains=matches_val)
        else:
            raise SyntaxException("PANIC SHOULDN'T BE HERE CHILD NODE")

def get_search_from_json(search_query):
    search = SearchTree(search_query)
    return search.root

def handle_search_from_json(search_query):
    try:
        search = SearchTree(search_query)

        try:
            result = MediaAlert.objects.filter(search.root)

            list_result = list(result.values())
            for result in list_result:
                if "geo_location_id" in result:
                    try:
                        geo_model = GeoLocation.objects.get(id=result["geo_location_id"])
                        geo_model_json = serializers.serialize("json", [geo_model])
                        result["geo_location"] = json.loads(geo_model_json)
                        del result["geo_location_id"]
                    except:
                        pass

            dict_result = {}
            for i in range(0, len(list_result)):
                dict_result["model" + str(i)] = list_result[i]
            print(dict_result)
            return Response(dict_result)

        except MediaAlert.DoesNotExist:
            return Response( {} )

    except SyntaxException as e:
        return Response( {"detail" : str(e)} )