from api_requests import ApiRequests
import asyncio
import sys

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Wrong arguments! Must receive \n1- First Election Round \n2- Second Election Round!" )
        quit()   
    api = ApiRequests()
    
    api.get_hash_mun_zon_sec(sys.argv[1])


