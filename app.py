from flask import Flask, render_template, request
import pickle
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Store expenses (keep AFTER imports, before usage)
expenses = []

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

# Chart function
def generate_chart():
    categories = {}

    for exp in expenses:
        cat = exp["category"]
        categories[cat] = categories.get(cat, 0) + exp["amount"]

    if categories:
        plt.figure()
        plt.bar(categories.keys(), categories.values())
        plt.xlabel("Category")
        plt.ylabel("Amount")
        plt.title("Spending by Category")

        # Ensure static folder exists
        if not os.path.exists("static"):
            os.makedirs("static")

        plt.savefig("static/chart.png")
        plt.close()

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

        # Store data
        expenses.append({
            "description": description,
            "amount": amount,
            "category": category
        })

        # Generate chart
        generate_chart()

    return render_template(
        "index.html",
        category=category,
        result=result,
        expenses=expenses
    )

if __name__ == "__main__":
    app.run(debug=True)