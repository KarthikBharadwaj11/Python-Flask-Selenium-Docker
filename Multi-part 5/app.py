from flask import Flask, request, jsonify, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
# from marshmallow_sqlalchemy import ModelSchema
from flask_marshmallow import Marshmallow
# from conf import ma
import os
from urllib.parse import quote 
from werkzeug.utils import secure_filename

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql+pymysql://root:%s@localhost:3306/student_flask'% quote('kabini'))


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Model
class Student(db.Model):
   __tablename__ = "students"
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(20))
   course = db.Column(db.String(100))
   profilePic = db.Column(db.String(255))

   def create(self):
       db.session.add(self)
       db.session.commit()
       return self

   def __init__(self, name, course, profilePic):
       self.name = name
       self.course = course
       self.profilePic = profilePic

   def __repr__(self):
       return f"{self.id}"

db.create_all()


class StudentSchema(ma.SQLAlchemyAutoSchema):

   class Meta:
      model = Student
      sqla_session = db.session
      load_instance = True
   id = fields.Number(dump_only=True)
   name = fields.String(required=True)
   course = fields.String(required=True)
   profilePic = fields.String(required=True)


@app.route('/')
def hello():
    return "Hello World"

@app.route('/api/v1/student', methods=['POST'])
def create_student():
      data = request.form
      name = data['name']
      course = data['course']
      
      files = request.files.getlist('profilePic')
      print(files)
      for file in files:
         if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            base = os.path.basename(filename)
            print(base)
            reqd_filename = os.path.splitext(base)[0]+ name + os.path.splitext(base)[1]
            print(reqd_filename)
            file.save(os.path.join('/home/kb/Desktop/VSCode/Multi-part 5/images', reqd_filename))
            new_data = data.to_dict()
            print(new_data)
            new_data['profilePic'] = reqd_filename
            print(new_data)
            student_schema = StudentSchema()
            student = student_schema.load(new_data)
            result = student_schema.dump(student.create())
            return make_response(jsonify({"student": result}), 200)

@app.route('/api/v1/student', methods=['GET'])
def index():
   get_students = Student.query.all()
   student_schema = StudentSchema(many=True)
   students = student_schema.dump(get_students)
   return make_response(jsonify({"students": students}))

@app.route('/api/v1/student/<id>', methods=['GET'])
def get_student_by_id(id):
   get_student = Student.query.get(id)
   student_schema = StudentSchema()
   student = student_schema.dump(get_student)
   return make_response(jsonify({"student": student}))

@app.route('/api/v1/student/<id>', methods=['PUT'])
def update_student_by_id(id):
   data = request.get_json()
   get_student = Student.query.get(id)
   if data.get('name'):
       get_student.name = data['name']
   if data.get('course'):
       get_student.course = data['course']
   # if data.get('profilePic'):
   #     get_student.profilePic = data['profilePic']
   db.session.add(get_student)
   db.session.commit()
   student_schema = StudentSchema(only=['id', 'name', 'course', 'profilePic'])
   student = student_schema.dump(get_student)

   return make_response(jsonify({"student": student}))

@app.route('/api/v1/student/<id>', methods=['DELETE'])
def delete_student_by_id(id):
   get_student = Student.query.get(id)
   db.session.delete(get_student)
   db.session.commit()
   return make_response("", 204)

if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)   