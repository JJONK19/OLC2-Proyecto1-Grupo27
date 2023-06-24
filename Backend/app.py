import os


from flask import Flask, Response, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from Analizador import Analizador
from xml.dom import minidom
import base64
import re
import json


app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type, Access-Control-Allow-Origin'

@app.route("/execute", methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Origin'])
def hello():

    if request.method != "POST":
        return jsonify({
            'status': 405,
            'message': f'Este metodo no esta permitido para este endpoint'
        })


    print(request)
    entrada = request.values["code"]
    print(entrada)

    # --- Recopilar el texto
    print("//////////////////////////////////////////////////")
    print(entrada)
    print("//////////////////////////////////////////////////")

    # --- Analizar cadena
    Interprete = Analizador()
    Salida = Interprete.analizar(entrada)
    # Errores
    for i in Salida.getErrores():
        print(i.descripcion)

    # SImbolos
    a = Salida.getSimbolos()
    for clave, valor in a.items():
        print(clave, ":", valor)
    # Instrucciones
    for i in Salida.instrucciones:
        print(i)

    print("EJECUCION////////////////////////////////////////////")
    Salida.Ejecucion()
    print("EJECUCION////////////////////////////////////////////")

    print("AST//////////////////////////////////////////////////")
    salida_ast = Salida.Grafo()
    print(salida_ast)
    print("AST//////////////////////////////////////////////////")

    dot_file = "arbolast.dot"

    # Escritura del archivo dot
    with open(dot_file, "w") as file:
        file.write(salida_ast)

    #Creacion de la img a partir del archivo dot
    output_image = "arbolast.jpg"

    command = f'dot -Tjpg {dot_file} -o {output_image}  '

    os.system(f'cmd /C "{command}"')

    #Conversión de la img a Base64
    with open(output_image, "rb") as image_file:
        base64_ast = base64.b64encode(image_file.read()).decode('utf-8')

    print("CONSOLA//////////////////////////////////////////////")
    salida_consola = Salida.getConsola()
    print(salida_consola)
    print("CONSOLA//////////////////////////////////////////////")

    r = "ok"

    return jsonify(
        {
        "result": r,
        "salida_consola": salida_consola,
        "base64_ast": base64_ast
        }
    )


@app.route("/c3d", methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Origin'])
def bye():
    if request.method != "POST":
        return jsonify({
            'status': 405,
            'message': f'Este metodo no esta permitido para este endpoint'
        })

    print(request)
    entrada = request.values["code"]
    print(entrada)

    # --- Recopilar el texto
    print("//////////////////////////////////////////////////")
    print(entrada)
    print("//////////////////////////////////////////////////")

    # --- Analizar cadena
    Interprete = Analizador()
    Salida = Interprete.analizar(entrada)
    # Errores
    for i in Salida.getErrores():
        print(i.descripcion)

    # SImbolos
    a = Salida.getSimbolos()
    for clave, valor in a.items():
        print(clave, ":", valor)
    # Instrucciones
    for i in Salida.instrucciones:
        print(i)

    print("AST//////////////////////////////////////////////////")
    salida_ast = Salida.Grafo()
    print(salida_ast)
    print("AST//////////////////////////////////////////////////")

    dot_file = "arbolast.dot"

    # Escritura del archivo dot
    with open(dot_file, "w") as file:
        file.write(salida_ast)

    # Creacion de la img a partir del archivo dot
    output_image = "arbolast.jpg"

    # command = f"{direccionI} {tParam} {test} {direccionArchivo} {tOParam} {direccionImagen}"

    command = f'dot -Tjpg {dot_file} -o {output_image}  '

    os.system(f'cmd /C "{command}"')

    # Conversión de la img a Base64
    with open(output_image, "rb") as image_file:
        base64_ast = base64.b64encode(image_file.read()).decode('utf-8')

    print("EJECUCION////////////////////////////////////////////")
    Salida.Ejecucion()
    print("EJECUCION////////////////////////////////////////////")

    #print("CONSOLA//////////////////////////////////////////////")
    #salida_consola = Salida.getConsola()
    #print(salida_consola)
    #print("CONSOLA//////////////////////////////////////////////")

    print("C3D//////////////////////////////////////////////////")
    salida_c3d = Salida.C3D()
    print(salida_c3d)
    print("C3D//////////////////////////////////////////////////")

    r = "ok"

    return jsonify(
        {
            "result": r,
            "salida_c3d": salida_c3d,
            "base64_ast": base64_ast
        }
    )


if __name__ == "__main__":
    app.run(debug=True)