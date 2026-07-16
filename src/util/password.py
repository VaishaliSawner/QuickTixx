import bcrypt

def hash_password(password:str):
    password_bytes = password.encode("utf-8")
    salt_key =  bcrypt.gensalt(10)
    hashed_password = bcrypt.hashpw(password_bytes,salt_key)
    return hashed_password.decode("utf-8")

def verify_password(hashed_password:str,password:str):
    password_bytes = password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes,hashed_password_bytes)

