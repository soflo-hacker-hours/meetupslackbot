import os
import json
import urllib

from boto3 import resource
from urllib.parse import parse_qsl

slack_hook = os.environ['SLACKWEBHOOKURL']

def deep_get(fnc, *args, fail=False):
    if not fnc:
        return fail
    obj = fnc
    for arg in args:
        if not arg in obj or not obj.__getitem__(arg):
            return fail
        obj = obj.__getitem__(arg)
    return obj

def response(code, body="{}", errors=[], error="", headers={}):
    if len(error):
        errors = [error]
    if len(errors):
        body = json.dumps({"errors": errors})
    return {
        "isBase64Encoded": False,
        "statusCode": code,
        "headers": headers,
        "body": body
    }

def toSlack(message):
    req = urllib.request.Request(slack_hook)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    data = json.dumps({"text": message}).encode("utf8")
    req.add_header('Content-Length', len(data))
    result = urllib.request.urlopen(req, data)

def handle_type(request):
    req_type = request["type"]
    api = {
      'url_verification': lambda x: {"challenge": x["challenge"]}
    }
    return api[req_type](request)
    
def handle_command(request):
    command = request["command"]
    commands = {
        '/meetup': lambda x: x
    }
    return commands[command](request["text"])

def lambda_handler(event, context):
    # Assume body is URL Encoded
    try:
        body = dict(parse_qsl(event["body"]))
    except:
        # Assume body is JSON Encoded
        try:
            body = json.loads(event["body"])
        except:
            # Go with nothing
            body = {}
    try:
        # Assume request has a type
        api_resp = handle_type(body)
        if api_resp:
            return response(200, body=json.dumps(api_resp))
        else:
            return response(200)
    except:
        pass
    try:    
        # Assume request has a command
        api_resp = handle_command(body)
        if api_resp:
            return response(200, body=json.dumps(api_resp))
        else:
            return response(200)
    except:
        # Unknown API type
        toSlack('Could not process: {}'.format(json.dumps(body)))
        return response(200)
