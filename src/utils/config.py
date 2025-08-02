from dotenv import load_dotenv
import os

load_dotenv(rf'config\.env')

DATABASE_URL = os.getenv('DATABASE_URL')  
PATH_RAW = os.getenv('PATH_RAW')  
PATH_PROCESSED = os.getenv('PATH_PROCESSED')  
 
