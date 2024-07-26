from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import Base, Pokemon, Entrenador, EntrenadorPokemon, Batalla
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokemon.db'
app.secret_key = 'some_secret_key'  # Necesario para usar flash messages
db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
# Index
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_pokemon')
def add_pokemon():
    # Renderiza el formulario para agregar un Pokémon
    pokemones = session.query(Pokemon).all()
    return render_template('add_pokemon.html', pokemones=pokemones)

@app.route('/add_entrenador')
def add_entrenador():
    # Renderiza el formulario para agregar un Entrenador
    entrenadores = session.query(Entrenador).all()
    return render_template('add_entrenador.html', entrenadores=entrenadores)

@app.route('/add_relacion')
def add_relacion():
    entrenadores = session.query(Entrenador).all()
    pokemones = session.query(Pokemon).all()
    relaciones = session.query(EntrenadorPokemon).all()
    return render_template('add_relacion.html', entrenadores=entrenadores, pokemones=pokemones, relaciones=relaciones)

@app.route('/add_batalla', methods=['GET', 'POST'])
def add_batalla():
    if request.method == 'POST':
        entrenador1_id = request.form['entrenador1_id']
        pokemon1_id = request.form['pokemon1_id']
        entrenador2_id = request.form['entrenador2_id']
        pokemon2_id = request.form['pokemon2_id']
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')
        resultado = request.form['resultado']
        # Verificar que los entrenadores sean diferentes
        if entrenador1_id == entrenador2_id:
            flash('Un entrenador no puede batallar contra sí mismo.')
            return redirect(url_for('add_batalla'))
        
        batalla = Batalla(
            entrenador1_id=entrenador1_id,
            pokemon1_id=pokemon1_id,
            entrenador2_id=entrenador2_id,
            pokemon2_id=pokemon2_id,
            fecha=fecha,
            resultado=resultado
        )
        
        session.add(batalla)
        session.commit()
        flash('Batalla agregada exitosamente.')
        return redirect(url_for('add_batalla'))
    
    entrenadores = session.query(Entrenador).all()
    pokemones = session.query(Pokemon).all()
    batallas = session.query(Batalla).all()
    return render_template('add_batalla.html', entrenadores=entrenadores, pokemones=pokemones, batallas=batallas)

@app.route('/pokemon')
def listar_pokemon():
    pokemones = session.query(Pokemon).all()
    return render_template('add_pokemon.html', pokemones=pokemones)
@app.route('/entrenador')
def listar_entrenador():
    entrenadores = session.query(Entrenador).all()
    return render_template('add_entrenador.html', entrenadores=entrenadores)

@app.route('/editar_pokemon/<int:pokemon_id>', methods=['GET', 'POST'])
def editar_pokemon(pokemon_id):
    pokemon = session.query(Pokemon).filter_by(id=pokemon_id).one()
    if request.method == 'POST':
        pokemon.nombre = request.form['nombre']
        pokemon.tipo = request.form['tipo']
        pokemon.habilidad = request.form['habilidad']
        pokemon.ataque = request.form['ataque']
        pokemon.defensa = request.form['defensa']
        pokemon.velocidad = request.form['velocidad']
        pokemon.salud = request.form['salud']
        
        session.add(pokemon)
        session.commit()
        flash('Pokémon editado exitosamente.')
        return redirect(url_for('listar_pokemon'))
    return render_template('editar_pokemon.html', pokemon=pokemon)

@app.route('/guardar_pokemon', methods=['POST','GET'])
def guardar_pokemon():
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo = request.form['tipo']
        habilidad = request.form['habilidad']
        ataque = request.form['ataque']
        defensa = request.form['defensa']
        velocidad = request.form['velocidad']
        salud = request.form['salud']
        # Verificar si el nombre del Pokémon ya existe
        existe_pokemon = session.query(Pokemon).filter_by(nombre=nombre).first()
        if existe_pokemon:
            flash(f'El Pokémon con el nombre {nombre} ya existe.')
            return redirect(url_for('add_pokemon'))
        
        pokemon = Pokemon(
            nombre=nombre,
            tipo=tipo,
            habilidad=habilidad,
            ataque=ataque,
            defensa=defensa,
            velocidad=velocidad,
            salud=salud,)
    
        session.add(pokemon)
        session.commit()
        flash('Pokémon agregado exitosamente.')
        return redirect(url_for('add_pokemon'))
    
