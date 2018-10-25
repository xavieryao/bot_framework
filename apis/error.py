from flask import jsonify

def api_error(err_type, message):
    return jsonify({
        'type': err_type,
        'message': message
    })