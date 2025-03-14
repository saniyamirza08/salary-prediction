from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)
import mysql.connector as mc
conn = mc.connect(user='root', password='SaniyaMirza@23', host='localhost', database='datascience')
import joblib
model = joblib.load("gradientboosting.lb")


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('userdata.html') 

job_titles = {
    'Data Scientist': 0,
    'Data Analyst': 1,
    'Machine Learning Engineer': 2,
    'Big Data Engineer': 3,
    'ML Ops': 4
}

job_types = {
    'Full Time': 0,
    'Internship': 1
}

experience_levels = {
    'Senior': 0,
    'Mid': 1,
    'Entry': 2,
    'Executive': 3
}


@app.route('/userdata', methods=['GET', 'POST'])
def userdata():
    if request.method == 'POST':
    
        job_title = request.form['job_title']
        job_type = request.form['job_type']
        experience_level = request.form['experience_level']
    
        
        job_title_encoded = job_titles.get(job_title, -1)
        job_type_encoded = job_types.get(job_type, -1)
        experience_level_encoded = experience_levels.get(experience_level, -1)
    

        unseen_data = [[job_title_encoded, job_type_encoded, experience_level_encoded]]
        
        output = model.predict(unseen_data)[0]

        query = """INSERT INTO Salaries_data(job_title, job_type, experience_level, predicted)
                   VALUES (%s, %s, %s, %s)"""
        mycursor = conn.cursor()
        details = (job_title, job_type, experience_level, int(output))
        mycursor.execute(query, details)
        conn.commit()
        mycursor.close()

        return f"The predicted salary for the job is: {output}"

    return render_template('userdata.html')
    
@app.route('/history')
def history():

    conn = mc.connect(user="root", host="localhost", password="SaniyaMirza@23", database='datascience') 
    mycursor = conn.cursor()

    query = "SELECT job_title, job_type, experience_level, predicted FROM Salaries_data"  
    mycursor.execute(query)

    data = mycursor.fetchall()

    mycursor.close()
    conn.close()

    return render_template('history.html', userdetails=data)



if __name__ == "__main__":
    app.run(debug=True)

