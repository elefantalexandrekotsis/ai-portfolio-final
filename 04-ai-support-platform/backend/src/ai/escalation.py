class EscalationDetector:
    KEYWORDS = ["speak to human","talk to person","real person","manager","supervisor","lawyer","legal action"]
    def check(self, message, history):
        for kw in self.KEYWORDS:
            if kw in message.lower():
                return {"should_escalate":True,"reason":kw,"escalation_message":"Transferring to human agent. Please wait."}
        if len(history) > 10:
            return {"should_escalate":True,"reason":"Long conversation","escalation_message":"Connecting you with a specialist."}
        return {"should_escalate":False,"reason":None,"escalation_message":None}
