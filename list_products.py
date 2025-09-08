from database.products import get_products

products = get_products()

if products:
    print("Products in DB:")
    for p in products:
        print(p)
else:
    print("❌ No products found in DB")
