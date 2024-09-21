from flask import Flask, request, jsonify, render_template
from Form_link_email import send_email
import sqlite3
 
app = Flask(__name__)
 
# Your email credentials.
SENDER_EMAIL = 'ts4235762@gmail.com'
SENDER_PASSWORD = 'ypwz xwyj wufc eglc'
JOB_ROLE = "Software Engineer"
GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSdt-jRV3uf0hMh5tvlkdEKE1pTVztmLXfA4ezY-MIAco4CKSw/viewform?vc=0&c=0&w=1&flr=0"
IMAGE_PATH = "C:/Users/dhans/Downloads/WhatsApp Image 2024-09-19 at 23.02.58_4dc12f66.jpg"
 

 
@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/get_selected_candidates', methods=['GET'])
def get_selected_candidates():
    conn = sqlite3.connect('hushhushDB.db') 
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM selected_users")
    candidates = cursor.fetchall()
    conn.close()
    return jsonify([{'name': name, 'email': email} for name, email in candidates])
 
@app.route('/send_email', methods=['POST'])
def send_email_route():
    data = request.json
    recipient_email = data.get('email')
    recipient_name = data.get('name')
 
    try:
        send_email(SENDER_EMAIL, SENDER_PASSWORD, recipient_email, recipient_name, JOB_ROLE, GOOGLE_FORM_LINK, IMAGE_PATH)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
 



 
if __name__ == '__main__':
    app.run(debug=True, port=3000)