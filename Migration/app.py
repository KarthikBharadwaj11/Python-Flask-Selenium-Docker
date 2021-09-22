from os import name
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
#from marshmallow_sqlalchemy import ModelSchema
from flask_marshmallow import Marshmallow 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/employee'
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Employee(db.Model):
   __tablename__ = "Employee_list"
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(20))
   age= db.Column(db.Integer)

   def create(self):
       db.session.add(self)
       db.session.commit()
       return self

   def __init__(self, name, age):
       self.name = name
       self.age = age

   def __repr__(self):
       return f"{self.id}"

db.create_all()

class EmployeeSchema(ma.SQLAlchemyAutoSchema):
   class Meta:
       model = Employee
       sqla_session = db.session
       load_instance = True
   id = fields.Number(dump_only=True)
   name= fields.String(required=True)
   age = fields.Integer(required=True)

@app.route('/api/v1/employee', methods=['POST'])
def create_todo():
   data = request.get_json()
   employee_schema = EmployeeSchema()
   employee = employee_schema.load(data)
   result = employee_schema.dump(employee.create())
   return make_response(jsonify({"employee": result}), 200)  


@app.route('/api/v1/employee', methods=['GET'])
def index():
   get_employee = Employee.query.all()
   employee_schema = EmployeeSchema(many=True)
   todos = employee_schema.dump(get_employee)
   return make_response(jsonify({"employee": Employee}))

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)