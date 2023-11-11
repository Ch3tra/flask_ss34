from sqlalchemy import create_engine, text

# Connect to the database
engine = create_engine("mysql+mysqlconnector://root:@localhost/ss34_proo")
# Test the connection
connection = engine.connect()

