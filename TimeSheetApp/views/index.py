from flask import Blueprint, render_template, session, redirect, url_for, escape, request, flash
#from simplecrypt import encrypt, decrypt
import pymysql
from TimeSheetApp.config.config import database_config as db_conf

db = pymysql.connect(db_conf['host'], db_conf['user'], db_conf['password'], db_conf['db_name'])
bp = Blueprint('__name__', __name__, template_folder='templates')

@bp.route('/')
def show():
    if 'username' in session :
        cursor = db.cursor()
        results = ""
        if session['flag'] == 'U':
            sql = "SELECT * FROM project_emp where emp_email = %s"
            cursor.execute(sql, session['username'])
            results = cursor.fetchall()
        else:
            sql = "SELECT * FROM emp_work"
            cursor.execute(sql)
            results = cursor.fetchall()
        cursor.close()
        #db.close()
        return render_template('home.html', results=results, resultedit=[])
        #return render_template('home.html')

    return redirect(url_for('__name__.loginshow'))

@bp.route('/loginshow')
def loginshow():
    return render_template('loginpage.html')

@bp.route('/showchangepass')
def showchangepass():
    return render_template('changepass.html')

@bp.route('/projectemp')
def projectemp():
    if session:
        if session['flag'] != 'U':
            cursor = db.cursor()
            sql = "SELECT * FROM emp_details"
            cursor.execute(sql)
            resultemp = cursor.fetchall()
            sql = "SELECT * FROM project_emp"
            cursor.execute(sql)
            resultprojectemp = cursor.fetchall()
            finalresult = []
            for row in resultemp:
                empres = {'name' : row[1], 'email' : row[8], 'payload': []}
                #empres.name = row[1]
                #empres.email = row[8]
                #print(empres)
                for emppro in resultprojectemp:
                    if row[8] == emppro[3]:
                        empres['payload'].append(emppro)
                finalresult.append(empres)
            #print(finalresult)
            return render_template('projectemp.html', results=finalresult)
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/projecttoemp')
def projecttoemp():
    if session:
        if session['flag'] != 'U':
            cursor = db.cursor()
            sql = "SELECT * FROM projects"
            cursor.execute(sql)
            resultproject = cursor.fetchall()
            sql = "SELECT * FROM project_emp"
            cursor.execute(sql)
            resultprojectemp = cursor.fetchall()
            finalresult = []
            for row in resultproject:
                projectres = {'project_name' : row[2], 'project_code' : row[1], 'payload': []}
                #empres.name = row[1]
                #empres.email = row[8]
                #print(empres)
                for proemp in resultprojectemp:
                    if row[1] == proemp[7]:
                        projectres['payload'].append(proemp)
                finalresult.append(projectres)
            #print(finalresult)
            return render_template('projecttoemp.html', results=finalresult)
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/projectempall')
def projectempall():
    if session:
        if session['flag'] != 'U':
            cursor = db.cursor()
            sql = "SELECT * FROM project_emp"
            cursor.execute(sql)
            results = cursor.fetchall()
            #print(finalresult)
            return render_template('projectempall.html', results=results)
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/employees')
def showemployees():
    if session:
        if session['flag'] != 'U':
            cursor = db.cursor()
            sql = "SELECT * FROM emp_details"
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            return render_template('employees.html', results=results)
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/sheetentry')
def sheetentry():
    if session:
        if session['flag'] == 'U':
            cursor = db.cursor()
            sql = "SELECT * FROM emp_work where email = %s"
            cursor.execute(sql, session['username'])
            results = cursor.fetchall()
            cursor.close()
            return render_template('timesheetentry.html', results=results)
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/changepass', methods=['GET', 'POST'])
def changepass():
    cursor = db.cursor()
    sql = ("SELECT * FROM users where email = %s")
    cursor.execute(sql, request.form['email'])
    result = cursor.fetchone()
    if (result):
        if (result[2] == request.form['email']) and result[3] == request.form['opass'] and result[5] == 'Yes':
            query = """ UPDATE users
                        SET password = %s
                        WHERE email = %s """

            data = (encrypt('password', request.form['cpass']), request.form['email'])
            cursor.execute(query, data)
            db.commit()
            cursor.close()
            #db.close()
            flash("Your password changed successfully.", 'error')
        else:
            flash("Your old password is not correct.", 'error')
    else:
        flash("Your are not register user.", 'error')
    return redirect(url_for('__name__.loginshow'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cursor = db.cursor()
        sql = ("SELECT * FROM users where email = %s")
        email = request.form['email']
        cursor.execute(sql, request.form['email'])
        result = cursor.fetchone()
        cursor.close()
        #db.close()
        if request.form['email'] == result[2] and request.form['inputPassword'] == result[3] and result[5] == 'Yes':
            session['username'] = request.form['email']
            session['flag'] = result[4]
            session['name'] = result[1]
            if session['flag'] == 'SA':
                session['superadmin'] = True
            elif session['flag'] == 'A':
                session['admin'] = True
            else:
                session['user'] = True
            return redirect(url_for('__name__.show'))
    return redirect(url_for('__name__.loginshow'))

@bp.route('/saveproject', methods=['GET', 'POST'])
def saveproject():
    if session:
        if session['flag'] != 'U' and session['flag'] != 'A':
            cursor = db.cursor()
            if (request.form['project_id']):
                query = ("UPDATE projects SET project_code = %s, project_name = %s, client=%s, client_code=%s, status=%s, progress=%s, start_date=%s, end_date=%s, biling_contact=%s, bill_to_email=%s, about=%s WHERE id = %s")
                data_user = (request.form['pcode'], request.form['pname'], request.form['cname'], request.form['ccode'],
                request.form['pstatus'], request.form['progress'], request.form['sdate'], request.form['edate'], request.form['bcontact'], request.form['bemail'], request.form['aboutp'], int(request.form['project_id']) )
                cursor.execute(query, data_user)
                db.commit()
            else:
                add_user = ("INSERT INTO projects "
                           "(id, project_code, project_name, client, client_code, status, progress, start_date, end_date, biling_contact, bill_to_email, about) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                data_user = (0, request.form['pcode'], request.form['pname'], request.form['cname'], request.form['ccode'], request.form['pstatus'],
                request.form['progress'], request.form['sdate'], request.form['edate'], request.form['bcontact'], request.form['bemail'], request.form['aboutp'] )
                cursor.execute(add_user, data_user)
                db.commit()

            cursor.close()
            #return render_template('addprojects.html')
            return redirect(url_for('__name__.showprojects'))
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))


