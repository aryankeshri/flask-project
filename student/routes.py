from flask import *
from functools import wraps
import hashlib, os, uuid
from pymysql import OperationalError, connect
from login_form import Verifier
from twilio.rest import Client
import random
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Message

student = Blueprint("student", __name__, template_folder="templates")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username', None) != None and session.get('username', "admin") != "admin":
            return f(*args, **kwargs)
        else:
            return redirect(url_for('main.login_page', next=request.url, s='1'))

    return decorated_function


@student.route("/student/register/")
@login_required
def register_incomplete():
    conn = connect("localhost", "root", "password", "jee")
    cursor = conn.cursor()

    cursor.execute("SELECT step_1,step_2,step_3 FROM student WHERE id=%s" % (session['id']))
    result = cursor.fetchall()[0]

    return render_template('student/register_incomplete.html', title='Registration', steps=result, no_of_notifs=0)


@student.route("/student/register/info", methods=['GET', 'POST'])
def register_step_1():
    return render_template('student/register/info.html', title="Register | Step 1")


@student.route("/student/register/upload", methods=['GET', 'POST'])
@login_required
def register_step_2():
    return render_template('student/register/upload.html', title="Register | Step 2")


@student.route("/student/register/payment")
@login_required
def register_step_3():
    return render_template('/student/register/payment.html', title="Payment")


@student.route("/student/register/payment/processing")
@login_required
def fake_payment_page():
    return render_template('/student/register/payment_processing.html', title='Processing Payment')


@student.route("/student/register", methods=['POST'])
def register_student():
    conn = connect("localhost", "root", "password", "jee")
    cursor = conn.cursor()

    # registration step 1 start here
    if "student/register/info" in request.referrer:

        cursor.execute("SELECT id FROM student ORDER BY id DESC LIMIT 1")
        ID = cursor.fetchall()
        newID = 1000
        if ID:
            newID = int(ID[0][0]) + 1

        session['username'] = request.form['name'].upper()
        session['father_name'] = request.form['father_name'].upper()
        session['mother_name'] = request.form['mother_name'].upper()
        session['gender'] = request.form['gender'].upper()
        session['state_of_eligibility'] = request.form['state_of_eligibility'].upper()
        session['date_of_birth'] = request.form['date'] + "-" + request.form['month'] + "-" + request.form['year']
        session['category'] = request.form['category'].upper()
        session['pwd'] = request.form['pwd'].upper()
        session['applying_for'] = request.form['applying_for'].upper()
        session['mode_of_exam'] = request.form['mode_of_exam'].upper()
        session['paper_medium'] = request.form['paper_medium'].upper()
        session['address'] = request.form['address'].upper()
        session['email'] = request.form['email']
        session['phone'] = request.form['phone'].upper()

        session['photo'] = None
        session['signature'] = None
        session['marksheet'] = None
        session['step_1'] = 1
        session['step_2'] = None
        session['step_3'] = None
        session['physics'] = 0
        session['chemistry'] = 0
        session['maths'] = 0
        session['AIR'] = None
        session['upload_verified'] = None
        session['info_verified'] = None
        session['obc_rank'] = None
        session['sc_rank'] = None
        session['st_rank'] = None

        cursor.execute('''INSERT INTO student(id,name,father_name,mother_name,gender,state_of_eligibility,date_of_birth,category,
pwd,applying_for,mode_of_exam,paper_medium,address,email,phone,password,step_1) VALUES({newID},'{username}',
'{father_name}','{mother_name}','{gender}','{state_of_eligibility}','{date_of_birth}','{category}','{pwd}','{applying_for}',
'{mode_of_exam}','{paper_medium}','{address}','{email}','{phone}','{passwd}',1) '''.format(newID=newID, **session,
                                                                                           passwd=request.form[
                                                                                               'passwd']))

        cursor.execute('''INSERT INTO credential(id,name,password) VALUES(%d,'%s','%s')''' % (
            newID, session['username'], request.form['passwd']))
        conn.commit()
        conn.close()

        session['id'] = newID
        session['password'] = request.form['passwd']

        # email send here
        from run import mail

        msg = Message('JEE MAIN Registration', sender='noreply@gmail', recipients=['ahteshamul8900@gmail.com'])

        msg.body = f'''Your Registration ID : %d''' % (session['id'])
        mail.send(msg)
        flash("Your registration ID is sent to your email address")
        #
        return redirect(url_for('student.register_step_2'))

    # registrations step 2 start here

    elif "student/register/upload" in request.referrer:

        ALLOWED_EXTENSION = ['jpg', 'jpeg']
        UPLOAD_FOLDER = 'static/student/' + str(session['id'])

        image = request.files['image']
        signature = request.files['signature']
        marksheet = request.files['marksheet']

        # hashed filenames
        image.filename = image.filename + str(session['id'])  # session id
        signature.filename = signature.filename + str(session['id'])
        marksheet.filename = marksheet.filename + str(session['id'])

        image.filename = hashlib.md5(image.filename.encode()).hexdigest()
        signature.filename = hashlib.md5(signature.filename.encode()).hexdigest()
        marksheet.filename = hashlib.md5(marksheet.filename.encode()).hexdigest()

        if not os.path.exists(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)

        image_path = os.path.join(UPLOAD_FOLDER + "/", image.filename)
        signature_path = os.path.join(UPLOAD_FOLDER + "/", signature.filename)  # session id
        marksheet_path = os.path.join(UPLOAD_FOLDER + "/", marksheet.filename)

        print(image_path)
        print(signature_path)
        print(marksheet_path)

        cursor.execute('''UPDATE student SET photo='/%s',signature='/%s',marksheet='/%s',step_2=1
			WHERE id=%d''' % (image_path, signature_path, marksheet_path, session['id']))

        conn.commit()
        conn.close()

        image.save(image_path)
        signature.save(signature_path)
        marksheet.save(marksheet_path)

        session['photo'] = image_path
        session['signature'] = signature_path
        session['marksheet'] = marksheet_path
        session['step_2'] = 1

        return redirect(url_for("student.register_step_3"))

    # registration step 3 start here

    elif "student/register/payment" in request.referrer:
        cursor.execute("UPDATE student SET step_3=1")
        conn.commit()
        conn.close()
        session['step_3'] = 1
        return redirect(url_for('student.fake_payment_page'))


