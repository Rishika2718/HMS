
from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
from datetime import datetime

from models.patient import regpat, patlogin, updpat, viewpat, listdept, canappt, getpat, searchdoc,searchpat
from models.doctor import doclogin, addavail, getavail, docappt, statusupdate, addpattmt, todayappt, weekappt, s_doc, patdet
from models.admin import adminlog, dashboard, view_appt, search_doc, searchpat, add_doc, update_doc, view_doc, view_pat, blacklistpatient, update_pat, delete_doc, getpatient,listdocs
from models.appointment import slotbook, bookappt, cancelappt

app = Flask(__name__)
app.secret_key = '12345'

@app.route('/')
def index():
    return render_template('basic.html')

@app.route('/patient/register', methods=['GET', 'POST'])
def regpatient():
    if request.method == 'POST':
        pid = request.form['patient_id']
        pname = request.form['name']
        pmobile = request.form['mobile']
        pemail = request.form['email']
        gen = request.form['gender']
        dob = request.form['dob']
        address = request.form['address']
        bloodgrp = request.form.get('blood_group')
        optional = request.form.get('optional_contact')
        msg = regpat(pid, pname, pmobile, pemail, gen, dob, address, bloodgrp, optional)
        flash(msg)
        return redirect(url_for('patlog'))
    return render_template('patient_register.html')

@app.route('/patient/login', methods=['GET', 'POST'])
def patlog():
    if request.method == 'POST':
        pemail = request.form['email']
        pmobile = request.form['mobile']
        user = patlogin(pemail, pmobile)
        if user:
            session['patient_id'] = user[0]
            session['patient_name'] = user[1]
            return redirect(url_for('patdashbd'))
        flash('Wrong credentials')
    return render_template('patlogin.html')

@app.route('/patient/dashboard')
def patdashbd():
    if 'patient_id' not in session:
        return redirect(url_for('patlog'))
    
    pid = session.get('patient_id')
    all = viewpat(pid)
    coming = []
    past = []
    today = datetime.today().date()
    
    for row in all:
        app_date = datetime.strptime(row[2], "%Y-%m-%d").date()
        status = row[4]
        if app_date >= today and status == "Booked":
            coming.append(row)
        else:
            past.append(row)
    
    return render_template("patdbd.html", coming=coming, past=past)

@app.route('/patient/book', methods=['POST'])
def bookpat():
    pid = session.get('patient_id')
    if not pid:
        return redirect(url_for('patlog'))
    
    doc_id = request.form['doc_id']
    date = request.form['date']
    time = request.form['time']
    
    if slotbook(doc_id, date, time):
        flash("Slot already booked for this doctor")
        return redirect(url_for('patdashbd'))
    
    msg = bookappt(pid, doc_id, date, time)
    flash(msg)
    return redirect(url_for('patdashbd'))

@app.route('/patient/cancel/<int:app_id>')
def cancelappt(app_id):
    if 'patient_id' not in session:
        return redirect(url_for('patlog'))
    
    result = cancelappt(app_id)
    flash(result)
    return redirect(url_for('patdashbd'))

@app.route('/patient/edit', methods=['GET', 'POST'])
def patientupd():
    if "patient_id" not in session:
        return redirect(url_for('patlog'))

    pid = session['patient_id']
    patient = getpat(pid)

    if request.method == 'POST':
        pname = request.form['name']
        pmobile = request.form['mobile']
        pemail = request.form['email']
        paddress = request.form['address']
        poptional = request.form.get('optional', '')
        msg = updpat(pid, pid, pname, pmobile, pemail, paddress, poptional)
        flash(msg)
        return redirect(url_for('patdashbd'))
    
    return render_template('patient_edit.html', patient=patient)

@app.route('/patient/departments')
def patient_departments():
    dts = listdept()
    return render_template("patient_departments.html", departments=dts)

@app.route('/patient/doctors')
def patdoc():
    doctors = searchdoc()
    return render_template("patient_doctors.html", doctors=doctors)

@app.route('/patient/search', methods=['GET'])
def patsearch():
    query = request.args.get('q', '')
    results = searchdoc(query)
    return render_template("patient_search.html", results=results)

