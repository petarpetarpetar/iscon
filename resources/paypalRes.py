import os

from flask import jsonify, request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

import paypalrestsdk as pp
from resources.studentRes import Student

pp.configure(
    {
        "mode": "sandbox",
        "client_id": "ATTL_MehwSWrp7WdG3hA95gryoTnvIIWywaIgMqMeLGfzV4HrKr1XFf53sCP4noGnJKTcUxgujr8gQbN",
        "client_secret": "EP8QRkwnUu0fNNeALYSUiMbaWy4zVdVLIAW-PQEnlWjipW1McV5ImAuvsraNMtcdzCNdZW26ra3kUxNm",
  }
)


class PaypalCreatePayment(Resource):
    def post(self, amount):
        print(amount)
        amount = float(amount)
        payment = pp.Payment(
            {
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {"return_url": "http://92.168.137.80:5000/payment/execute", "cancel_url": "http://192.168.137.80:5000/add_funds"},
                "transactions": [
                    {
                        "item_list": {
                            "items": [{"name": "test balance", "sku": "12345", "price": amount, "currency": "USD", "quantity": 1}]
                        },
                        "amount": {"total": amount, "currency": "USD"},
                        "description": "This is the payment transaction description.",
                    }
                ],
            }
        )

        if payment.create():
            print("payment created!")
        else:
            print(payment.error)

        return jsonify({"paymentID": payment.id})


class PaypalExecutePayment(Resource):
    # @jwt_required() not working
    def post(self):
        print("payment")
        payment = pp.Payment.find(request.form["paymentID"])
        amount = float(payment["transactions"][0]["amount"]["total"])
        if payment.execute({"payer_id": request.form["payerID"]}):
            # Topping up the user's balance
            print(request.form["_user_id"])
            Student.topup(request.form["_user_id"], amount)
            print("payment executed successfully!")
            return jsonify({"success": True})
        else:
            print(payment.error)
        return jsonify({"success": False})
