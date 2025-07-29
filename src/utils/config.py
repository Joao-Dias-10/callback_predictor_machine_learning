from dotenv import load_dotenv
import os

load_dotenv(rf'config\.env')

TESTE = os.getenv('TESTE')  
