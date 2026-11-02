from datetime import datetime


class EventManager:

    def __init__(self):
        # People currently inside restricted zones
        self.people_inside = set()

    def check_person(self, person_id, inside_zone):

        # Person is inside the restricted zone
        if inside_zone:

            # New entry
            if person_id not in self.people_inside:

                self.people_inside.add(person_id)

                event = {
                    "person_id": person_id,
                    "event": "Restricted Zone Intrusion",
                    "zone": "Restricted Zone",
                    "time": datetime.now().strftime("%H:%M:%S")
                }

                return event

        # Person is outside the zone
        else:

            # Person has left the zone
            if person_id in self.people_inside:
                self.people_inside.remove(person_id)

        return None