@app.route('/editar_entrenador/<int:entrenador_id>', methods=['GET', 'POST'])
def editar_entrenador(entrenador_id):
    entrenador = session.query(Entrenador).filter_by(id=entrenador_id).one()
    if request.method == 'POST':
        entrenador.nombre = request.form['nombre']
        entrenador.edad = request.form['edad']
        entrenador.ciudad_origen = request.form['ciudad_origen']
        entrenador.rango = request.form['rango']
                
        session.add(entrenador)
        session.commit()
        flash('Entrenador editado exitosamente.')
        return redirect(url_for('listar_entrenador'))
    return render_template('editar_entrenador.html', entrenador=entrenador)

@app.route('/guardar_entrenador', methods=['POST','GET'])
def guardar_entrenador():
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        ciudad_origen = request.form['ciudad_origen']
        rango = request.form['rango']
        # Verificar si el nombre del Entrenador ya existe
        existe_entrenador = session.query(Entrenador).filter_by(nombre=nombre).first()
        if existe_entrenador:
            flash(f'El Entrenador con el nombre {nombre} ya existe.')
            return redirect(url_for('add_entrenador'))
        
        entrenador = Entrenador(
            nombre=nombre,
            edad=edad,
            ciudad_origen=ciudad_origen,
            rango=rango,)
    
        session.add(entrenador)
        session.commit()
        flash('Entrenador agregado exitosamente.')
        return redirect(url_for('add_entrenador'))

@app.route('/guardar_relacion', methods=['POST'])
def guardar_relacion():
    if request.method == 'POST':
        entrenador_id = request.form['entrenador_id']
        pokemon_id = request.form['pokemon_id']
         # Verificar si el pokemon ya fue asignado a un entrenador
        existe_relacion = session.query(EntrenadorPokemon).filter_by(pokemon_id=pokemon_id).first()
        if existe_relacion:
            flash(f'El Pokemon seleccionado ya esta asignado a otro entrenador.')
            return redirect(url_for('add_relacion'))
        relacion = EntrenadorPokemon(entrenador_id=entrenador_id, pokemon_id=pokemon_id)
        session.add(relacion)
        session.commit()
        flash('Relación Entrenador-Pokémon agregada exitosamente.')
        return redirect(url_for('add_relacion'))

@app.route('/editar_relacion/<int:relacion_id>', methods=['GET', 'POST'])
def editar_relacion(relacion_id):
    relacion = session.query(EntrenadorPokemon).filter_by(id=relacion_id).one()
    if request.method == 'POST':
        relacion.entrenador_id = request.form['entrenador_id']
        relacion.pokemon_id = request.form['pokemon_id']
        session.add(relacion)
        session.commit()
        flash('Relación Entrenador-Pokémon editada exitosamente.')
        return redirect(url_for('add_relacion'))
    
    entrenadores = session.query(Entrenador).all()
    pokemones = session.query(Pokemon).all()
    return render_template('editar_relacion.html', relacion=relacion, entrenadores=entrenadores, pokemones=pokemones)

@app.route('/borrar_pokemon/<int:pokemon_id>', methods=['POST'])
def borrar_pokemon(pokemon_id):
    pokemon = session.query(Pokemon).filter_by(id=pokemon_id).first()
    if pokemon:
        # Eliminar referencias en EntrenadorPokemon
        session.query(EntrenadorPokemon).filter_by(pokemon_id=pokemon_id).delete()
        # Eliminar referencias en Batalla
        session.query(Batalla).filter((Batalla.pokemon1_id == pokemon_id) | (Batalla.pokemon2_id == pokemon_id)).delete()
        # Eliminar el Pokémon
        session.delete(pokemon)
        session.commit()
        flash('Pokémon eliminado exitosamente.')
    else:
        flash('Pokémon no encontrado.')
    return redirect(url_for('listar_pokemon'))

@app.route('/borrar_entrenador/<int:entrenador_id>', methods=['POST'])
def borrar_entrenador(entrenador_id):
    entrenador = session.query(Entrenador).filter_by(id=entrenador_id).first()
    if entrenador:
        # Eliminar referencias en EntrenadorPokemon
        session.query(EntrenadorPokemon).filter_by(entrenador_id=entrenador_id).delete()
        # Eliminar referencias en Batalla
        session.query(Batalla).filter((Batalla.entrenador1_id == entrenador_id) | (Batalla.entrenador2_id == entrenador_id)).delete()
        # Eliminar el Entrenador
        session.delete(entrenador)
        session.commit()
        flash('Entrenador eliminado exitosamente.')
    else:
        flash('Entrenador no encontrado.')
    return redirect(url_for('listar_entrenador'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=9000, debug=True)