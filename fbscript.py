import json
import facebook
from models import db, User, Event, favorite, attendance, Auth, Calendar, Category, Facebook


def main():
    token = {"EAALShho8E80BAFC1d96qFYVYlO5yB3FRjnmA9iqPWVs4vUnmumKjd013f16XXXfKJnSJvB8L8fVnlmNZBSHP3XSuaSTJFgNIW2bqM8BsoHvi0CG5MSQZBm7u1n9pWpXC8843dkWEVJ9ZC5nPGCwCFOZCa0Ur8Ee1NXQyb0ZArT382nae29Lk4p3drtV0y6wxe4QwZBCyr3ZBpZCOHuvJwQ7o3vvxE0CBE1acH4BKKmbUKwZDZD"}
    graph = facebook.GraphAPI(token)

    fields = ['name,email, events']

    ids = [10220832650024954]
    
    def exists(var):
        if var:
            return var
        else:
            return ""

    for id in ids:
        profile = graph.get_object(id, fields = fields)
        """print(json.dumps(profile, indent=4))"""
        data = json.dumps(profile, indent=4)
        print(type(data))
        decoded_data = json.loads(data)
        """print(type(decoded_data))"""
        events = decoded_data["events"]["data"]
        eventsqty = len(events)
        readingevent = 0
        while readingevent < eventsqty:
            """print(decoded_data["events"]["data"][readingevent])"""
            event_id = exists(decoded_data["events"]["data"][readingevent].get("id"))
            event_name = exists(decoded_data["events"]["data"][readingevent].get("name"))
            description = exists(decoded_data["events"]["data"][readingevent].get("description"))
            city = exists(decoded_data["events"]["data"][readingevent]["place"]["location"].get("city"))
            street = exists(decoded_data["events"]["data"][readingevent]["place"]["location"].get("street"))
            lat = exists(decoded_data["events"]["data"][readingevent]["place"]["location"].get("latitude"))
            longi = exists(decoded_data["events"]["data"][readingevent]["place"]["location"].get("longitude"))
            start_time = exists(decoded_data["events"]["data"][readingevent].get("start_time"))
            end_time = exists(decoded_data["events"]["data"][readingevent].get("end_time"))

            event = Event()
            event.event_name = event_name
            event.description = description
            event.start_time = start_time
            event.end_time = end_time
            event.city = city
            event.street = street
            event.lat = lat
            event.longi = longi
        
            db.session.add(event)

            db.session.commit()
            print("Success")


        

if __name__ =="__main__":
    main()
