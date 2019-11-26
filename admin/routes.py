from flask import *
from functools import wraps
from login_form import Verifier
from pymysql import OperationalError, connect
import uuid, copy

admin = Blueprint("admin", __name__, template_folder="templates")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username', None) == "admin":
            return f(*args, **kwargs)
        else:
            return redirect(url_for('main.login_page', a='1', next=request.url))

    return decorated_function


@admin.route("/adminlogin", methods=['POST'])
def admin_login():
    session.clear()
    V = Verifier("admin", request.form.get('passwd'), "admin")

    try:
        success = V.verify()

        if success:
            session['username'] = "admin"
            session['password'] = request.form['passwd']

            if session.get('next_page', None) != None:
                next_page = session['next_page']
                session.pop('next_page')
                return redirect(next_page)

            return redirect(url_for('admin.admin_home'))
        else:
            flash("admin")
            return redirect(url_for('main.login_page', lf=uuid.uuid4().hex[:-4], a='1'))
    except OperationalError:
        flash("Connection Error")
        return redirect(url_for('main.login_page', ce='1', a='1'))


@admin.route("/admin")
@login_required
def admin_home():
    conn = connect("localhost", "root", "password", "jee")
    cursor = conn.cursor()

    if request.args.get('select_type') == 'reg_incom':
        cursor.execute(
            "SELECT id,name,physics,chemistry,maths,photo,signature,marksheet,upload_verified,info_verified,step_2,step_3 FROM student WHERE step_2 = 0 OR step_3 = 0")

    elif request.args.get('select_type') == 'verified':
        cursor.execute(
            "SELECT id,name,physics,chemistry,maths,photo,signature,marksheet,upload_verified,info_verified,step_2,step_3 FROM student WHERE upload_verified IS NOT NULL AND info_verified IS NOT NULL")

    elif request.args.get('select_type') == 'not_verified':
        cursor.execute(
            "SELECT id,name,physics,chemistry,maths,photo,signature,marksheet,upload_verified,info_verified,step_2,step_3 FROM student WHERE upload_verified IS NULL OR info_verified IS NULL")
    else:
        cursor.execute(
            "SELECT id,name,physics,chemistry,maths,photo,signature,marksheet,upload_verified,info_verified,step_2,step_3 FROM student")

    result = cursor.fetchall()

    cursor.execute("SELECT * FROM claims WHERE resolved=0 AND seen_admin=0")
    notifications = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM claims WHERE seen_admin=0")
    notifs = cursor.fetchall()

    return render_template('admin/home.html', title="Admin", students=result, notifications=notifications,
                           no_of_notifs=notifs[0][0])


@admin.route("/admin/ranking")
@login_required
def ranking():
    return "RANK"


@admin.route("/admin/change", methods=['GET', 'POST'])
@login_required
def change_data():
    conn = connect("localhost", "root", "password", "jee")
    cursor = conn.cursor()

    if request.method == "POST":
        cursor.execute("UPDATE student SET physics=%.1f,chemistry=%.1f,maths=%.1f WHERE id=%d" % (
        float(request.form['physics']), float(request.form['chemistry']), float(request.form['maths']),
        int(request.form['id'])))
        conn.commit()
        flash("Marks of student changed successfully")

    cursor.execute(
        "SELECT id,name,email,physics,chemistry,maths FROM student WHERE id=%d" % int(request.args.get('id')))
    result = cursor.fetchall()
    conn.close()
    return render_template('admin/change_data.html', student=result[0], id=request.args.get('id'), no_of_notifs=0)