######################################### login verifier ###############################################

@student.route("/studentlogin", methods=['POST'])
def student_login():
    print(request.form.get('passwd'))
    V = Verifier(request.form.get('id'), request.form.get('passwd'), "student")

    try:
        all_data = V.verify()

        if all_data:
            session['id'] = int(all_data[0])
            session['username'] = all_data[1]
            session['father_name'] = all_data[2]
            session['mother_name'] = all_data[3]
            session['gender'] = all_data[4]
            session['state_of_eligibility'] = all_data[5]
            session['date_of_birth'] = all_data[6]
            session['category'] = all_data[7]
            session['pwd'] = all_data[8]
            session['applying_for'] = all_data[9]
            session['mode_of_exam'] = all_data[10]
            session['paper_medium'] = all_data[11]
            session['address'] = all_data[12]
            session['email'] = all_data[13]
            session['phone'] = all_data[14]
            session['password'] = all_data[15]
            session['photo'] = all_data[16]
            session['signature'] = all_data[17]
            session['marksheet'] = all_data[18]
            session['step_1'] = all_data[19]
            session['step_2'] = all_data[20]
            session['step_3'] = all_data[21]
            session['physics'] = all_data[22]
            session['chemistry'] = all_data[23]
            session['maths'] = all_data[24]
            session['AIR'] = all_data[25]
            session['upload_verified'] = all_data[26]
            session['info_verified'] = all_data[27]
            session['obc_rank'] = all_data[28]
            session['sc_rank'] = all_data[29]
            session['st_rank'] = all_data[30]

            if session.get('next_page', None) != None:
                next_page = session.get('next_page')
                session.pop('next_page')
                return redirect(next_page)

            return redirect(url_for('student.student_home'))
        else:
            flash("student")
            return redirect(url_for('main.login_page', lf=uuid.uuid4().hex[:-4], s='1'))
    except OperationalError:
        flash("Connection Error")
        return redirect(url_for('main.login_page', ce='1', s='1'))


############################### Home pages ##########################

@student.route("/student", methods=['GET', 'POST'])
@login_required
def student_home():
    conn = connect("localhost", "root", "password", "jee")
    cursor = conn.cursor()

    cursor.execute("SELECT subject,message,resolved,id FROM claims WHERE id=%d AND resolved=1 AND seen_student=0" % (
        int(session['id'])))
    notifications = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM claims WHERE id=%d AND resolved=1 AND seen_student=0" % (int(session['id'])))
    notifs = cursor.fetchall()

    # if notifications:
    # 	flash("notification")
    # else:
    # 	session.pop('_flash',None)

    return render_template('student/profile.html', title="Profile", notifications=notifications,
                           no_of_notifs=notifs[0][0])


################################# Rankings ##################################3