@bp.route('/saveemployee', methods=['GET', 'POST'])
def saveemployee():
    if session:
        if session['flag'] != 'U' and session['flag'] != 'A':
            cursor = db.cursor()
            if (request.form['emp_id']):
                query = ("UPDATE emp_details SET name = %s, ph1 = %s, ph2=%s, blood_group=%s, address=%s, emergency_contact_no=%s, gender=%s, email=%s, dob=%s, start_date=%s,"
                "end_date=%s, is_active=%s, employee=%s, hra=%s, lta=%s, uniform_allowance=%s, edu_allowance=%s, softfurnishing_allowance=%s, years=%s, food_coupon=%s, days=%s, vichle_engno=%s  WHERE id = %s")
                data_user = (request.form['ename'], request.form['phone1'], request.form['phone2'], request.form['bgroup'], request.form['address'],
                request.form['pcno'], request.form['gender'], request.form['oemail'], request.form['edob'], request.form['osdate'], request.form['oedate'],
                request.form['oeisactive'], request.form['oemptype'], request.form['ehra'], request.form['elta'], request.form['euallow'], request.form['oeduallow'],
                request.form['oesfallow'], request.form['oeyears'], request.form['oefood'], request.form['oedays'], request.form['oevengno'], request.form['emp_id'] )
                cursor.execute(query, data_user)
                db.commit()
            else:
                add_user = ("INSERT INTO emp_details "
                           "(id, name, ph1, ph2, blood_group, address, emergency_contact_no, gender, email, dob, start_date, end_date, is_active, employee, hra, lta, uniform_allowance, edu_allowance, softfurnishing_allowance, years, food_coupon, days, vichle_engno) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                data_user = (0, request.form['ename'], request.form['phone1'], request.form['phone2'], request.form['bgroup'], request.form['address'],
                request.form['pcno'], request.form['gender'], request.form['oemail'], request.form['edob'], request.form['osdate'], request.form['oedate'],
                request.form['oeisactive'], request.form['oemptype'], request.form['ehra'], request.form['elta'], request.form['euallow'], request.form['oeduallow'],
                request.form['oesfallow'], request.form['oeyears'], request.form['oefood'], request.form['oedays'], request.form['oevengno'] )
                cursor.execute(add_user, data_user)
                db.commit()

            cursor.close()
            #return render_template('addprojects.html')
            return redirect(url_for('__name__.showemployees'))
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('name', None)
    session.pop('flag', None)
    session.pop('superadmin', None)
    session.pop('admin', None)
    session.pop('user', None)
    #db.close()
    return redirect(url_for('__name__.loginshow'))

