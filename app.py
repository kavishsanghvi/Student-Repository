"""
@author: kavishsanghvi
@purpose: flask application fetching data from database
"""

from flask import Flask, render_template
app = Flask(__name__, template_folder='templates')
import sqlite3

def student_grades_table_db(db_path) -> None:
        db_file: str = db_path
        db: sqlite3.Connection = sqlite3.connect(db_file)
        query: str = "select students.Name, grades.StudentCWID, grades.Course, grades.Grade, instructors.Name from grades \
                  JOIN students on grades.StudentCWID = students.CWID \
                  JOIN instructors on grades.InstructorCWID = instructors.CWID \
                  ORDER BY students.Name ASC"
        
        ans: list = []
        for row in db.execute(query):
            ans.append((row))
            
        db.commit()
        db.close()
        return ans

ans = student_grades_table_db('lab12.db')

@app.route("/") 
def template_run():
    return render_template('home.html', ans=ans)


if __name__ == '__main__':
    app.run(debug=True, port=3005)
