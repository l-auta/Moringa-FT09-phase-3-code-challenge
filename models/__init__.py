# In models/__init__.py or another appropriate file
from database.setup import create_tables

# Ensure the tables are created as soon as models are imported
create_tables()
