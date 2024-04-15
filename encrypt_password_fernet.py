from cryptography.fernet import Fernet
import sys


#Funcion encriptar passwords, almacenamos en el mismo path el key.fernet que va a ser generico.
def encrypt_password(password, name):
    #Obtenemos la calve de cifrado.
    with open("key.fernet", "rb") as f:
        key = f.read()
        f.close()
    #Cargamos la key para usarla de encoder.
    fernet = Fernet(key)
    #Encriptamos la password
    encrypted_password = fernet.encrypt(password.encode())
    #Guardamos la contraseña cifrada en la misma ruta de ejecucion en la carpeta passwords.
    with open(f".\passwords\{name}.fernet", 'a') as file:
        file.write(encrypted_password.decode())
        file.close()
        
#Funcion para desencriptar contraseñas, hay que indicar el nombre del fichero con la contraseña cifrada.
def decrypt_password(name):
    with open("key.fernet", "rb") as f:
        key = f.read()
        f.close()
    fernet = Fernet(key)
    with open(f"./passwords/{name}.fernet", 'rb') as file:
        password = file.read()
    decrypted_password = fernet.decrypt(password)
    return decrypted_password.decode()

if __name__ == '__main__':
    encrypt_password(sys.argv[1],sys.argv[2])