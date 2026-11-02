class RiskEngine:

    def calculate_risk(
        self,
        is_authorized,
        zone_level="HIGH",
        duration=0
    ):

        # Authorized person
        if is_authorized:

            if zone_level == "CRITICAL":
                return {
                    "level": "MEDIUM",
                    "score": 40,
                    "reason": "Authorized person in critical zone"
                }

            return {
                "level": "LOW",
                "score": 10,
                "reason": "Authorized person entered restricted zone"
            }

        # Unknown person
        else:

            if zone_level == "CRITICAL":
                return {
                    "level": "CRITICAL",
                    "score": 100,
                    "reason": "Unknown person in critical zone"
                }

            if duration >= 30:
                return {
                    "level": "CRITICAL",
                    "score": 90,
                    "reason": "Unknown person remained in restricted zone"
                }

            return {
                "level": "HIGH",
                "score": 75,
                "reason": "Unknown person entered restricted zone"
            }
if __name__ == "__main__":

    risk = RiskEngine()

    print(
        risk.calculate_risk(
            is_authorized=True,
            zone_level="HIGH"
        )
    )

    print(
        risk.calculate_risk(
            is_authorized=False,
            zone_level="HIGH"
        )
    )

    print(
        risk.calculate_risk(
            is_authorized=False,
            zone_level="CRITICAL"
        )
    )