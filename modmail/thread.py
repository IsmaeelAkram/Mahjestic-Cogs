class Thread:
    def __init__(self, member_id: int, messages: list, created_at: int):
        self.member_id = member_id
        self.messages = messages
        self.created_at = created_at

    def json(self):
        return {"member_id": self.member_id, "messages": self.messages, "created_at": self.created_at}
    
     