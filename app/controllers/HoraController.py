from flask import Blueprint, jsonify
from datetime import datetime

hora_bp = Blueprint('hora_bp', __name__)

@hora_bp.route('/hora', methods=['GET'])
def obter_hora():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return jsonify({'hora': now})
