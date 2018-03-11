#views.py
#Holds the various views that the flask app can return

from flask import render_template, request
from app import app
from models import *
from uuid import *
from playhouse import shortcuts
import json
import logging
import datetime
from babel.dates import format_timedelta

#Shamelessly taken from http://flask.pocoo.org/snippets/45/ - works well
def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

#Default index page, maybe change this to have an overview type page
@app.route('/')
def index():
    return render_template("index.html")

#Return an about page
@app.route('/about')
def about():
    return render_template("about.html")

'''
MACHINE STUFF BELOW
This section deals with endpoints handling machine stuff
'''
#Display a list of machines
@app.route('/machines')
def machines():

    #Woo pretty stuff!
    if request_wants_json():
        try:
            overallResult = []
            result = Machine.select().dicts().execute()
            for r in result:
                overallResult.append(r)
            #Dump the entire dict
            raise Exception("test error!")
            return json.dumps(overallResult)
        except Exception as ex:
            return json.dumps(str(ex))
    else:
        try:
            #Select all the machines in the DB
            return render_template("machines.html", machine_list=Machine.select())
        except Exception as ex:
            #Or if we get an error ugly print the error (for now)
            return "Error! %s" % str(ex)

    '''
    try:
        #Select all the machines in the DB
        return render_template("machines.html", machine_list=Machine.select())
    except Exception as ex:
        #Or if we get an error ugly print the error (for now)
        return "Error! %s" % str(ex)

    if request.headers['Content-Type'] == 'text/html' or request.headers['CONTENT_TYPE'] == 'text/html':
        try:
            #Select all the machines in the DB
            return render_template("machines.html", machine_list=Machine.select())
        except Exception as ex:
            #Or if we get an error ugly print the error (for now)
            return "Error! %s" % str(ex)

    elif request.headers['Content-Type'] == 'application/json':
        try:
            #Select all the machines in the DB
            overallResult = []
            result = Machine.select().dicts().execute()
            for r in result:
                overallResult.append(r)

            return json.dumps(overallResult)
        except Exception as ex:
            #Or if we get an error ugly print the error (for now)
            return json.dumps("Error! %s" % str(ex))

    else:
        return "415 Unsupported Media Type"

    overallResult = []
    result = Machine.select().dicts().execute()
    for r in result:
        overallResult.append(r)

    return json.dumps(overallResult)
    '''

#Display a machine
@app.route('/machines/<machine_uid>')
def machine(machine_uid):
    try:
        #Pass the machine name through
        machine_details = Machine.get(Machine.machineuid == machine_uid)
        last_usage = Log.select(Log, User).join(User, on=(Log.useruid==User.useruid)).where(Log.machineuid == machine_uid).order_by(Log.starttime.desc()).limit(25)

        # Calculate the time delta for the log display, and pretty-print it. Not sure this is
        # the best way to do this, suggestions welcome.
        for p in last_usage:
            timediff = p.endtime - p.starttime
            p.elapsed = format_timedelta(timediff, granularity="second", locale="en_GB")

        return render_template("machine.html", machine_details=machine_details, last_usage=last_usage)
    except Exception as ex:
        return "Error! %s" % str(ex)


#Register a new machine
@app.route('/machines/new', methods=['GET', 'POST'])
def newmachine():
    #Used to test that the database worked
    #Machine.create(creator='APITest', machinename='TestMachine', machineuid='MakeAProperUID', status=True)

    #Check if GET versus POST
    if request.method == 'GET':
        #If GET return the base form with UUID
        return render_template("newmachine.html", machine_uid=str(uuid4()))
    elif request.method == 'POST':
        #This will be POSTed data this time, try create a new machine
        try:
            Machine.create(creator="API", machinename=request.form['machinename'], machineuid=request.form['machineuid'], status=True)
            return render_template("newmachine.html", error=False, machine_uid=str(uuid4()))
        #Catch every exception so we can print out the error
        except Exception as ex:
            #Return with error, and set up form for a new UUID
            return render_template("newmachine.html", error=True, error_string=str(ex), machine_uid=str(uuid4()))

'''
USER STUFF BELOW!
This section deals with endpoints handling user stuff
'''
#Display a list of users
@app.route('/users')
def users():
    try:
        #Select all the machines in the DB
        return render_template("users.html", user_list=User.select())
    except Exception as ex:
        #Or if we get an error ugly print the error (for now)
        return "Error! %s" % str(ex)

#Display a user
@app.route('/users/<user_uid>')
def user(user_uid):
    try:
        #Pass the machine name through
        user_details = User.get(User.useruid == user_uid)
        last_usage = Log.select(Log, Machine).join(Machine, on=(Machine.machineuid==Log.machineuid)).where(Log.useruid == user_uid).order_by(Log.starttime.desc()).limit(25)

        # Calculate the time delta for the log display, and pretty-print it. Not sure this is
        # the best way to do this, suggestions welcome.
        for p in last_usage:
            timediff = p.endtime - p.starttime
            p.elapsed = format_timedelta(timediff, granularity="second", locale="en_GB")

        return render_template("user.html", user_details=user_details, last_usage=last_usage)

    except Exception as ex:
        return "Error! %s" % str(ex)

