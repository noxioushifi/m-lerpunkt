from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

url = "https://api.utilitycloud.app/weborder/v1/NewLead"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://klarkraft-weborder.utilitycloud.app",
    "Referer": "https://klarkraft-weborder.utilitycloud.app/",
    "Accept-Language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "tenant": "7080010002488"
}

def send_request(phone_number):
    payload = {
        "Phone": phone_number,
        "MockResponse": False,
        "SessionId": "sylw4me9pp",
        "Product": {
            "ProductId": "e62ded98bc14454a9fc1e9d6790dd69f",
            "ProductName": "Klarkraft strømavtale",
            "PrimaryProduct": True
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/get_info", methods=["POST"])
@app.route("/get_info", methods=["POST"])
def get_info():
    phone_number = request.form["phone_number"]
    response = send_request(phone_number)

    if response:
        lead_details = response.get("LeadDetails", {})
        accounting_point = lead_details.get("AccountingPoints", [])[0].get("AccountingPoint", {})

        first_name = lead_details.get("FirstName", "")
        last_name = lead_details.get("LastName", "")
        address = (
            f"{accounting_point.get('Address', {}).get('StreetName')} {accounting_point.get('Address', {}).get('BuildingNumber')}, {accounting_point.get('Address', {}).get('PostCode')} {accounting_point.get('Address', {}).get('CityName')}, {accounting_point.get('Address', {}).get('CountryCode')}")
        phone = lead_details.get("Phone", "")
        identification = accounting_point.get("Identification", "")
        meter_identification = accounting_point.get("MeterIdentification", "")
        forbruk = accounting_point.get("AnnualPeriodEstimatedMetrics", "")

        return jsonify({
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "phone": phone,
            "identification": identification,
            "meter_identification": meter_identification,
            "forbruk": forbruk
        })
    else:
        return jsonify({"error": "Failed to get a response."})


if __name__ == "__main__":
    app.run(debug=True)
