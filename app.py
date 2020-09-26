from flask import Flask, render_template, request, redirect, url_for
import json
import os
import random

app = Flask(__name__)
database = {}
with open('food.json') as fp:
    database = json.load(fp)

@app.route('/')
def home():
    return "This is working"

@app.route('/food_list')
def show_food_list():
    return render_template('food_list.template.html', all_food = database)

@app.route('/food_list/add')
def show_form():
    return render_template('form.template.html')

@app.route('/food_list/add', methods=["POST"])
def process_add_food():
    food_name = request.form.get('food_name')
    num_calories = request.form.get('num_calories')
    type_of_meal = request.form.get('type_of_meal')
    date = request.form.get('date')
    database.append({
        'id' : random.randint(1000,99999),
        'food_name' : food_name,
        'num_calories' : num_calories,
        'type_of_meal' : type_of_meal,
        'date' : date
    })

    with open('food.json', 'w') as fp:
        json.dump(database,fp)

    return redirect(url_for('show_food_list'))

@app.route('/food_list/<int:id>/edit')
def show_edit_food(id):
    #find food record to edit
    food_to_edit = None
    for food in database:
        if food["id"] == id:
            food_to_edit = food
    if food_to_edit:
        return render_template('edit.template.html', food=food_to_edit)
    else:
        return f"Food with id {id} is not found"


@app.route('/food_list/<int:id>/edit', methods=["POST"])
def process_edit_food(id):
    food_to_edit = None
    for food in database:
        if food["id"] == id:
            food_to_edit = food
            break
    
    if food_to_edit:
        food_to_edit['food_name'] = request.form.get('food_name')
        food_to_edit['num_calories'] = request.form.get('num_calories')
        food_to_edit['type_of_meal'] = request.form.get('type_of_meal')
        food_to_edit['date'] = request.form.get('date')

    #save back to json file
        with open('food.json','w') as fp:
            json.dump(database, fp)

        return redirect(url_for('show_food_list'))
    else:
        return f"Food with id {id} is not found"

@app.route('/food_list/<int:id>/delete')
def show_delete_food(id):
    #find food entry 
    food_to_delete = None
    for food in database:
        if food["id"] == id:
            food_to_delete = food
    
    if food_to_delete:
        return render_template('ask_to_delete_food.template.html', food=food_to_delete)

@app.route('/food_list/<int:id>/delete', methods = ["POST"])
def confirm_delete_food(id):
    #find food
    food_to_delete = None
    for food in database:
        if food["id"] == id:
            food_to_delete = food
    
    if food_to_delete:
        database.remove(food_to_delete)

        with open('food.json', 'w') as fp:
            json.dump(database,fp)
        return redirect(url_for('show_food_list'))
    else:
        return f"Food with ID {{id}} is not found"


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)