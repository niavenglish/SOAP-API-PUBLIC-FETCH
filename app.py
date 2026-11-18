
from flask import Flask, request, jsonify
from zeep import Client
from zeep.exceptions import Fault
from zeep.transports import Transport
from requests import Session
from requests.exceptions import RequestException

app = Flask(__name__)

WSDL_URL = "http://www.dneonline.com/calculator.asmx?WSDL"


def validate_number(value, field_name):
    # Only allow whole numbers between 1 and 100
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be a whole number.")

    try:
        number = int(value)
    except (TypeError, ValueError, OverflowError):
        raise ValueError(f"{field_name} must be a whole number.")

    if str(number) != str(value).strip():
        raise ValueError(f"{field_name} must be a whole number.")

    if not 1 <= number <= 100:
        raise ValueError(
            f"{field_name} must be between 1 and 100."
        )

    return number


def calculate(first_number, second_number):
    a = validate_number(first_number, "First number")
    b = validate_number(second_number, "Second number")

    session = Session()
    session.trust_env = True
    transport = Transport(session=session, timeout=10,
                          operation_timeout=10)

    
    client = Client(wsdl=WSDL_URL, transport=transport)

    
    result = client.service.Add(intA=a, intB=b)

    
    return {
        "first_number": a,
        "second_number": b,
        "result": int(result)
    }


def process_request(first_number, second_number):
    try:
        result = calculate(first_number, second_number)
        return jsonify({
            "message": "Calculation completed successfully",
            "data": result
        }), 200

    except ValueError as exc:
        return jsonify({
            "error": f"Input validation failed: {exc}"
        }), 400

    except Fault as exc:
        return jsonify({
            "error": f"SOAP service returned a fault: {exc}"
        }), 502

    except (RequestException, Exception) as exc:
        app.logger.exception("SOAP request failed")
        return jsonify({
            "error": f"Unable to complete SOAP request: {exc}"
        }), 502


# GET endpoint
@app.route("/calculate", methods=["GET"])
def get_calculation():
    first = request.args.get("a")
    second = request.args.get("b")
    return process_request(first, second)


# POST endpoint
@app.route("/calculate", methods=["POST"])
def post_calculation():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A valid JSON object is required."
        }), 400

    return process_request(data.get("a"), data.get("b"))


if __name__ == "__main__":
    app.run(debug=True)