@app.route('/patient/history')
def patdetails():
    if "patient_id" not in session:
        return redirect(url_for('patlog'))
    
    pid = session["patient_id"]
    history = viewpat(pid)
    return render_template("patient_history.html", history=history)


@app.route('/doctor/login', methods=['GET', 'POST'])
def doclog():
    if request.method == 'POST':
        demail = request.form['email']
        dmobile = request.form['mobile']
        user = doclogin(dmobile, demail)
        if user:
            session['doctor_id'] = user[0]
            session['doctor_name'] = user[1]
            return redirect(url_for('doctor_dashboard'))
        flash('Wrong credentials')
    return render_template('doctor_login.html')

@app.route('/doctor/dashboard')
def doctor_dashboard():
    if 'doctor_id' not in session:
        return redirect(url_for('doclog'))
    
    doc_id = session.get('doctor_id')
    today = todayappt(doc_id)
    week = weekappt(doc_id)
    patients = docappt(doc_id)
    
    return render_template('doctor_dashboard.html', today=today, week=week, patients=patients)

@app.route('/doctor/mark_status', methods=['POST'])
def statusapdate():
    if 'doctor_id' not in session:
        return redirect(url_for('doclog'))
    
    app_id = request.form['app_id']
    status = request.form['status']
    result = statusupdate(app_id, status)
    flash(result)
    return redirect(url_for('doctor_dashboard'))

@app.route('/doctor/add_treatment', methods=['POST'])
def doctmt():
    if 'doctor_id' not in session:
        return redirect(url_for('doclog'))
    
    app_id = request.form['app_id']
    diagnosis = request.form['diagnosis']
    prescription = request.form['prescription']
    followup = request.form.get('followup')
    notes = request.form.get('notes')
    cost = request.form.get('cost')
    
    msg = addpattmt(app_id, diagnosis, prescription, followup, notes, cost)
    flash(msg)
    return redirect(url_for('doctor_dashboard'))

