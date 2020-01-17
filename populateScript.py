import json
import facebook
from flask import Flask, jsonify, request
from models import (
    db,
    User,
    Event,
    favorite,
    attendance,
    Auth,
    Calendar,
    Category,
    fbUser,
    fbCalendar,
    fbattendance,
    fbfavorite
)
from trainedClassifier import clf


def exists(var):
    if var:
        return var
    else:
        return ""

def categoryClassification(somedescription):
    category_classification = clf.String(somedescription)
    return category_classification

def main():

    token = {
        "EAALShho8E80BAEhHcgUyeKi0VwHamG0lZAMiSLmqTyXqkqCW5fRLpr10gIUoZC2MGnfnYYrPkIkZC7LGFZBYa5OzHv9BHaZCYrQSg2GF2r6JBmEDGpgyisucFoPCPDBZB8DJjDAZCdON33TdnmSCOxAPcc4YEZCZBZChMZD"
    }
    graph = facebook.GraphAPI(token)

    fields = ["name,email, events"]

    ids = [10220832650024954]
    


    for id in ids:
        profile = graph.get_object(id, fields=fields)
        data = json.dumps(profile, indent=4)
        decoded_data = json.loads(data)
        events = decoded_data["events"]["data"]
        eventsqty = len(events)
        readingevent = 0
        while readingevent < eventsqty:
            event_id = exists(decoded_data["events"]["data"][readingevent].get("id"))
            event_name = exists(
                decoded_data["events"]["data"][readingevent].get("name")
            )
            description = exists(
                decoded_data["events"]["data"][readingevent].get("description")
            )
            city = exists(
                decoded_data["events"]["data"][readingevent]["place"]["location"].get("city")
            )
            street = exists(
                decoded_data["events"]["data"][readingevent]["place"]["location"].get("street")
            )
            lat = exists(
                decoded_data["events"]["data"][readingevent]["place"]["location"].get("latitude")
            )
            longi = exists(
                decoded_data["events"]["data"][readingevent]["place"]["location"].get("longitude")
            )
            start_time_raw = exists(
                decoded_data["events"]["data"][readingevent].get("start_time")
            )
            end_time_raw = exists(
                decoded_data["events"]["data"][readingevent].get("end_time")
            )

            determinedCategory = categoryClassification(event_name)
            start_time = start_time_raw.replace('T', ' ').replace('-0300', '')
            end_time = end_time_raw.replace('T', ' ').replace('-0300', '')

            event = Event()
            event.event_id = event_id
            event.event_name = event_name
            event.description = description
            event.event_category = determinedCategory
            event.start_time = start_time
            event.end_time = end_time
            event.city = city
            event.street = street
            event.is_canceled = False
            event.lat = lat
            event.longi = longi

            if Event.query.get(event_id):
                readingevent +=1
            else:
                db.session.add(event)
                readingevent +=1
        db.session.commit()
    return jsonify({'msg': 'Success'}), 200


if __name__ == "__main__":
    main()
