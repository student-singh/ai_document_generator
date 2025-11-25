from datetime import datetime
from bson import ObjectId

class Project:
    def __init__(self, user_id, title, doc_type, topic, structure=None, content=None, history=None, _id=None):
        self._id = ObjectId(_id) if _id else ObjectId()
        self.user_id = user_id
        self.title = title
        self.doc_type = doc_type
        self.topic = topic
        self.structure = structure or []
        self.content = content or {}  # { "0": {text: "", prompt_used: "", version: 1} }
        self.history = history or []
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}