@app.route('/doctor/availability', methods=['GET', 'POST'])
def docavail():
    if 'doctor_id' not in session:
        return redirect(url_for('doclog'))
    
    doc_id = session.get('doctor_id')
    
    if request.method == 'POST':
        avail = {d: request.form.get(d, '') for d in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']}
        addavail(doc_id, avail)
        flash("Availability updated")
        return redirect(url_for('doctor_dashboard'))
    
    current_avail = getavail(doc_id)
    return render_template('doctor_availability.html', availability=current_avail)

@app.route('/doctor/patient_history/<patient_id>')
def doctor_view_patient_history(patient_id):
    if 'doctor_id' not in session:
        return redirect(url_for('doclog'))

    history = patdet(patient_id)
    return render_template("doctor_view_patient_history.html", history=history)

@app.route('/admin/login', methods=['GET', 'POST'])
def adlogin():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        success, name = adminlog(username, pwd)
        if success:
            session['admin'] = username
            session['admin_name'] = name
            return redirect(url_for('admindashboard'))
        flash('Invalid admin credentials')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admindashboard():
    if 'admin' not in session:
        return redirect(url_for('adlogin'))
    
    dc, pc, ac = dashboard()
    appts = view_appt()
    return render_template('admin_dashboard.html', doctors=dc, patients=pc, appointments=ac, appt_list=appts)

@app.route('/admin/search_doctor', methods=['GET', 'POST'])
def search_doctor():
    if 'admin' not in session:
        return redirect(url_for('adlogin'))    
    data = []
    if request.method == 'POST':
        d_id = request.form.get('doctor_id')
        specialization = request.form.get('specialization')
        if d_id:
            doc = view_doc(d_id)
            if doc:
                data.append((doc[0], doc[1], doc[2], doc[3], doc[4],doc[5]))
        elif specialization:
            doctors = search_doc(specialization)
            for d in doctors:
                data.append((d[0], d[1], d[2], d[3], d[4],d[5]))
    elif request.method == 'GET':
        q = request.args.get('q', '').strip()
        if q:
            doc = view_doc(q)
            if doc:
                data.append((doc[0], doc[1], doc[2], doc[3], doc[4],doc[5]))
            else:
                ds = search_doc(q)
                if ds:
                    for d in ds:
                        data.append((d[0], d[1], d[2], d[3], d[4],d[5]))
    return render_template('adminsearchdoc.html', results=data)


@app.route('/admin/search_patient', methods=['GET'])
def asearchpat():
    if 'admin' not in session:
        return redirect(url_for('adlogin'))
    q = request.args.get('q', '')
    data = searchpat(q)
    return render_template('adminsearchpat.html', results=data)

@app.route('/admin/add_doctor', methods=['GET', 'POST'])
def adadddoc():
    if 'admin' not in session:
        return redirect(url_for('adlogin'))
    
    if request.method == 'POST':
        d_id = request.form['doctor_id']
        name = request.form['name']
        demail = request.form['email']
        dmobile = request.form['mobile']
        dtiming = request.form['timing']
        deptid = request.form['department']
        msg = add_doc(d_id, name, dmobile, demail, dtiming, deptid)
        flash(msg)
        return redirect(url_for('admindashboard'))
    
    return render_template('adminnewdoc.html')

@app.route('/admin/edit_doctor', methods=['GET'])
def edit_docmain():
    if 'admin' not in session:
        return redirect(url_for('adlogin'))
    all_doctors = listdocs()
    return render_template('choosedoc.html', doctors=all_doctors)
@app.route('/admin/edit_doctorselect', methods=['GET'])
def edit_docselect():
    doctor_id = request.args.get('doctor_id')
    return redirect(url_for('adupdatedoc', doctor_id=doctor_id))


@app.route('/admin/edit_doctor/<doctor_id>', methods=['GET', 'POST'])
def adupdatedoc(doctor_id):
    if 'admin' not in session:
        return redirect(url_for('adlogin'))
    doctor = view_doc(doctor_id)
    if doctor is None:
            flash("Doctor does not exist!", "danger")
            return redirect(url_for('search_doctor'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        dept = request.form.get('department')
        timing = request.form.get('timing')
        msg = update_doc(doctor_id, name, mobile, email, timing, dept)
        flash(msg)
        return redirect(url_for('admindashboard'))
    return render_template('adminupddoc.html', doctor=doctor)

@app.route('/admin/edit_patient/<patient_id>', methods=['GET', 'POST'])
def adupdatepat(patient_id):
    if 'admin' not in session:
        return redirect(url_for('adlogin'))
    
    patient = getpatient(patient_id)
    
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        msg = update_pat(patient_id, name, mobile, email, address)
        flash(msg)
        return redirect(url_for('admindashboard'))
    
    return render_template('admin_edit_patient.html', patient=patient)

@app.route('/admin/delete_doctor/<doctor_id>')
def adremovedoc(doctor_id):
    if 'admin' not in session:
        return redirect(url_for('adlogin'))

    msg = delete_doc(doctor_id)
    flash(msg)
    return redirect(url_for('admindashboard'))

@app.route('/admin/delete_patient/<patient_id>')
def admin_delete_patient(patient_id):
    if 'admin' not in session:
        return redirect(url_for('adlogin'))

    msg = blacklistpatient(patient_id)
    flash(msg)
    return redirect(url_for('admindashboard'))

@app.route('/admin/view_doctor/<doctor_id>')
def adgetdoc(doctor_id):
    if 'admin' not in session:
        return redirect(url_for('adlogin'))
    
    doc = viewdoc(doctor_id)
    return render_template('adminviewdoc.html', doctor=doc)

@app.route('/admin/view_patient/<patient_id>')
def adgetpatient(patient_id):
    if 'admin' not in session:
        return redirect(url_for('adlogin'))
    
    pat = view_pat(patient_id)
    return render_template('adminviepat.html', patient=pat)

@app.route('/admin/all_appointments')
def adallappts():
    if 'admin' not in session:
        return redirect(url_for('adlogin'))
    
    appts = view_appt()
    today = datetime.today().date()
    coming = []
    past = []
    
    for a in appts:
        date = datetime.strptime(a[3], "%Y-%m-%d").date()
        if date >= today:
            coming.append(a)
        else:
            past.append(a)
    
    return render_template("adminallappt.html", upcoming=coming, past=past)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)