@student.route("/student/ranking", methods=['GET', 'POST'])
@login_required
def student_ranking():
    conn = connect("localhost", "root", "password", "jee")
    cursor = conn.cursor()

    prepareSQL = "SELECT id,name,gender,date_of_birth,physics,chemistry,maths,(maths+chemistry+physics) as total,AIR,obc_rank,st_rank,sc_rank FROM student ORDER BY "

    if request.args.get('s') == 'phy' and request.args.get('o') == 'a':
        prepareSQL += "physics ASC"
    elif request.args.get('s') == 'phy' and request.args.get('o') == 'd':
        prepareSQL += "physics DESC"

    elif request.args.get('s') == 'chem' and request.args.get('o') == 'a':
        prepareSQL += "chemistry ASC"
    elif request.args.get('s') == 'chem' and request.args.get('o') == 'd':
        prepareSQL += "chemistry DESC"

    elif request.args.get('s') == 'maths' and request.args.get('o') == 'a':
        prepareSQL += "maths ASC"
    elif request.args.get('s') == 'maths' and request.args.get('o') == 'd':
        prepareSQL += "maths DESC"

    elif request.args.get('s') == 'AIR' and request.args.get('o') == 'a':
        prepareSQL += "AIR ASC"
    elif request.args.get('s') == 'AIR' and request.args.get('o') == 'd':
        prepareSQL += "AIR DESC"

    elif request.args.get('s') == 'tot' and request.args.get('o') == 'a':
        prepareSQL += "total ASC"
    elif request.args.get('s') == 'tot' and request.args.get('o') == 'd':
        prepareSQL += "total DESC"

    elif request.args.get('s') == 'id' and request.args.get('o') == 'a':
        prepareSQL += "id ASC"
    elif request.args.get('s') == 'id' and request.args.get('o') == 'd':
        prepareSQL += "id DESC"

    elif request.args.get('s') == 'name' and request.args.get('o') == 'a':
        prepareSQL += "name ASC"
    elif request.args.get('s') == 'name' and request.args.get('o') == 'd':
        prepareSQL += "name DESC"

    elif request.args.get('s') == 'obc' and request.args.get('o') == 'a':
        prepareSQL += "obc_rank ASC"
    elif request.args.get('s') == 'obc' and request.args.get('o') == 'd':
        prepareSQL += "obc_rank DESC"

    elif request.args.get('s') == 'sc' and request.args.get('o') == 'a':
        prepareSQL += "sc_rank ASC"
    elif request.args.get('s') == 'sc' and request.args.get('o') == 'd':
        prepareSQL += "sc_rank DESC"

    elif request.args.get('s') == 'st' and request.args.get('o') == 'a':
        prepareSQL += "st_rank ASC"
    elif request.args.get('s') == 'st' and request.args.get('o') == 'd':
        prepareSQL += "st_rank DESC"

    else:
        prepareSQL += "name ASC"

    cursor.execute(prepareSQL)
    result = cursor.fetchall()
    conn.close()
    return render_template('student/ranking.html', title="Ranking", rank=result, int=int, no_of_notifs=0)


@student.route("/student/password", methods=['GET', 'POST'])
@login_required
def student_password():
    conn = connect("localhost", "root", "password", "jee")
    cursor = conn.cursor()
    passwd = request.form['passwd']
    hash_passwd = hashlib.md5(passwd.encode()).hexdigest()

    cursor.execute("UPDATE student SET password='%s' WHERE id=%d" % (hash_passwd, session['id']))
    conn.commit()
    cursor.execute("UPDATE credential SET password='%s' WHERE id=%d" % (passwd, session['id']))
    conn.commit()
    conn.close()

    return redirect(url_for('student.student_home'))


@student.route("/student/notification")
@login_required
def notification():
    conn = connect("localhost", "root", "password", "jee")
    cursor = conn.cursor()

    cursor.execute("SELECT subject,message,resolved FROM claims WHERE id=%d" % (int(session['id'])))
    all_notifications = cursor.fetchall()

    cursor.execute("UPDATE claims SET seen_student=1 WHERE id=%d" % (int(session['id'])))
    conn.close()

    return render_template('student/notification.html', title="Notification", all_notifications=all_notifications,
                           no_of_notifs=0)


@student.route("/student/claim", methods=['POST'])
@login_required
def claim():
    conn = connect("localhost", "root", "password", "jee")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO claims VALUES(%d,'%s','%s','%s',0,0,0)" % (
        int(session['id']), session['username'], request.form['subject'], request.form['claim']))
    conn.commit()
    conn.close()

    return redirect(url_for('student.student_home'))


