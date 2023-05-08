from app import app, db

with app.app_context():
   db.create_all()

#$ python
 #from project import app, db
 #app.app_context().push()
 #db.create_all()   

if __name__ == '__main__':
    app.run(debug=True)
