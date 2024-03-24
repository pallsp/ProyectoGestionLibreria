import sqlalchemy as db 
import persistence.model as mod

#este módulo creará nuestra base de datos 

engine = db.create_engine('sqlite:///./db/login.db', echo = True, future = True)
mod.Base.metadata.create_all(engine)
