from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2,datetime,time
 
app = Flask(__name__)
app.secret_key = "hello"
con = psycopg2.connect(
    host ="127.0.0.1",
    database ="postgres",
    user = "postgres",
    password ="0000"
)

@app.route('/')
def Index():
    cur = con.cursor()
    cur.execute("SELECT * FROM (SELECT * FROM Public.Employee ORDER BY id desc limit 10)Employee order by id")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html',employees=data)
@app.route('/insert', methods=['GET','POST'])
def insert():
    if request.method == 'POST':
        userDetails=request.form
        idd=userDetails['id']
        name=userDetails['name']
        time=userDetails['time']
        cur= con.cursor()
        if not idd or not name or not time:
            flash("OOPS!! You have not filled up the data in all the given fields properly", "danger")
            con.commit()
            return redirect(url_for('Index'))
        try:
            cur.execute("INSERT INTO Public.Employee(id, name, time) VALUES (%s, %s, %s)",(idd,name,time))
            flash("SUCCESS!! Data Inserted Successfully", "success")
        except Exception:
            flash("WARNING!! There already exists data with the same ID", "warning")
        
        con.commit()
        return redirect(url_for('Index'))
@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("SUCCESS!! Record Has Been Deleted Successfully", "success")
    cur= con.cursor()
    cur.execute("DELETE FROM Public.Employee WHERE id=%s", (id_data,))
    con.commit()
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)
con.close()