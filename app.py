from flask import Flask, render_template, url_for, request, redirect #import flask, our function for rendering and URLfor to link css
from flask_sqlalchemy import SQLAlchemy #import our database which is SQLAlchemy
from datetime import datetime #import datetime functions

app = Flask(__name__) #create our app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #configure the database, everything is stored in that test.db file
db = SQLAlchemy(app) #set object, now we have initilized our database

#next step is to create a model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) #int to refernece each entery, this is our primary key
    content = db.Column(db.String(200), nullable=False) #String 200 characters, dont want it to be null
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow) #store datetime in a column, the function returns the current central time

    def __repr__(self):
        return '<Task %r>' % self.id #everytime we make a new task itll return the ID


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() #sort tasks by date
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:id>') #this is our route for the deleting path
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the task'
    
@app.route('/update/<int:id>', methods=['GET', 'POST']) #this is our route for the updating path
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content'] #set content in the task in this route to whatever you enter
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the task'
    else:
        return render_template('update.html', task = task)

if __name__ == "__main__":
    app.run(debug=True) #this makes it so that if we have any errors they pop up on the webpage
    