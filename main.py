from datetime import datetime
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

spreadsheet_data = DataManager()
flight_search = FlightSearch()
send_notification = NotificationManager()

DEPARTURE_AIRPORT = "CLT"


def cheap_flight_data(flight_search_results):
    """Formats data returned by kiwi api for cheapest flight"""
    # separating date and time, reformatting
    leave_datetime = datetime.strptime(flight_search_results["route"][0]["local_departure"], "%Y-%m-%dT%H:%M:%S.000Z")
    leave_date = leave_datetime.strftime("%m-%d-%Y")
    leave_time = leave_datetime.strftime("%I:%M %p")
    return_datetime = datetime.strptime(flight_search_results["route"][-1]["local_arrival"], "%Y-%m-%dT%H:%M:%S.000Z")
    return_date = return_datetime.strftime("%m-%d-%Y")
    return_time = return_datetime.strftime("%I:%M %p")

    # creating dictionary of flight information in the correct format
    flight_data = {
        "price": flight_search_results["price"],
        "depart_city": flight_search_results["cityFrom"],
        "depart_code": flight_search_results["flyFrom"],
        "dest_city": flight_search_results["cityTo"],
        "dest_code": flight_search_results["flyTo"],
        "leave_date": leave_date,
        "leave_time": leave_time,
        "return_date": return_date,
        "return_time": return_time,
    }
    return flight_data


def format_message(flight_data):
    """Formats message sent via twilio api"""
    message_str = f"Low price alert! Only ${flight_data['price']} to fly from " \
                   f"{flight_data['depart_city']}-{flight_data['depart_code']} to " \
                  f"{flight_data['dest_city']}-{flight_data['dest_code']}, from {flight_data['leave_date']} at " \
                  f"{flight_data['leave_time']} to {flight_data['return_date']} at {flight_data['return_time']}."
    return message_str


# get spreadsheet data
data = DataManager.get_rows(spreadsheet_data)
# add IATA codes to rows where they are missing
for row in data["prices"]:
    if row["iataCode"] == "":
        # get city code from kiwi
        iata_code = flight_search.get_iata(row["city"])
        # update row via put request
        DataManager.add_iata(spreadsheet_data, row["id"], iata_code)
# print(data)

# getting flight info
for row in data["prices"]:
    max_price = row["lowestPrice"]
    flight_info = cheap_flight_data(flight_search.find_cheapest_flight(DEPARTURE_AIRPORT, row["iataCode"]))
    # sending notification for flights cheaper than max price
    if int(flight_info["price"]) <= int(max_price):
        send_notification.send_message(format_message(flight_info))
