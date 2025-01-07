from database import dispatcher

class User:
    current_user = None

    def __init__(self, username, password):
        self.user_id = dispatcher.execute(
            "SELECT id FROM user_data WHERE username = ? AND password = ?", (username, password)
        )[0]['id']
        print(self.user_id)
        self.username = username
        self.password = password

    @property
    def id(self):
        return self.user_id  # Return user_id when accessing `id`

    def get_flight_information(self):
        flight_query = "SELECT * FROM Flights WHERE user_id = ?"
        flights_result = dispatcher.execute(flight_query, (self.id,))  # Use self.id here
        if not flights_result:
            return None

        user_flights = []

        for flight in flights_result:
            flight_information = {
                "flight_id": int(flight["flight_id"]),
                "price": float(flight["price"]),
                "currency": flight["currency"],
                "number_of_seats": int(flight["number_of_seats"]),
                "segments": []
            }

            segment_query = "SELECT * FROM Segments WHERE flight_id = ?"
            segment_result = dispatcher.execute(segment_query, (flight["flight_id"],))
            if segment_result:
                for segment in segment_result:
                    flight_information["segments"].append({
                        "type": segment["type"],
                        "departure": segment["departure"],
                        "arrival": segment["arrival"],
                        "departure_time": segment["departure_time"],
                        "arrival_time": segment["arrival_time"]
                    })

            user_flights.append(flight_information)

        return user_flights

    def get_hotel_information(self):
        query = "SELECT * FROM Hotels WHERE user_id = ?"
        result = dispatcher.execute(query, (self.id,))
        return result
    
    def get_first_name(self):
        query = "SELECT first_name FROM user_data WHERE id = ?"
        result = dispatcher.execute(query, (self.id,))
        return result
    
    def get_last_name(self):
        query = "SELECT last_name FROM user_data WHERE id = ?"
        result = dispatcher.execute(query, (self.id,))
        return result

    @classmethod
    def login(cls, username, password):
        query = "SELECT * FROM user_data WHERE username = ? AND password = ?"
        result = dispatcher.execute(query, (username, password))
        if result:
            cls.current_user = cls(username, password)
            return cls.current_user
        return None

    @classmethod
    def get_current_user(cls):
        return cls.current_user
