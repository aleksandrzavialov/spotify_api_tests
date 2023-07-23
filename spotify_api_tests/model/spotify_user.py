import os
from dataclasses import dataclass

@dataclass()
class SpotifyUser:
    name: str = os.getenv('user_name')
    email: str = os.getenv('user_mail')
    id: str = os.getenv('user_id')

