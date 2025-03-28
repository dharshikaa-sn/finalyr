from flask import Flask, render_template, request, redirect, url_for, flash
from main import database_connection

app = Flask(__name__)
app.secret_key = "your_secret_key"


@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uEmail = request.form.get('uEmail')
        uPassword = request.form.get('uPassword')
        print(uEmail, uPassword)
        connection = database_connection()
        cursor = connection.cursor()
        cursor.execute(f"select password from users where email='{uEmail}';")
        db_pwd = cursor.fetchall()
        print(db_pwd)
        cursor.execute(f"select email from users where email='{uEmail}';")
        mail = cursor.fetchall()
        print(mail)

        if mail == []:
            print("new user")
        else:
            if mail[0][0] == uEmail:

                if db_pwd[0][0] == uPassword:
                    print(db_pwd)
                    print(uPassword)
                    return render_template('dashboard.html')  # Render the second HTML page if login is successful
                # else:
                #     return render_template('nexGen.html', error="Invalid credentials")
                else:
                    error = 'Incorrect user credentials'
                    return render_template('nexGen.html', error=error)

        # Stay on the login page

        return render_template('nexGen.html')  # Default to the login page on GET request
    return render_template('nexGen.html')


@app.route("/logout")
def logout():
    return redirect(url_for("login"))


@app.route("/forgot_password")
def forgot_pwd():
    return render_template('forgot_password.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        business_name = request.form["business_name"]
        password = request.form["password"]
        re_password = request.form["re_password"]
        country = request.form["country"]
        state = request.form["state"]

        if password != re_password:
            flash("Passwords do not match!", "danger")
            return render_template("sign_up.html",
                                   full_name=full_name,
                                   email=email,
                                   phone=phone,
                                   business_name=business_name,
                                   country=country,
                                   state=state)

        else:
            flash("Account successfully created!", "success")
            connection = database_connection()
            cursor = connection.cursor()
            query = '''
                    INSERT INTO users (full_name, email, phone, business_name, password, country, state) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    '''

            values = (full_name, email, phone, business_name, password, country, state)
            cursor.execute(query, values)
            connection.commit()  # To save changes in the database
            return redirect(url_for("dashboard"))  # Redirect to a success page


    return render_template("sign_up.html")


# @app.route("/submit")


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == "__main__":
    app.run(debug=True)
