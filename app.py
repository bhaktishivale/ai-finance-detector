from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Smart spending detection
def detect_spending(amount, category):
    if category == "Food" and amount > 300:
        return "⚠️ High spending on food!"
    elif category == "Shopping" and amount > 1000:
        return "⚠️ Too much shopping!"
    elif category == "Bills" and amount > 1500:
        return "⚠️ High bill detected!"
    else:
        return "✅ Spending looks normal."

@app.route("/", methods=["GET", "POST"])
def home():
    category = ""
    result = ""

    if request.method == "POST":
        description = request.form["description"]
        amount = int(request.form["amount"])

        # Predict category
        desc_vec = vectorizer.transform([description])
        category = model.predict(desc_vec)[0]

        # Get insight
        result = detect_spending(amount, category)

    return render_template("index.html", category=category, result=result)

if __name__ == "__main__":
    app.run(debug=True)