from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"reply": "Send me a message and I’ll try to help!"})

    lower = message.lower()

    if "order" in lower:
        reply = "To track your order, visit the Orders page and enter your order number. If you’d like, I can walk you through it step by step."
    elif "return" in lower or "refund" in lower:
        reply = "Our return policy allows returns within 30 days of delivery for unused items in original packaging. I can share the full policy or help with a return request."
    elif "account" in lower or "password" in lower or "email" in lower:
        reply = "You can update your account details from the My Account section. If you’re locked out, we can help you reset your password securely."
    elif "shipping" in lower or "delivery" in lower:
        reply = "Most domestic orders ship within 2–5 business days. Tracking details are sent as soon as the order is dispatched."
    elif "cancel" in lower:
        reply = "Order cancellations are usually possible before fulfillment. If your order has already shipped, we can help you with the next steps."
    else:
        reply = f"I hear you: “{message}”. This is a demo support assistant, so I can help with common support topics like shipping, returns, tracking, and account updates."

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
