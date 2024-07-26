from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Pokemon(Base):
    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50))
    tipo = Column(String(50))
    habilidad = Column(String(50))
    ataque = Column(Integer)
    defensa = Column(Integer)
    velocidad = Column(Integer)
    salud = Column(Integer)

class Entrenador(Base):
    __tablename__ = 'entrenadores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50))
    edad = Column(Integer)
    ciudad_origen = Column(String(50))
    rango = Column(String(50))
    pokemones = relationship('EntrenadorPokemon', back_populates='entrenador')


class EntrenadorPokemon(Base):
    __tablename__ = 'entrenador_pk'
    id =  Column(Integer, primary_key=True, autoincrement=True)
    entrenador_id = Column(Integer, ForeignKey('entrenadores.id'))
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'))
    entrenador = relationship('Entrenador', back_populates='pokemones')
    pokemon = relationship('Pokemon')


class Batalla(Base):
    __tablename__ = 'batallas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    entrenador1_id = Column(Integer, ForeignKey('entrenadores.id'))
    entrenador2_id = Column(Integer, ForeignKey('entrenadores.id'))
    pokemon1_id = Column(Integer, ForeignKey('pokemon.id'))
    pokemon2_id = Column(Integer, ForeignKey('pokemon.id'))
    fecha = Column(Date)
    resultado = Column(String(50))

    entrenador1 = relationship("Entrenador", foreign_keys=[entrenador1_id])
    entrenador2 = relationship("Entrenador", foreign_keys=[entrenador2_id])
    pokemon1 = relationship("Pokemon", foreign_keys=[pokemon1_id])
    pokemon2 = relationship("Pokemon", foreign_keys=[pokemon2_id])


# Crear la base de datos
engine = create_engine('sqlite:///pokemon.db')
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()
