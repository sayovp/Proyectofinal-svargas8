from flask import  Flask, request,render_template,redirect, url_for , jsonify
from flask_restful import Api
from flask_login import LoginManager, login_required, login_user, current_user
from app import app
from models.heladeria import Heladeria, Productos, Ingredientes
from models.usuarios import Usuarios


login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    usuario = Usuarios.query.get(id)
    if usuario:
        return usuario
    return None

'''
Este listar productos es mas relacionado con el proyecto 2.
Maneja un metodo Get.
De acuerdo al enunciado no requiere autenticación y/o validar rol.
Usa el modelo de la Heladeria para traer la lista de productos y renderizar en web 
'''
@app.route("/ListarProductos")
def main():
    heladeria = Heladeria()
    productos = heladeria.productos
    return render_template("index.html", productos = productos)

'''
Este vender es mas relacionado con el proyecto 2.
Maneja un metodo Get.
De acuerdo al enunciado requiere autenticación pero no validar rol.
Usa el modelo de la Heladeria para hacer uso del metodo de vender retornando si fue una venta exitosa o 
falto algun ingrediente. para luego renderizar en el HTML de venta 
'''
@login_required
@app.route("/vender/<idproductos>")
def confir(idproductos):
    if current_user.is_authenticated:
        heladeria = Heladeria()
        resultado = heladeria.vender(idproductos)
        print(resultado)
        return render_template("venta.html", resultado = resultado)
    else:
        return render_template("venta.html", resultado = "no autorizado")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form['nombreusuario']
        password = request.form['contrasena']
        print(username)
        user = Usuarios.query.filter_by(username = username, password = password).first()
        
        if user:
            print(user.username)
            print(user.es_admin)
            login_user(user)
            print(user.es_admin)
            return redirect(url_for("main"))
            '''if user.es_admin:
                print("entre")
                return redirect(url_for("perrocontroller"))
            else:
                return redirect(url_for("home"))'''
    return render_template("login.html")


'''
Esta ruta creada lista los productos segun la informacion suministrada.
De acuerdo al enunciado no requiere autenticación y/o validar rol.
Maneja un metodo Get.
- Al colocar un + trae todos los productos en el sistema.
- Al colocar un numero consulta si ese idproducto existe en la bd y de acuerto traer la informacion
- Al colocar un texto busca los productos relacionados con ese texto.
Usa el modelo de la Heladeria para traer los productos.
para este caso la devolución de resultados se realiza por Json
'''
@app.route("/productos/<producto>")
def productos(producto):
    heladeria = Heladeria()
    productos = heladeria.productos
    productos_json = []
    print(producto)
    print(producto.isdigit())
    if producto=='+':
        for producto in productos:
            productos_json.append(producto.dict_productos())
    
        return jsonify({"productos": productos_json})
    elif producto.isdigit(): 
        print(producto)
        productoQ = Productos.query.get(producto)
        print(productoQ.nombreProducto)
        if not productoQ:
            return jsonify({"error": "Producto no encontrado"}), 404
        productos_json.append(productoQ.dict_productos())
        return jsonify({"productos": productos_json})
    else: 
        productos = Productos.query.filter(Productos.nombreProducto.like(f"%{producto}%")).all()
        if not productos:
            return jsonify({"error": "Producto no encontrado"}), 404
        for producto in productos:
            productos_json.append(producto.dict_productos())
        return jsonify({"productos": productos_json})


'''
Esta ruta consulta la calorias de los productos.
De acuerdo al enunciado si requiere autenticación.
Maneja un metodo Get.
Usa el modelo de la Heladeria el cual esta relacionado con el modeolo de Productos.
tiene un entrada en el cual se valida que sea numerica
genera un Json con el nombre del producto y la cantidad de calorías, 
o un error si el producto no se encuentra o el usuario no está autenticado.
'''
@login_required
@app.route("/productosCalorias/<producto>")
def productosCalorias(producto):
    if current_user.is_authenticated:
        if producto.isdigit():
            productoQ = Productos.query.get(producto)
            if not productoQ:
                return jsonify({"error": "Producto no encontrado"}), 404
            calorias = productoQ.calcular_calorias()
            return jsonify({"producto": productoQ.nombreProducto, "Calorias":calorias})
        else:
            return jsonify({"error": "No corresponde a un Id numerico entero"})
    else:
        return jsonify({"error": "El usuario no esta autenticado"}),401

