from flask import jsonify

def make_response(payload=None, response_code=200, err_msg=""):
    resp = {
        "status": {
            "code": response_code,
            "errorDetails": err_msg
        }
    }
    if payload:
        resp['payload'] = payload
    return jsonify(resp), response_code