from dataclasses import dataclass


@dataclass()
class SpotifyPlaylist:
    name: str
    description: str
    public: bool = False

