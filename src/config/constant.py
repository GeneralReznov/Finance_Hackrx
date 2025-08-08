import os
from dotenv import load_dotenv
load_dotenv()
os.environ['GOOGLE_API_KEY'] = "AIzaSyCZGGDVIyjebUyHX8m0xO6f1pBD6KKjErc"

class GlobalState:
    def __init__(self):
        self.vector_store = None
        self.accepted_extensions = {
            ".pdf", ".docx", ".pptx", ".xlsx",
            ".png", ".jpg", ".jpeg", ".csv",
            ".json", ".txt" ,".ppt"
        }
        self.google_api_key = os.environ.get('GOOGLE_API_KEY')
        self.temp_paths = []
        self.links = [] 
        self.vector_store_path = []

global_state = GlobalState()
