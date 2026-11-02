class Authorization:

    def __init__(self):

        self.authorized_people = {
            "A001": "Security Person 1",
            "A002": "Security Person 2",
            "A003": "Security Person 3"
        }


    def check(self, rfid_id):

        if rfid_id in self.authorized_people:

            return {
                "name": self.authorized_people[rfid_id],
                "authorized": True
            }

        return {
            "name": "Unknown Person",
            "authorized": False
        }