'''
Esta ruta consulta la rentabilidad de un producto.
De acuerdo al enunciado si requiere autenticación y que tenga rol admin.
Maneja un metodo Get.
Usa el modelo de la Heladeria el cual esta relacionado con el modeolo de Productos.
tiene un entrada en el cual se valida que sea numerica
genera un Json con el nombre del producto y la rentabilidad de este, 
o un error si el producto no se encuentra o el usuario no está autenticado.
'''
@login_required
@app.route("/productosRentable/<producto>")
def productosRentable(producto):
    if current_user.is_authenticated:
        if current_user.es_admin:
                if producto.isdigit():
                    productoQ = Productos.query.get(producto)
                    if not productoQ:
                        return jsonify({"error": "Producto no encontrado"}), 404
                    rentabilidad = productoQ.calcular_rentabilidad()
                    return jsonify({"producto": productoQ.nombreProducto, "Rentabilidad":rentabilidad})
                else:
                     return jsonify({"error": "No corresponde a un Id numerico entero"})
        else:
            return jsonify({"error": "El usuario no tiene permiso"})
    else:
        return jsonify({"error": "El usuario no esta autenticado"}),401

'''
Esta ruta consulta el costo de un producto.
De acuerdo al enunciado si requiere autenticación y que tenga rol admin o emppleado.
Maneja un metodo Get.
Usa el modelo de la Heladeria el cual esta relacionado con el modeolo de Productos.
tiene un entrada en el cual se valida que sea numerica
genera un Json con el nombre del producto y el costo de este, 
o un error si el producto no se encuentra o el usuario no está autenticado.
'''
@login_required
@app.route("/productosCosto/<producto>")
def productosCosto(producto):
    if current_user.is_authenticated:
        if current_user.es_admin or current_user.es_empleado:
            if producto.isdigit():
                productoQ = Productos.query.get(producto)
                if not productoQ:
                    return jsonify({"error": "Producto no encontrado"}), 404
                costo = productoQ.calcular_costo()
                return jsonify({"producto": productoQ.nombreProducto, "Costo":costo})
            else:
                return jsonify({"error": "No corresponde a un Id numerico entero"})
        else:
            return jsonify({"error": "El usuario no tiene permiso"})
    else:
        return jsonify({"error": "El usuario no esta autenticado"}),401    

'''
Esta ruta ejecuta el metodo vender.
Maneja un metodo Get.
De acuerdo al enunciado requiere autenticación pero no validar rol.
tiene un entrada en el cual se valida que sea numerica
genera un Json con el resultado de la venta exitosa, si falta un ingrediente, 
o un error si el producto no se encuentra o el usuario no está autenticado.
'''
@login_required
@app.route("/venderJ/<idproductos>")
def vender(idproductos):
    if current_user.is_authenticated:
        if idproductos.isdigit():
            heladeria = Heladeria()
            resultado = heladeria.vender(idproductos)
            print(resultado)
            return jsonify({"resultado_venta": f"{resultado}"})
        else:
            return jsonify({"error": "No corresponde a un Id numerico entero"})
    else :
        return jsonify({"error": "Usuario no autenticado"})

'''
Esta ruta creada lista los ingredientes segun la informacion suministrada.
De acuerdo al enunciado si requiere autenticación y validar rol de admin y empleado.
Maneja un metodo Get.
- Al colocar un + trae todos los ingredientes en el sistema.
- Al colocar un numero consulta si ese idingredientes existe en la bd y de acuerto traer la informacion
- Al colocar un texto busca los ingredientes relacionados con ese texto.
Usa el modelo de la Heladeria para traer los ingredientes.
para este caso la devolución de resultados se realiza por Json
'''
@login_required
@app.route("/ingredientes/<ingrediente>")
def ingredientes(ingrediente):
    if current_user.is_authenticated:
        if current_user.es_admin or current_user.es_empleado:
            ingredientes_json = []
            print(ingrediente)
            print(ingrediente.isdigit())
            if ingrediente=='+':
                heladeria = Heladeria()
                ingredientes = heladeria.ingredientes
                for ingrediente in ingredientes:
                    ingredientes_json.append(ingrediente.dict_ingredientes())
            
                return jsonify({"Ingredientes": ingredientes_json})
            elif ingrediente.isdigit(): 
                print(ingrediente)
                ingredienteQ = Ingredientes.query.get(ingrediente)
                #print(ingredienteQ.nombreProducto)
                if not ingredienteQ:
                    return jsonify({"error": "Ingrediente no encontrado"}), 404
                ingredientes_json.append(ingredienteQ.dict_ingredientes())
                return jsonify({"Ingredientes": ingredientes_json})
            else: 
                ingredienteQ = Ingredientes.query.filter(Ingredientes.nombreIngrediente.like(f"%{ingrediente}%")).all()
                if not ingredienteQ:
                    return jsonify({"error": "Ingrediente no encontrado"}), 404
                for ingrediente in ingredienteQ:
                    ingredientes_json.append(ingrediente.dict_ingredientes())
                return jsonify({"Ingredientes": ingredientes_json})
        else:
            return jsonify({"error": "No corresponde a un Id numerico entero"})
    else :
        return jsonify({"error": "Usuario no autenticado"})