@admin.route("/admin/update", methods=['GET', 'POST'])
@login_required
def update_ranks():
    conn = connect("localhost", "root", "password", "jee")
    cursor = conn.cursor()
    new_data = []

    cursor.execute("SELECT id FROM student WHERE step_2 = 0 OR step_3 = 0")
    result = cursor.fetchall()

    # if result:
    # 	flash("You must verify all account first and update all students marks")
    # 	return redirect(url_for('admin.admin_home'))
    # AIR RANK
    cursor.execute("SELECT id,physics,chemistry,maths,AIR FROM student")
    result = cursor.fetchall()

    result = sorted(result, key=lambda student: student[1] + student[2] + student[3], reverse=True)

    for rank, values in enumerate(result):
        cursor.execute("UPDATE student SET physics=%d,chemistry=%d,maths=%d,AIR=%d WHERE id=%d" % (values[1],
                                                                                                   values[2], values[3],
                                                                                                   rank + 1, values[0]))

    # OBC RANK
    cursor.execute("SELECT id,physics,chemistry,maths,obc_rank FROM student WHERE category='OBC'")
    result = cursor.fetchall()

    result = sorted(result, key=lambda student: student[1] + student[2] + student[3], reverse=True)

    for rank, values in enumerate(result):
        cursor.execute("UPDATE student SET physics=%d,chemistry=%d,maths=%d,obc_rank=%d WHERE id=%d" % (values[1],
                                                                                                        values[2],
                                                                                                        values[3],
                                                                                                        rank + 1,
                                                                                                        values[0]))

    # SC RANK
    cursor.execute("SELECT id,physics,chemistry,maths,sc_rank FROM student WHERE category='SC'")
    result = cursor.fetchall()

    result = sorted(result, key=lambda student: student[1] + student[2] + student[3], reverse=True)

    for rank, values in enumerate(result):
        cursor.execute("UPDATE student SET physics=%d,chemistry=%d,maths=%d,sc_rank=%d WHERE id=%d" % (values[1],
                                                                                                       values[2],
                                                                                                       values[3],
                                                                                                       rank + 1,
                                                                                                       values[0]))

    # ST RANK
    cursor.execute("SELECT id,physics,chemistry,maths,st_rank FROM student WHERE category='ST'")
    result = cursor.fetchall()

    result = sorted(result, key=lambda student: student[1] + student[2] + student[3], reverse=True)

    for rank, values in enumerate(result):
        cursor.execute("UPDATE student SET physics=%d,chemistry=%d,maths=%d,st_rank=%d WHERE id=%d" % (values[1],
                                                                                                       values[2],
                                                                                                       values[3],
                                                                                                       rank + 1,
                                                                                                       values[0]))

    conn.commit()
    conn.close()
    flash("All the ranks has been updated successfully")
    return redirect(url_for('admin.admin_home'))


@admin.route("/admin/notification")
@login_required
def notification():
    conn = connect("localhost", "root", "password", "jee")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM claims")
    claims = cursor.fetchall()

    cursor.execute("UPDATE claims SET seen_admin=1 WHERE seen_admin=0")
    conn.commit()
    conn.close()

    return render_template('admin/notification.html', title="notification", notifications=claims, no_of_notifs=0)


@admin.route("/admin/verify", methods=['GET', 'POST'])
@login_required
def verify():
    conn = connect("localhost", "root", "password", "jee")
    cursor = conn.cursor()

    if request.method == "POST":
        r = request.form
        cursor.execute('''UPDATE student SET address='{}',applying_for='{}',category='{}',
			date_of_birth='{}', email='{}', father_name='{}', mother_name='{}',
			gender='{}', mode_of_exam='{}',name='{}',paper_medium='{}',
			phone='{}',pwd='{}',state_of_eligibility='{}',
			upload_verified={},info_verified={} WHERE id={}'''.format(r['address'].upper(),
                                                                      r['applying_for'].upper(), r['category'].upper(),
                                                                      r['date_of_birth'], r['email'],
                                                                      r['father_name'].upper(),
                                                                      r['mother_name'].upper(),
                                                                      r['gender'].upper(), r['mode_of_exam'].upper(),
                                                                      r['name'].upper(), r['paper_medium'].upper(),
                                                                      r['phone'], r['pwd'],
                                                                      r['state_of_eligibility'].upper(), 1, 1,
                                                                      int(request.args.get('id'))))
        conn.commit()

    cursor.execute("SELECT * FROM student WHERE id=%d" % (int(request.args.get('id'))))

    result = cursor.fetchall()
    conn.close()

    return render_template('admin/verify.html', title="Verify", student=result[0], no_of_notifs=0)


@admin.route("/admin/resolve")
@login_required
def resolve():
    conn = connect("localhost", "root", "password", "jee")
    cursor = conn.cursor()

    cursor.execute("UPDATE claims SET resolved=1,seen_admin=1 WHERE id=%d" % (int(request.args.get('id'))))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.notification'))