@bp.route('/showsignup')
def showsignup():
    return render_template('signup.html')

@bp.route('/addprojects')
def addprojects():
    if session:
        if session['flag'] != 'U':
            return render_template('addprojects.html', result=[])
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/showprojectempform')
def showprojectempform():
    if session:
        if session['flag'] != 'U':
            cursor = db.cursor()
            sql = "SELECT * FROM projects"
            cursor.execute(sql)
            resultsp = cursor.fetchall()
            sql = "SELECT * FROM emp_details"
            cursor.execute(sql)
            resultse = cursor.fetchall()
            cursor.close()
            return render_template('projectempform.html', resultsp=resultsp, resultse=resultse, resultid = [])
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/showempform')
def showempform():
    if session:
        if session['flag'] != 'U':
            return render_template('employeesform.html', result=[])
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/viewprofile')
def viewprofile():
    if session:
        cursor = db.cursor()
        cursor.execute('SELECT * from emp_details Where email = %s', [session['username']])
        result = cursor.fetchone()
        db.commit()
        cursor.close()
        return render_template('employeesform.html', result=result, view='yes')
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/users')
def showusers():
    if session:
        if session['flag'] != 'U':
            cursor = db.cursor()
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            #db.close()
            return render_template('users.html', results=results)
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/saveuser', methods=['GET', 'POST'])
def saveuser():
    if session:
        if session['flag'] != 'U' and session['flag'] != 'A':
            cursor = db.cursor()
            query = """ UPDATE users
                        SET user_type = %s, is_active = %s
                        WHERE id = %s """

            data = (request.form['utype'], request.form['ustatus'], int(request.form['user_id']))
            cursor.execute(query, data)
            db.commit()
            cursor.close()
            return redirect(url_for('__name__.showusers'))
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/savetimesheet', methods=['GET', 'POST'])
def savetimesheet():
    if session:
        if session['flag'] == 'U':
            cursor = db.cursor()
            projectnamecode = request.form['eproject']
            pronamecode = projectnamecode.split(',')
            if request.form['timesheet_id']:
                sql = "UPDATE emp_work SET emp_name=%s, project_name = %s, project_code = %s, hours = %s, email=%s, start_date=%s, end_date=%s, summary=%s, detail_summary=%s WHERE id = %s"
                data = (session['name'], pronamecode[0], pronamecode[1], request.form['ehours'], session['username'], request.form['tsdate'], request.form['tedate'], request.form['tsummary'], request.form['tactivity'], int(request.form['timesheet_id']))
                cursor.execute(sql, data)
                db.commit()
            else:
                sql = "SELECT id FROM emp_work WHERE email = %s AND project_code = %s AND (start_date = %s OR end_date = %s)"
                data = (session['username'], pronamecode[1], request.form['tsdate'], request.form['tedate'])
                cursor.execute(sql, data)
                result = cursor.fetchall()
                print(result)
                if result == ():
                    add_user = ("INSERT INTO emp_work "
                               "(id, emp_name, project_name, project_code, hours, email, start_date, end_date, summary, detail_summary) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                    data_user = (0, session['name'], pronamecode[0], pronamecode[1], request.form['ehours'], session['username'], request.form['tsdate'], request.form['tedate'], request.form['tsummary'], request.form['tactivity'])
                    cursor.execute(add_user, data_user)
                    db.commit()
                else:
                    flash("You tried to push a duplicate entry so kindly edit it.", 'error')
                    return redirect(url_for('__name__.show'))
            cursor.close()
            return redirect(url_for('__name__.sheetentry'))
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/saveprojectemp', methods=['GET', 'POST'])
def saveprojectemp():
    if session:
        if session['flag'] != 'U' and session['flag'] != 'A':
            cursor = db.cursor()
            if len(request.form['emppro_id']) != 0:
                add_user = "UPDATE project_emp SET is_active = %s, start_date = %s, end_date = %s WHERE id = %s"
                data_user = (request.form['epstatus'], request.form['epsdate'], request.form['epedate'], int(request.form['emppro_id']))
                cursor.execute(add_user, data_user)
                db.commit()
            else:
                tempnameemail = request.form['epname']
                temppnamepcode = request.form['eproject']
                empnameemail = tempnameemail.split(',')
                projectnamecode = temppnamepcode.split(',')
                sql = "SELECT * FROM project_emp where emp_email = %s and project_code = %s"
                data = (empnameemail[1], projectnamecode[1])
                cursor.execute(sql, data)
                result = cursor.fetchone()
                if result == None:
                    add_user = ("INSERT INTO project_emp "
                               "(id, emp_name, project_name, emp_email, is_active, start_date, end_date, project_code) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
                    data_user = (0, empnameemail[0], projectnamecode[0], empnameemail[1], request.form['epstatus'], request.form['epsdate'], request.form['epedate'], projectnamecode[1])
                    cursor.execute(add_user, data_user)
                    db.commit()
            cursor.close()
            return redirect(url_for('__name__.projectempall'))
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/projects')
def showprojects():
    if session:
        if session['flag'] != 'U':
            cursor = db.cursor()
            sql = "SELECT * FROM projects"
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            #db.close()
            return render_template('projects.html', results=results)
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/deleteproject/<int:p_id>')
def deleteproject(p_id):
    if session:
        if session['flag'] != 'U' and session['flag'] != 'A':
            pd_id = int(p_id)
            cursor = db.cursor()
            cursor.execute('DELETE from projects Where id = %s', [pd_id])
            db.commit()
            cursor.close()
            return redirect(url_for('__name__.showprojects'))
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/deleteuser/<int:u_id>')
def deleteuser(u_id):
    if session:
        if session['flag'] != 'U' and session['flag'] != 'A':
            ud_id = int(u_id)
            cursor = db.cursor()
            cursor.execute('DELETE from users Where id = %s', [ud_id])
            db.commit()
            cursor.close()
            return redirect(url_for('__name__.showusers'))
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/deleteemp/<int:e_id>')
def deleteemp(e_id):
    if session:
        if session['flag'] != 'U' and session['flag'] != 'A':
            ed_id = int(e_id)
            cursor = db.cursor()
            cursor.execute('DELETE from emp_details Where id = %s', [ed_id])
            db.commit()
            cursor.close()
            return redirect(url_for('__name__.showemployees'))
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/deletetimesheet/<int:ts_id>')
def deletetimesheet(ts_id):
    if session:
        if session['flag'] == 'U':
            tsd_id = int(ts_id)
            cursor = db.cursor()
            cursor.execute('DELETE from emp_work Where id = %s', [tsd_id])
            db.commit()
            cursor.close()
            return redirect(url_for('__name__.sheetentry'))
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/deleteempproject/<int:ep_id>')
def deleteempproject(ep_id):
    if session:
        if session['flag'] != 'U' and session['flag'] != 'A':
            epd_id = int(ep_id)
            cursor = db.cursor()
            cursor.execute('DELETE from project_emp Where id = %s', [epd_id])
            db.commit()
            cursor.close()
            return redirect(url_for('__name__.projectempall'))
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/editproject/<int:p_id>')
def editproject(p_id):
    if session:
        if session['flag'] != 'U' and session['flag'] != 'A':
            pe_id = int(p_id)
            cursor = db.cursor()
            cursor.execute('SELECT * from projects Where id = %s', [pe_id])
            result = cursor.fetchone()
            db.commit()
            cursor.close()
            return render_template('addprojects.html', result=result)
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/editemp/<int:e_id>')
def editemp(e_id):
    if session:
        if session['flag'] != 'U' and session['flag'] != 'A':
            ed_id = int(e_id)
            cursor = db.cursor()
            cursor.execute('SELECT * from emp_details Where id = %s', [ed_id])
            result = cursor.fetchone()
            db.commit()
            cursor.close()
            return render_template('employeesform.html', result=result)
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/editprojectemp/<int:epe_id>')
def editprojectemp(epe_id):
    if session:
        if session['flag'] != 'U' and session['flag'] != 'A':
            eped_id = int(epe_id)
            cursor = db.cursor()
            cursor.execute('SELECT * from project_emp Where id = %s', [eped_id])
            result = cursor.fetchone()
            resultsp = (result[2], result[7], result[4], result[5], result[6])
            resultse = (result[1], result[3])
            resultid = (result[0], result[1])
            cursor.close()
            return render_template('projectempform.html', resultsp=resultsp, resultse=resultse, resultid=resultid)
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))


