import pydantic
import dotenv


class Config(pydantic.BaseSettings):
    base_url: str = 'https://accounts.spotify.com'
    api_url: str = 'https://api.spotify.com'
    permission_list: str = 'user-top-read, playlist-read-private, playlist-modify-public, playlist-modify-private, user-library-read, user-read-private, user-read-email, user-follow-modify, user-follow-read, user-library-modify'
    driver_name = 'firefox'
    browser_version = '98.0'
    hold_driver_at_exit: bool = False
    window_width: int = 1920
    window_height: int = 1080
    timeout: float = 3.0
    headless: bool = False


dotenv.load_dotenv()
config = Config(dotenv.find_dotenv('.env'))
