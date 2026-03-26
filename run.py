import os 
os.system("cd milvus;sudo docker-compose up -d;cd ..")
os.system("uvicorn main:app --reload ")