@bp.route('/viewemp/<int:e_id>')
def viewemp(e_id):
    if session:
        if session['flag'] != 'U':
            ed_id = int(e_id)
            cursor = db.cursor()
            cursor.execute('SELECT * from emp_details Where id = %s', [ed_id])
            result = cursor.fetchone()
            db.commit()
            cursor.close()
            return render_template('employeesform.html', result=result, view='yes')
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/edituser/<int:u_id>')
def edituser(u_id):
    if session:
        if session['flag'] != 'U' and session['flag'] != 'A':
            ue_id = int(u_id)
            cursor = db.cursor()
            cursor.execute('SELECT * from users Where id = %s', [ue_id])
            result = cursor.fetchone()
            db.commit()
            cursor.close()
            return render_template('userform.html', result=result)
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/edittimesheet/<int:ts_id>')
def edittimesheet(ts_id):
    if session:
        if session['flag'] == 'U':
            tse_id = int(ts_id)
            cursor = db.cursor()
            cursor.execute('SELECT * from emp_work Where id = %s', [tse_id])
            results = cursor.fetchone()
            resultedit = (results[0], results[1])
            db.commit()
            cursor.close()
            ##resultedit.append(results[0])
            return render_template('home.html', results=results, resultedit=resultedit)
        else:
            return redirect(url_for('__name__.logout'))
    else:
        return redirect(url_for('__name__.loginshow'))

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    cursor = db.cursor()
    cursor.execute('SELECT * from emp_details Where email = %s', [request.form['email']])
    result = cursor.fetchone()
    db.commit()
    if result:
        add_user = ("INSERT INTO users "
                   "(id, name, email, password, user_type) "
                   "VALUES (%s, %s, %s, %s, %s)")
        data_user = (0, request.form['inputName'], request.form['email'], request.form['inputPassword'], 'U')
        cursor.execute(add_user, data_user)
        db.commit()
        cursor.close()
        #db.close()
        flash("You are successfully signed up.", 'error')
        return redirect(url_for('__name__.loginshow'))
    else:
        flash("You are not register with Nichesoft.", 'error')
        return redirect(url_for('__name__.loginshow'))
