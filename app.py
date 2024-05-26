Enter fifrom flask import Flask, jsonify, request, make_response,send_file, redirect, url_for
from flask_pymongo import PyMongo
import json
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

app = Flask(__name__)

# Ρύθμιση της MongoDB URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/pspi"
mongo = PyMongo(app)


@app.route('/')
def home():
   return send_file('homepage.html')

@app.route('/products')
def products():
    return send_file('products.html')
    
    
@app.route('/homepage.html')
def redirect_to_homepage():
    return send_file('homepage.html')

@app.route('/products.html')
def redirect_to_products_page():
    return redirect(url_for('products'))
    
        
@app.route('/logo.png')
def logo():
    return send_file('logo.png')
    
@app.route('/image-1.jpg')
def image1():
    return send_file("image-1.jpg")
    
@app.route('/image-2.jpg')
def image2():
    return send_file('image-2.jpg')
 
@app.route('/image-3.jpg')
def image3():
    return send_file('image-3.jpg')
    
@app.route('/products.css')
def products_css():
    return send_file('products.css')
 
@app.route('/products.js')
def products_js():
    return send_file('products.js')
     
@app.route('/homepage.css')
def homepage_css():
    return send_file('homepage.css')


@app.route('/add', methods=['POST'])
def add():
    new_product = request.json
    
    if not new_product:
        return jsonify({"error": "Invalid input"}), 400
    
    try:
        exists = mongo.db.products.find_one({"Name": new_product["Name"]})
        if exists:
            # Διαγραφή υπάρχοντος εγγράφου
            mongo.db.products.delete_one({"Name": new_product["Name"]})

        # Προσθήκη νέου εγγράφου
        mongo.db.products.insert_one(new_product)
        return jsonify({"message": "Document added!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search')
def search():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Name parameter is required"}), 400

    try:
        results = mongo.db.products.find({"Name": name})
        products = []
        for result in results:
            product = {
                "ID": result.get("ID"),
                "Name": result.get("Name"),
                "Production_Year": result.get("Production_Year"),
                "Price": result.get("Price"),
                "Color": result.get("Color"),
                "Size": result.get("Size")
            }
            products.append(product)
        
        response = make_response(json.dumps({"products": products}, ensure_ascii=False))
        response.mimetype = 'application/json'
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/content-based-filtering', methods=['POST'])
def content_based_filtering():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    try:
        input_product = {
            "Name": data["Name"],
            "Production_Year": data["Production_Year"],
            "Price": data["Price"],
            "Color": data["Color"],
            "Size": data["Size"]
        }
        
        def cosine_similarity(vec1, vec2):
            dot_product = np.dot(vec1, vec2)
            norm_vec1 = np.linalg.norm(vec1)
            norm_vec2 = np.linalg.norm(vec2)
            return dot_product / (norm_vec1 * norm_vec2)

        input_vector = np.array([
            input_product["Production_Year"],
            input_product["Price"],
            input_product["Color"],
            input_product["Size"]
        ])

        results = mongo.db.products.find()
        similar_products = []

        for result in results:
            product_vector = np.array([
                result["Production_Year"],
                result["Price"],
                result["Color"],
                result["Size"]
            ])
            similarity = cosine_similarity(input_vector, product_vector)
            print("Similarity with", result["Name"], ":", similarity)  # Προσθήκη εκτυπώσεων εδώ
            if similarity > 0.7:
                similar_products.append(result["Name"])

        return jsonify({"similar_products": similar_products})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/crawler')
def crawler():
    semester = request.args.get('semester')
    if not semester:
        return jsonify({"error": "Parameter 'semester' is required"}), 400

    try:
        # Δημιουργία του Selenium Chrome WebDriver χωρίς το όρισμα options
        driver = webdriver.Chrome(ChromeDriverManager().install())

        # Κατασκευή του URL με βάση το εξάμηνο που δόθηκε ως παράμετρο
        url = f"https://qa.auth.gr/el/x/studyguide/600000438/{semester}"
        
        # Μετάβαση στο URL
        driver.get(url)

        # Αναζήτηση των στοιχείων των μαθημάτων
        courses = driver.find_elements(By.XPATH, "//div[@class='element-details']//a[@class='link-to-course']")
        course_names = [course.text for course in courses]

        # Κλείσιμο του WebDriver
        driver.quit()

        return jsonify({"courses": course_names})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


 


if __name__ == '__main__':
    app.run(debug=True)
le contents here
