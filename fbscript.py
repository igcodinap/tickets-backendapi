import json
import facebook

def main():
    token = {"EAALShho8E80BAN9rSjWcHCdIuffH9p4nFi7gMJBTF0o8i7FpZCvdjhZAhlXtxJzy9vmIwmB1HfVxAvTyteEkVRDtUhvupOd3TnS8xNjDoiFhsGZC9RJvVgI5RXqQ8zYJ2cUFJmrWzVlgFfILETEGgSwKznsFj1ZAqZAR4IeG653k7SBaAdIcNPkWVhDOSzLEl378hVMQfLtBkl3tJMaNaV8YTjce6NlwUQVEj1kLtmAZDZD"}
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

            print(event_name)
            print(event_id)
            print(description)
            print(city)
            print(street)
            print(lat)
            print(longi)
            print(start_time)
            print(end_time)
            readingevent +=1
            print("*********************")


        

if __name__ =="__main__":
    main()
