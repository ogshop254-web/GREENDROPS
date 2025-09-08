from database.db import init_db
from database.products import add_product

init_db()

# Insert test products
add_product("Apple", 50)
add_product("Banana", 30)
add_product("Mango", 80)

print("✅ Test products added to the database.")
