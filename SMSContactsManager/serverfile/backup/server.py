from flask import Flask, request, jsonify
import mysql.connector
import json
import os

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the path to the config.json file relative to the script directory
config_file_path = os.path.join(script_dir, '..', 'config.json')

# Load the configuration from the config.json file
with open(config_file_path) as f:
    config = json.load(f)

app = Flask(__name__)


with open('config.json') as f:
    config = json.load(f)

user_id = input("Please enter an ID: ")
config["user_id"] = user_id

mydb = mysql.connector.connect(
    host=config["host"],
    user=config["user"],
    password=config["password"],
    database=config["database"]
)
mycursor = mydb.cursor()
mycursor.execute("""CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    phone_number VARCHAR(255),
                    message TEXT,
                    user_id VARCHAR(255)
                )""")


@app.route('/send_sms', methods=['POST'])
def send_sms():
    phone_number = request.json['phone_number']
    message = request.json['message']

    query = "INSERT INTO messages (phone_number, message, user_id) VALUES (%s, %s, %s)"
    mycursor.execute(query, (phone_number, message, config['user_id']))
    mydb.commit()

    return jsonify({"status": "success", "message": f"Message is ready to be sent to {phone_number}"})



@app.route('/get_messages', methods=['GET'])
def get_messages():
    mycursor.execute("SELECT * FROM messages")
    result = mycursor.fetchall()
    messages = []

    for row in result:
        message_data = {
            "id": row[0],
            "phone_number": row[1],
            "message": row[2],
            "user": row[3]
        }
        messages.append(message_data)

    return jsonify({"status": "success", "messages": messages})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
