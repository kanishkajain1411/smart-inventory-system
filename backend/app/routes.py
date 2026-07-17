from flask import Blueprint, request, jsonify
from .database import db
from sqlalchemy import func
from .models import Category, Product, Supplier, Order ,User
api = Blueprint("api", __name__)


@api.route("/categories", methods=["POST"])
def add_category():

    try:

        data = request.get_json()

        category = Category(
            name=data["name"],
            description=data.get("description", "")
        )

        db.session.add(category)
        db.session.commit()

        return jsonify({
            "message": "Category Added Successfully"
        }),201


    except Exception as e:

        db.session.rollback()

        print(e)

        return jsonify({
            "message": str(e)
        }),500

@api.route("/categories", methods=["GET"])
def get_categories():
    

    categories = Category.query.all()

    result = []

    for category in categories:
        result.append({
            "id": category.id,
            "name": category.name,
            "description": category.description
        })

    return jsonify(result)

@api.route("/products", methods=["POST"])
def add_product():

    data = request.get_json()

    product = Product(
        name=data["name"],
        sku=data["sku"],
        price=data["price"],
        quantity=data["quantity"],
        status=data["status"],
        category_id=data["category_id"]
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "Product Added Successfully"
    }), 201

@api.route("/products", methods=["GET"])
def get_products():

    products = Product.query.all()

    result = []

    for product in products:
        result.append({
            "id": product.id,
            "name": product.name,
            "sku": product.sku,
            "price": product.price,
            "quantity": product.quantity,
            "status": product.status,
            "category": product.category.name,
            "category_id": product.category_id

        })

    return jsonify(result)

@api.route("/products/<int:id>", methods=["PUT"])
def update_product(id):

    product = Product.query.get_or_404(id)

    data = request.get_json()

    product.name = data["name"]
    product.sku = data["sku"]
    product.price = data["price"]
    product.quantity = data["quantity"]
    product.status = data["status"]
    product.category_id = data["category_id"]

    db.session.commit()

    return jsonify({
        "message": "Product Updated Successfully"
    })

@api.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):

    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return jsonify({
        "message": "Product Deleted Successfully"
    })

@api.route("/dashboard", methods=["GET"])
def dashboard():

    total_products = Product.query.count()

    total_categories = Category.query.count()

    low_stock = Product.query.filter(Product.quantity < 10).count()

    out_of_stock = Product.query.filter(Product.quantity == 0).count()

    inventory_value = db.session.query(
        func.sum(Product.price * Product.quantity)
    ).scalar()

    if inventory_value is None:
        inventory_value = 0

    return jsonify({
        "total_products": total_products,
        "total_categories": total_categories,
        "low_stock_products": low_stock,
        "out_of_stock_products": out_of_stock,
        "total_inventory_value": inventory_value
    })

@api.route("/dashboard/recent-products", methods=["GET"])
def recent_products():

    products = Product.query.order_by(Product.id.desc()).limit(5).all()

    result = []

    for product in products:
        result.append({
            "id": product.id,
            "name": product.name,
            "category": product.category.name,
            "quantity": product.quantity,
            "status": product.status
        })

    return jsonify(result)

@api.route("/dashboard/low-stock", methods=["GET"])
def low_stock_products():

    products = Product.query.filter(Product.quantity < 10).all()

    result = []

    for product in products:
        result.append({
            "id": product.id,
            "name": product.name,
            "quantity": product.quantity,
            "status": product.status,
            "category": product.category.name
        })

    return jsonify(result)

@api.route("/dashboard/out-of-stock", methods=["GET"])
def out_of_stock_products():

    products = Product.query.filter(Product.quantity == 0).all()

    result = []

    for product in products:
        result.append({
            "id": product.id,
            "name": product.name,
            "quantity": product.quantity,
            "status": product.status,
            "category": product.category.name
        })

    return jsonify(result)

@api.route("/dashboard/category-summary", methods=["GET"])
def category_summary():

    categories = Category.query.all()

    result = []

    for category in categories:
        result.append({
            "category": category.name,
            "total_products": len(category.products)
        })

    return jsonify(result)

@api.route("/dashboard/inventory-value", methods=["GET"])
def inventory_value():

    categories = Category.query.all()

    result = []

    for category in categories:

        total_value = 0

        for product in category.products:
            total_value += product.price * product.quantity

        result.append({
            "category": category.name,
            "inventory_value": total_value
        })

    return jsonify(result)

@api.route("/products/<int:id>", methods=["GET"])
def get_single_product(id):

    product = Product.query.get_or_404(id)

    return jsonify({
        "id": product.id,
        "name": product.name,
        "sku": product.sku,
        "price": product.price,
        "quantity": product.quantity,
        "status": product.status,
        "category_id": product.category_id
    })

# ================= Update Category =================

@api.route("/categories/<int:id>", methods=["PUT"])
def update_category(id):

    category = Category.query.get_or_404(id)

    data = request.get_json()

    category.name = data["name"]
    category.description = data.get("description", "")

    db.session.commit()

    return jsonify({
        "message": "Category Updated Successfully"
    })