#Register a new user
@app.route('/users/new', methods=['GET', 'POST'])
def newuser():
    #Used to test that the database worked
    #Machine.create(creator='APITest', machinename='TestMachine', machineuid='MakeAProperUID', status=True)

    #Check if GET versus POST
    if request.method == 'GET':
        #If GET return the base form with UUID
        return render_template("newuser.html", user_uid=str(uuid4()))
    elif request.method == 'POST':
        #This will be POSTed data this time, try create a new user
        try:
            User.create(creator="API", username=request.form['username'], useruid=request.form['useruid'], carduid=request.form['carduid'], valid=True)
            return render_template("newuser.html", error=False, user_uid=str(uuid4()))
        #Catch every exception so we can print out the error
        except Exception as ex:
            #Return with error, and set up form for a new UUID
            return render_template("newuser.html", error=True, error_string=str(ex), user_uid=str(uuid4()))

#Display a list of permissions
@app.route('/permissions')
def permissions():
    try:
        return render_template("permissions.html", permission_list=Permission.select(Permission, User, Machine).join(User, on=(Permission.useruid == User.useruid).alias('user')).switch(Permission).join(Machine, on=(Permission.machineuid == Machine.machineuid).alias('machine')).where(Permission.useruid == User.useruid, Permission.machineuid == Machine.machineuid).execute())
    except Exception as ex:
        return "Error! %s" % str(ex)

#Register a new permission
@app.route('/permissions/new', methods=['GET', 'POST'])
def newpermission():
    #Used to test that the database worked
    #Machine.create(creator='APITest', machinename='TestMachine', machineuid='MakeAProperUID', status=True)

    #Check if GET versus POST
    if request.method == 'GET':
        #If GET return the base form
        return render_template("newpermission.html", user_list=User.select(), machine_list=Machine.select())
    elif request.method == 'POST':
        #This will be POSTed data this time, try create a new permission
        try:
            #This has to be put in, because, you know, the form doesn't return anything sensible :|
            if request.form.get('canuse'):
                canuse = True
            else:
                canuse = False

            if request.form.get('caninduct'):
                caninduct = True
            else:
                caninduct = False

            Permission.create(creator="API", machineuid=request.form['machineuid'], useruid=request.form['useruid'], caninduct=caninduct, canuse=canuse)
            return render_template("newpermission.html", user_list=User.select(), machine_list=Machine.select(), error=False)
        #Catch every exception so we can print out the error
        except Exception as ex:
            #Return with error, and set up form for a new UUID
            return render_template("newpermission.html", user_list=User.select(), machine_list=Machine.select(), error=True, error_string=str(ex))

#Return usage for a specific machine
#Deprecate once moved to a new page format
@app.route('/usage/<machine>')
def machineusage(machine):
    return render_template("usage.html", machine_name=machine)

#Check if a card is valid for use on a certain machine
@app.route('/canuse/<machine>/<card>')
def checkvalid(machine, card):
    # Subquery to consolidate the card ID request and limit response to one.
    userselect = User.select(User.useruid).where(User.carduid == card)
    result = Permission.select(Permission.canuse, Permission.caninduct).where(Permission.machineuid == machine).where(Permission.useruid == userselect).limit(1).dicts().execute()

    resultlist = []
    for r in result:
        resultlist.append(r)
    
    # If there wasn't anything in the returned result then deny access,
    # otherwise give out the result.
    if len (resultlist) != 0:
        return(json.dumps(resultlist))
    else:
        # Resort to denying access if there was no response.
        # Can this be less of a "literal string"?
        return "[{\"caninduct\": 0, \"canuse\": 0}]"
    
    '''
    if(result > 0):
        return(result)
    else:
        return("no result!")
    '''
'''
LOGGING
'''

@app.route('/log/new', methods=['POST'])
def logusage():
    try:
        # Force parsing as JSON even if content header is
        # incorrect, because we don't accept anything else.
        json = request.get_json(force=True)
    except Exception as ex:
        # Return a bad request if we aren't getting our JSON.
        # This could happen if the content type isn't set properly or if the JSON
        # is particularly malformed such that it can't even be
        print ("Bad JSON request.")
        print(ex)
        return "{\"error\":\"Bad JSON\"}", 400 # 400 BAD REQUEST

    try:
        log = Log()
        log.endtime = datetime.datetime.now()
        log.starttime = log.endtime - datetime.timedelta(seconds=int(json["elapsed"]))
        log.machineuid = json["machineuid"]

        # Check that the machine UID exists and is associated with a machine.
        machineQuery = Machine.select().where(Machine.machineuid == log.machineuid)
        if machineQuery.exists() is False:
            print ("Bad request, Machine UID doesn't exist.")
            return "{\"error\":\"Machine UID doesn't exist\"}", 400 # 400 BAD REQUEST

        # Check that the Card UID exists and is associated with a user UID. This is what
        # we need to associate the log request with.
        log.useruid = User.select(User.useruid).where(User.carduid == json["carduid"]).limit(1)
        if log.useruid is None:
            print ("Bad request, Card UID doesn't exist.")
            return "{\"error\":\"Card UID doesn't exist\"}", 400 # 400 BAD REQUEST

        # If we're debugging the App it would probably be nice to see all the json
        # and also to save it in the database for future lookup.
        # Otherwise store a readable note of seconds used.
        if app.debug is True:
            print(json)
            log.notes = json
        else:
            log.notes = json["elapsed"] + "s used"

    except (TypeError, ValueError) as ex:
        print ("TypeError or ValueError when populating new log from JSON.")
        print (json)
        print (ex)
        return "{\"error\":\"Bad JSON - bad value type or a value conversion error occurred.\"}", 400 # 400 BAD REQUEST

    try:
        log.save()
    except Exception as ex:
        # Had a problem saving the data to the database,
        # so return an internal server error.
        print("Error creating log in database.")
        print(ex)
        return "0", 500 # 500 SERVER ERROR

    # Return created response
    return "1", 201 # 201 CREATED
