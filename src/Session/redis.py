import redis
import json
import uuid

# Your RAGPrompting class should be here or imported

# Redis session manager
class RedisSessionManager:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def create_session(self, user_data: dict):
        session_id = str(uuid.uuid4())
        self.redis.set(session_id, json.dumps(user_data))
        return session_id

    def get_session(self, session_id: str):
        data = self.redis.get(session_id)
        return json.loads(data) if data else None

    def delete_session(self, session_id: str):
        self.redis.delete(session_id)
        
    def update_session(self, session_id: str, user_data: dict):
        self.redis.set(session_id, json.dumps(user_data))
        
    def clear_sessions(self):
        self.redis.flushdb()
        
    def get_all_sessions(self):
        return {key.decode(): json.loads(value.decode()) for key, value in self.redis.scan_iter()}