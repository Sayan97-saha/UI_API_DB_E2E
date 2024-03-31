import json
from pprint import pprint

import psycopg2
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from jsonschema import validate
from psycopg2 import sql
import pandas as pd

app = Flask(__name__)
CORS(app)


@app.route("/test")
def hello_world():
    resp_json = {"test": "data"}
    return resp_json


@app.route("/index")
def index_html():
    return render_template('index.html')


@app.route('/post_endpoint', methods=['POST'])
def post_endpoint():
    schema = {
        "type": "object",
        "properties": {
            "firstName": {"type": "string"},
            "lastName": {"type": "string"},
            "mobile": {"type": "string"},
            "qualification": {"type": "string"},
            "govt_id_type": {"type": "string"},
            "govt_id_num": {"type": "string"},
            "email": {"type": "string"},
            "dob": {"type": "string"},
            "exp": {"type": "string"},
            "preferred_role": {"type": "string"},
            "certifications": {"type": "string"},
            "filename": {"type": "string"}
        },
        "required": ["firstName", "lastName", "mobile", "qualification", "govt_id_type", "govt_id_num",
                     "email", "dob", "exp", "preferred_role", "filename",]
    }

    data = request.json
    try:
        validate(instance=data, schema=schema)
        print("Received data:", data)

        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="password",
            port=5432
        )

        f_name = data['firstName']
        l_name = data['lastName']
        mob_num = data['mobile']
        qualification = data['qualification']
        govt_id_type = data['govt_id_type']
        govt_id_num = data['govt_id_num']
        email = data['email']
        dob = data['dob']
        exp = data['exp']
        pref_role = data['preferred_role']
        certifications = data['certifications']
        resume_filename = data['filename']

        cursor = conn.cursor()
        print("DB connected")
        query = "select count(*) from registration_details where govt_id_num = '"+govt_id_num+"' or contact_number = '"+mob_num+"' or email = '"+email+"'"
        print("check query = " + query)
        cursor.execute(sql.SQL(query))

        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=columns)
        print(df)

        if(df.loc[0, 'count'] == 0):
            print("Data check successful! Data is not present in DB, injecting data")
            query = ("insert into registration_details (first_name, last_name, contact_number, qualification, govt_id_type, govt_id_num, email,"+
								  "date_of_birth, experience_range, preferred_role, certifications, resume_filename)"+
								  "values ('"+f_name+"', '"+l_name+"', '"+mob_num+"', '"+qualification+"', '"+govt_id_type+"', '"+govt_id_num+
                                   "', '"+email+"', '"+dob+"', '"+exp+"', '"+pref_role+"', '"+certifications+"', '"+resume_filename+"')")
            print("Data injection query = " + query)
            cursor.execute(sql.SQL(query))
            conn.commit()
            print("Data injection successful!")
        else:
            print("data already exists, cannot inject data!")
            raise Exception("data already exists, cannot inject data!")

    except Exception as e:
        print(e)
        return jsonify({'error': pprint(str(e))}), 400

    # name = data['name']
    # age = data['age']
    # phone = data['phone']
    #



    return jsonify({'message': 'Data submitted successfully'})


app.run()
