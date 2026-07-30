class RiskScorer:

    @staticmethod
    def calculate(cvss):

        if cvss is None:
            return "UNKNOWN"

        score = float(cvss)

        if score >= 9:
            return "CRITICAL"

        if score >= 7:
            return "HIGH"

        if score >= 4:
            return "MEDIUM"

        return "LOW"