@api.route("/categories/<int:id>", methods=["GET"])
def get_single_category(id):

    category = Category.query.get_or_404(id)

    return jsonify({
        "id": category.id,
        "name": category.name,
        "description": category.description
    })

# ================= Delete Category =================

@api.route("/categories/<int:id>", methods=["DELETE"])
def delete_category(id):

    category = Category.query.get_or_404(id)

    db.session.delete(category)

    db.session.commit()

    return jsonify({
        "message": "Category Deleted Successfully"
    })



# GET ALL SUPPLIERS

@api.route("/suppliers", methods=["GET"])
def get_suppliers():

    suppliers = Supplier.query.all()

    return jsonify(
        [s.to_dict() for s in suppliers]
    )



# ADD SUPPLIER

@api.route("/suppliers", methods=["POST"])
def add_supplier():

    data = request.json


    supplier = Supplier(

        name=data["name"],
        contact_person=data.get("contact_person"),
        phone=data.get("phone"),
        email=data.get("email"),
        address=data.get("address"),
        status=data.get("status","Active")

    )


    db.session.add(supplier)

    db.session.commit()


    return jsonify({
        "message":"Supplier added successfully"
    })



# GET SINGLE SUPPLIER

# GET SINGLE SUPPLIER

@api.route("/suppliers/<int:id>")
def get_supplier(id):

    supplier = Supplier.query.get_or_404(id)

    return jsonify(
        supplier.to_dict()
    )



# UPDATE SUPPLIER

@api.route("/suppliers/<int:id>", methods=["PUT"])
def update_supplier(id):

    supplier = Supplier.query.get_or_404(id)

    data=request.json


    supplier.name=data["name"]
    supplier.contact_person=data.get("contact_person")
    supplier.phone=data.get("phone")
    supplier.email=data.get("email")
    supplier.address=data.get("address")
    supplier.status=data.get("status")


    db.session.commit()


    return jsonify({
        "message":"Supplier updated"
    })



# DELETE SUPPLIER

@api.route("/suppliers/<int:id>", methods=["DELETE"])
def delete_supplier(id):

    supplier=Supplier.query.get_or_404(id)

    db.session.delete(supplier)

    db.session.commit()


    return jsonify({
        "message":"Supplier deleted"
    })

# ================= ORDERS =================



# GET ALL ORDERS

@api.route("/orders", methods=["GET"])
def get_orders():

    orders = Order.query.all()

    return jsonify(
        [order.to_dict() for order in orders]
    )



# ADD ORDER
# ADD ORDER

@api.route("/orders", methods=["POST"])
def add_order():
    try:
        data = request.get_json()

        product_id = int(data["product_id"])

        product = Product.query.get(product_id)

        if not product:
            return jsonify({"message": "Product not found"}), 404

        order = Order(
            customer_name=data["customer_name"],
            product_id=product_id,
            quantity=int(data["quantity"]),
            total_amount=product.price * int(data["quantity"]),
            status=data.get("status", "Pending")
        )

        db.session.add(order)
        db.session.commit()

        return jsonify({"message": "Order Added Successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500



# UPDATE ORDER

@api.route("/orders/<int:id>", methods=["PUT"])
def update_order(id):

    order = Order.query.get_or_404(id)

    data=request.json


    order.customer_name=data["customer_name"]

    order.product_id=data["product_id"]

    order.quantity=data["quantity"]

    order.status=data["status"]


    db.session.commit()


    return jsonify({
        "message":"Order Updated Successfully"
    })





# DELETE ORDER

@api.route("/orders/<int:id>", methods=["DELETE"])
def delete_order(id):

    order = Order.query.get_or_404(id)


    db.session.delete(order)

    db.session.commit()


    return jsonify({
        "message":"Order Deleted Successfully"
    })


# ================= GET ALL USERS =================

@api.route("/users", methods=["GET"])
def get_users():

    users = User.query.all()

    return jsonify(
        [u.to_dict() for u in users]
    )



# ================= ADD USER =================

@api.route("/users", methods=["POST"])
def add_user():

    data = request.json


    user = User(

        name=data["name"],
        email=data["email"],
        password=data["password"],
        role=data["role"],
        status=data.get("status","Active")

    )


    db.session.add(user)

    db.session.commit()


    return jsonify({
        "message":"User added successfully"
    })



# ================= GET SINGLE USER =================

@api.route("/users/<int:id>")
def get_user(id):

    user = User.query.get_or_404(id)

    return jsonify(
        user.to_dict()
    )



# ================= UPDATE USER =================

@api.route("/users/<int:id>", methods=["PUT"])
def update_user(id):

    user = User.query.get_or_404(id)

    data = request.json


    user.name = data["name"]
    user.email = data["email"]
    user.role = data["role"]
    user.status = data.get("status")


    db.session.commit()


    return jsonify({
        "message":"User updated"
    })



# ================= DELETE USER =================

@api.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):

    user = User.query.get_or_404(id)


    db.session.delete(user)

    db.session.commit()


    return jsonify({
        "message":"User deleted"
    })