@student.route("/student/college", methods=['GET', 'POST'])
@login_required
def college():
    conn = connect("localhost", "root", "password", "jee")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM college LIMIT 900")
    result1 = cursor.fetchall()
    cursor.execute("SELECT category FROM student WHERE id=%d" % (int(session['id'])))
    result2 = cursor.fetchall()
    # cursor.execute("SELECT AIR,obc_rank,sc_rank,st_rank FROM student WHERE id=%d"%(int(session['id'])))
    # result2 = cursor.fetchall()

    conn.close()
    return render_template("student/college.html", title="Colleges", colleges=result1, category=result2, no_of_notifs=0)


@student.route("/student/resolved")
@login_required
def resolved_claim():
    conn = connect("localhost", "root", "password", "jee")
    cursor = conn.cursor()

    cursor.execute("UPDATE claims SET seen_student=1 WHERE id=%d" % (int(session['id'])))
    conn.commit()
    conn.close()
    return redirect(url_for('student.student_home'))


@student.route("/student/resetoption")
def reset_option():
    return render_template('/student/reset/reset_option.html', title="Reset Request")


@student.route("/student/resetparse", methods=['GET', 'POST'])
def reset_parse():
    data = {'email_verify': '', 'otp_verify': ''}

    conn = connect("localhost", "root", "password", "jee")

    try:
        ids = int(request.form['id'])
    except:
        flash("Invalid registration number. Please enter a valid registration id")
        return redirect(url_for('student.reset_option'))

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE id=%d" % (ids))
    result = cursor.fetchall()

    if not result:
        flash("Invalid registration number. Please enter a valid registration id")
        return redirect(url_for('student.reset_option'))

    data = {'id': request.form['id']}
    s = Serializer('secret', 600)

    if 'email_verify' in request.form:
        token = s.dumps(data)

        conn = connect('localhost', 'root', 'password', 'jee')
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM student WHERE id=%d" % (int(request.form['id'])))
        email = cursor.fetchall()[0][0]

        from run import mail

        msg = Message('Password Request Request', sender='noreply@gmail', recipients=['ahteshamul8900@gmail.com'])

        msg.body = f'''To reset your password, visit the given link:
        {url_for('student.reset_password',token=token,_external=True)}'''
        print(msg)
        # mail.send(msg)
        flash("An email has been sent to your email address valid for next 10 minutes")
        return redirect(url_for('student.reset_option'))

    if 'otp_verify' in request.form:
        OTP = int(random.uniform(209483, 899837))
        print(OTP)
        data['otp'] = str(OTP)
        token = s.dumps(data).decode('utf-8')
        #
        # account_sid = 'AC85f8424cd53699fdd1e909c8c68561ed'
        # auth_token = '2d6b96bc480837dcce949d2c59bd649b'
        #
        # myPhone = '+917366944929'
        # TwilioNumber = '+15206367520'
        #
        # client = Client(account_sid, auth_token)
        #
        # client.messages.create(
        #     to=myPhone,
        #     from_=TwilioNumber,
        #     body='The OTP number is ' + str(OTP)
        # )

        flash("An OTP has been sent to your registered mobile number valid for next 10 minutes")
        return redirect(url_for('student.reset_from_otp', token=token, method='otp', otp=data['otp']))


@student.route("/student/resetotp/<token>", methods=['GET', 'POST'])
def reset_from_otp(token):
    if request.method == "POST":
        try:
            s = Serializer('secret', 600)
            data = s.loads(token)
            ID = data['id']

            if (request.args.get('method') == 'otp' and data['otp'] == request.form['otp']) or request.args.get(
                    'method') == 'email':
                return redirect(url_for('student.reset_password', token=token))

            else:
                raise ValueError("Invalid OTP")
        except:
            flash("The entered OTP is invalid or expired")

    return render_template('student/reset/reset_from_otp.html', title='Reset From OTP', toks=token)


@student.route("/student/resetpassword/<token>", methods=['GET', 'POST'])
def reset_password(token):
    try:
        s = Serializer('secret', 600)
        data = s.loads(token)
        ID = data['id']

        if request.method == "POST":
            passwd = request.form['passwd']
            confirm_passwd = request.form['confirm_passwd']

            if passwd != confirm_passwd:
                flash("Enter same password in both input fields")
            else:
                conn = connect("localhost", "root", "password", "jee")
                cursor = conn.cursor()

                cursor.execute("UPDATE jee.student SET password='%s' WHERE id=%d" % (request.form['passwd'], int(ID)))
                cursor.execute(
                    "UPDATE jee.credential SET password='%s' WHERE id='%s'" % (request.form['passwd'], str(ID)))
                conn.commit()
                conn.close()
                flash("Password reset successfully. You can now login to your account")
                return redirect(url_for('main.login_page'))
    except:
        flash("Timed out for resetting password. Try again to reset the password")

    return render_template('/student/reset/reset_password.html', title='Reset Password', token=token)
