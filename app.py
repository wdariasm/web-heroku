from __future__ import print_function
from flask import Flask
from flask_restful import Api
from api_voice import usuario, concurso, grabacion, hifire
from flask_cors import CORS
import os

app = Flask( __name__)
api = Api(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})

"""
@app.route( '/' )
def inicio():
    return render_template( 'index.html' )

@app.route('/home')
def home():
    return render_template( 'index.html' )

@app.route('/login')
def login():
    return render_template( 'index.html' )

@app.route('/registro')
def registro():
    return render_template( 'index.html' )

@app.route('/concurso')
def concurso_master():
    return render_template( 'index.html' )

@app.route('/detalle-voz')
def detalle_voz():
    return render_template( 'index.html' )

@app.route('/mis-concursos')
def mis_concursos():
    return render_template( 'index.html' )

@app.route('/concursar/<string:url>')
def concursar():
    return render_template('index.html')
"""

api.add_resource(usuario.Healthys, '/api/health')
api.add_resource(usuario.Users, '/api/users/')
api.add_resource(concurso.ConcursoList, '/api/concursos/')
api.add_resource(grabacion.Grabacion, '/api/grabaciones/')
api.add_resource(concurso.ConcursoUser, '/api/concursos/user/<user_id>/')
api.add_resource(concurso.ConcursoUrl, '/api/concursos/validar/<string:url>/')
api.add_resource(grabacion.ConcursoGrabacion, '/api/concursos/<string:concurso_id>/grabaciones/<estado>/')
api.add_resource(concurso.Concurso, '/api/concursos/<concurso_id>/')
api.add_resource(usuario.UserLogin, '/api/api-token-auth/')
api.add_resource(grabacion.TestGrabacion, '/api/test/grabacion')
api.add_resource(concurso.ConcursoCache , '/api/concursos/visitados/')
api.add_resource(hifire.HiFire, '/hirefire/<string:hifire_token>/info')

if __name__ == '__main__':
    port = os.environ.get( 'PORT', 5000)
    #app.run(host='0.0.0.0', port=port, debug=True)
    app.run( host='0.0.0.0', port=port )
