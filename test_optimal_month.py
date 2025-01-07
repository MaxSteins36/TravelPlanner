import asyncio
import unittest
from unittest.mock import patch, AsyncMock
from flask import Flask, jsonify, Blueprint, request

optimal_month_blueprint = Blueprint('optimal_month', __name__)

async def get_access_token():
    return "mocked_access_token"

async def split_month_call_api(access_token, origin, destination, month, dif_day, adults):
    return [
        {
            "departure_time": "2025-04-03T08:30:00",
            "price": 638.62,
            "currency": "EUR",
            "airline": "MF",
            "return_date": "2025-04-08T19:40:00",
            "segmentId": "65",
            "cabin": "ECONOMY",
            "id": "#1",
        },
        {
            "departure_time": "2025-04-02T08:15:00",
            "price": 855.98,
            "currency": "EUR",
            "airline": "CX",
            "return_date": "2025-04-08T22:15:00",
            "segmentId": "25",
            "cabin": "PREMIUM_ECONOMY",
            "id": "#2",
        },
        {
            "departure_time": "2025-04-02T09:05:00",
            "price": 915.25,
            "currency": "EUR",
            "airline": "CX",
            "return_date": "2025-04-08T22:15:00",
            "segmentId": "15",
            "cabin": "BUSINESS",
            "id": "#3",
        },
    ]

@optimal_month_blueprint.route('/get_optimal_month', methods=['POST'])
async def get_optimal_month():
    data = request.get_json()
    access_token = await get_access_token()
    if not access_token:
        return jsonify({"error": "Access token retrieval failed", "optimal_month_results": []}), 200

    results = await split_month_call_api(
        access_token,
        data["origin"],
        data["destination"],
        data["month"],
        data["dif_day"],
        data["adults"],
    )

    return jsonify({"optimal_month_results": results}), 200

class TestOptimalMonth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.register_blueprint(optimal_month_blueprint)
        cls.client = cls.app.test_client()

    @patch("optimal_month.get_access_token", new_callable=AsyncMock)
    @patch("optimal_month.split_month_call_api", new_callable=AsyncMock)
    def test_get_optimal_month_success(self, mock_split_month_call_api, mock_get_access_token):
        mock_get_access_token.return_value = "mocked_access_token"
        mock_split_month_call_api.return_value = [
            {
                "departure_time": "2025-04-03T08:30:00",
                "price": 638.62,
                "currency": "EUR",
                "airline": "MF",
                "return_date": "2025-04-08T19:40:00",
                "segmentId": "65",
                "cabin": "ECONOMY",
                "id": "#1",
            },
            {
                "departure_time": "2025-04-02T08:15:00",
                "price": 855.98,
                "currency": "EUR",
                "airline": "CX",
                "return_date": "2025-04-08T22:15:00",
                "segmentId": "25",
                "cabin": "PREMIUM_ECONOMY",
                "id": "#2",
            },
        ]

        request_data = {
            "origin": "JFK",
            "destination": "LAX",
            "month": "January",
            "dif_day": 5,
            "adults": 2,
        }

        with self.app.test_client() as client:
            response = client.post(
                "/get_optimal_month",
                json=request_data,
            )
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn("optimal_month_results", data)
            self.assertEqual(len(data["optimal_month_results"]), 2)  # Two results
            self.assertEqual(data["optimal_month_results"][0]["id"], "#1")

    @patch("optimal_month.get_access_token", new_callable=AsyncMock)
    def test_get_optimal_month_access_token_failure(self, mock_get_access_token):
        mock_get_access_token.return_value = None

        request_data = {
            "origin": "JFK",
            "destination": "LAX",
            "month": "February",
            "dif_day": 7,
            "adults": 1,
        }

        with self.app.test_client() as client:
            response = client.post(
                "/get_optimal_month",
                json=request_data,
            )
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn("optimal_month_results", data)
            self.assertEqual(len(data["optimal_month_results"]), 0)