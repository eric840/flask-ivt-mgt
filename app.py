import os
import peeweedbevolve # new; must be imported before models
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Store, Warehouse

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.before_request
def before_request():
   db.connect()

@app.after_request
def after_request(response):
   db.close()
   return response

@app.cli.command() # new
def migrate(): # new 
   db.evolve(ignore_tables={'base_model'}) # new

@app.route("/", methods=['GET'])
def index():
   return "Inventory Management System"

# display all stores
@app.route("/store/", methods=['GET'])
def store_index():
   stores =  Store.select()
   return render_template('store_index.html',stores=stores)

# show create store form
@app.route("/store/new", methods=['GET'])
def store_new():
    return render_template('store_new.html')

# create new store with data from form
@app.route("/store/", methods=['POST'])
def store_create():
    # get form value in form
    store_name = request.form.get('store_name')
    store = Store(name=store_name)
    if store.save(): 
        flash("Store created!", "success")
    else:
        flash("Unable to create!", "danger")
    return redirect(url_for('store_new'))

# show specific store with id
@app.route("/store/<store_id>", methods=['GET'])
def store_show(store_id):
    store = Store.get_by_id(store_id) # query to get one store with id
    return render_template('store_show.html',store=store) # then pass store instance to the html template

# update specific store with id 
@app.route("/store/<store_id>", methods=['POST'])
def store_update(store_id):
    store = Store.get_by_id(store_id)
    store.name = request.form.get('store_name')
    if store.save():
        flash("Updated!", "success")
    else:
        flash("Unable to update store.", "danger")
    return redirect(url_for("store_show", store_id=store.id))

# delete specific store with id
@app.route("/store/<store_id>/delete", methods=['POST'])
def store_delete(store_id):
    store = Store.get_by_id(store_id)
    if store.delete_instance():
        flash("Deleted!", "success")
    return redirect(url_for("store_index"))

# show create warehouse form 
@app.route("/warehouse/new", methods=["GET"])
def warehouse_new():
    stores = Store.select() # to render all store in select options
    return render_template("warehouse_new.html", stores=stores)

# create new warehouse with data from form
@app.route("/warehouse/", methods=["POST"])
def warehouse_create():
    w = Warehouse(store=request.form.get("store_id"), location=request.form.get("location"))
    if w.save():
        flash("Warehouse created.", "success")
    else:
        flash("Unable to create warehouse.", "danger")
    return redirect(url_for("warehouse_new"))

if __name__ == '__main__':
   app.run()