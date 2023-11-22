from flask import Flask
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import urllib.parse


username=urllib.parse.quote_plus('yash7232')
password=urllib.parse.quote_plus('Yash@7232')

app = Flask(__name__)

# #configuring MongoDB
client = MongoClient(f'mongodb+srv://{username}:{password}@cluster0.kn66rfv.mongodb.net/your_database?retryWrites=true&w=majority')
db = client['log_database']
logs_collection = db['logs']
logs_collection.create_index([('message', 'text')])


# Provide real-time log ingestion and searching capabilities.
@app.route('/ingest', methods=['POST'])
def ingest_log():
    log_data = request.get_json()
    logs_collection.insert_one(log_data)
    return jsonify({"message": "Log ingested successfully"}), 201


#landing Page
@app.route('/')
def index():
    return render_template('index.html',  query_params={},errors=[])

#Implemeted Realtime Search functionality
@app.route('/search', methods=['GET'])
def search_logs():
    error=[]
    query_params = request.args.to_dict()
    today_datetime = datetime.utcnow()
    today_datetime = today_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # Allow combining multiple filters and removing empty parameters
    query_params = {k: v for k, v in query_params.items() if v}
    parameters=query_params.copy()

    # print(query_params)
    print(parameters)
    
    # Utilized regular(regex) expressions for search
    # Created a regex pattern for partial matching in the 'message' field
    if 'message' in query_params:
        regex_pattern = f'.*{query_params["message"]}.*'
        query_params['message'] = {'$regex': regex_pattern, '$options': 'i'}

    # Implemented search within specific date ranges.
    start_date = query_params.get('start_date')
    end_date = query_params.get('end_date')

    '''  removing the start_date from query_parms and end_date from query_parms
         removing them was important beacuse other wise mongodb query won't work
         because the 'start_date','end_date' aslo become the part of the query but we dont have 
         these feilds  in the database
    '''
    query_params.pop('start_date', None)
    query_params.pop('end_date', None)

    if start_date or end_date:
        try:
            validate_date(start_date,error,"start date")
            validate_date(end_date,error,"end date")

            if len(error)>1:
                    return render_template('index.html',  query_params=parameters,errors=error)

            # Add timestamp range to query parameters
            query_params['timestamp'] = {'$gte': start_date, '$lte': end_date}
        except ValueError as e:
            error.append(e)

    result = list(logs_collection.find(query_params, {'_id': 0}))
    

    # Pass query parameters to the template for rendering
    return render_template('index.html', logs=result, query_params=parameters, errors=error)


#this function validates the date
def validate_date(date, errors,name):
    try:
        # Parse the date string into a datetime object
        date_obj = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')

        # Extract year, month, and day from the datetime object
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day

        # Validate the year
        if year > 3000:
            errors.append(f"Enter a proper year in { name} feild ; it should be within 3000.")

        # Validate the month
        if month not in range(1, 13):
            errors.append(f"Wrong month entered in {name} feild ! Month should be in the range 1 to 12.")
            
        # Validate the day
        if day not in range(1, 32):
            errors.append(f"Wrong date entered in {name} feild! Date should be in the range 1 to 31.")
            
    except ValueError as e:
        errors.append(f"Invalid date format in {name} feild! Please enter the date in the format 'YYYY-MM-DDTHH:mm:ssZ'.")
    

    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0' ,port=3000)