'''
Esta ruta consulta si un ingrediente es sano.
De acuerdo al enunciado requiere autenticación y si tiene rol de admin o empleado.
Maneja un metodo Get.
Usa el modelo de la Heladeria el cual esta relacionado con el modelo de ingredientes.
tiene un entrada en el cual se valida que sea numerica
genera un Json con el nombre del producto y si es sano el producto, 
o un error si el ingrediente no se encuentra o el usuario no está autenticado.
'''    
@login_required
@app.route("/ingredienteSano/<ingrediente>")
def ingredienteSano(ingrediente):
    if current_user.is_authenticated:
        if current_user.es_admin or current_user.es_empleado:
            if ingrediente.isdigit():
                ingredienteQ = Ingredientes.query.get(ingrediente)
                if not ingredienteQ:
                    return jsonify({"error": "Producto no encontrado"}), 404
                sano = ingredienteQ.ingredientesano()
                return jsonify({"producto": ingredienteQ.nombreIngrediente, "Es_Sano":sano})
            else:
                return jsonify({"error": "No corresponde a un Id numerico entero"})
        else:
            return jsonify({"error": "No corresponde a un Id numerico entero"})
    else :
        return jsonify({"error": "Usuario no autenticado"})

'''
Esta ruta ejecuta el pmetodo de abastecer para ingresar nuevo inventario a un ingrediente.
De acuerdo al enunciado requiere autenticación y si tiene rol de admin o empleado.
Maneja un metodo Get.
Usa el modelo de la Heladeria el cual esta relacionado con el modelo de ingredientes.
tiene un entrada en el cual se valida que sea numerica
genera un Json con el nombre del ingrediente, inventario antiguo e inventario nuevo, 
o un error si el ingrediente no se encuentra o el usuario no está autenticado o no tienen permiosos.
'''
@login_required
@app.route("/ingredienteAbastecer/<ingrediente>")
def ingredienteAbastecer(ingrediente):
    if current_user.is_authenticated:
        if current_user.es_admin or current_user.es_empleado:
            if ingrediente.isdigit():
                ingredienteQ = Ingredientes.query.get(ingrediente)
                if not ingredienteQ:
                    return jsonify({"error": "Producto no encontrado"}), 404
                print (ingredienteQ.inventario)
                inventarioAntiguo = ingredienteQ.inventario
                ingredienteQ.abastecer()
                print(ingredienteQ.inventario)
                inventarioNuevo = ingredienteQ.inventario
                return jsonify({"producto": ingredienteQ.nombreIngrediente, "inventario anterior":inventarioAntiguo, "inventario nuevo":inventarioNuevo})
            else:
                return jsonify({"error": "No corresponde a un Id numerico entero"})
        else:
                return jsonify({"error": "Usuarui no tiene permisos"})
    else :
        return jsonify({"error": "Usuario no autenticado"})

'''
Esta ruta ejecuta el metodo de renovar para dejar en 0 un ingrediente.
De acuerdo al enunciado requiere autenticación y si tiene rol de admin o empleado.
Maneja un metodo Get.
Usa el modelo de la Heladeria el cual esta relacionado con el modelo de ingredientes.
tiene un entrada en el cual se valida que sea numerica
genera un Json con el nombre del ingrediente, inventario antiguo e inventario nuevo, 
o un error si el ingrediente no se encuentra o el usuario no está autenticado o no tienen permiosos.
'''
@login_required
@app.route("/ingredienteRenovar/<ingrediente>")
def ingredienteRenovar(ingrediente):
    if current_user.is_authenticated:
        if current_user.es_admin or current_user.es_empleado:
            if ingrediente.isdigit():
                ingredienteQ = Ingredientes.query.get(ingrediente)
                if not ingredienteQ:
                    return jsonify({"error": "Producto no encontrado"}), 404
                print (ingredienteQ.inventario)
                inventarioAntiguo = ingredienteQ.inventario
                ingredienteQ.renovar_inentario()
                print(ingredienteQ.inventario)
                inventarioNuevo = ingredienteQ.inventario
                if (inventarioAntiguo == inventarioNuevo):
                    return jsonify({"error": "El ingrediente es una Base, del cual el inventario no puede quedar en 0"})
                else:
                    return jsonify({"producto": ingredienteQ.nombreIngrediente, "inventario anterior":inventarioAntiguo, "inventario nuevo":inventarioNuevo})
            else:
                return jsonify({"error": "No corresponde a un Id numerico entero"})
        else:
            return jsonify({"error": "No corresponde a un Id numerico entero"})
    else :
        return jsonify({"error": "Usuario no autenticado"})