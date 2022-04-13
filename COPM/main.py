from clipboard import copy, paste
import hashlib
from sys import argv
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
from time import sleep
import tkinter as tk
import pwd
import grp

if os.path.exists(os.getcwd()+'/.flag'):
    try:
        print('Unflagging')
        if os.path.exists(os.getcwd()+'/.passCache'):
            os.remove(os.getcwd()+'/.passCache')
        if os.path.exists(os.getcwd()+'/.nameCache'):
            os.remove(os.getcwd()+'/.nameCache')
        os.remove('.flag')
    except PermissionError:
        print('Run as root through terminal to secure passwords')

if not os.path.exists(os.getcwd()+'/.passCache'):
    print('Password cache does not exist, creating now')
    try:
        with open('.passCache', 'x') as f:
            f.close()
        #os.chmod(os.getcwd()+'/.passCache', 773)
        uid = pwd.getpwnam(os.getlogin()).pw_uid
        gid = grp.getgrnam('root').gr_gid
        os.chown(os.getcwd()+'/.passCache', uid, gid)
        if pwd.getpwuid(os.stat(os.getcwd()+'/.passCache').st_uid).pw_name == uid and pwd.getpwuid(os.stat(os.getcwd()+'/.passCache').st_gid).pw_name == gid and oct(os.stat(os.getcwd()+'/.passCache').st_mode)[-3]+oct(os.stat(os.getcwd()+'/.passCache').st_mode)[-2]+oct(os.stat(os.getcwd()+'/.passCache').st_mode)[-1] == '770':
            print('Password cache created successfully')
        else:
            print('Password cache permissions corrupted, may be insecure')
    except PermissionError:
        print('Operation Failed, run as root through terminal for initial setup')
        with open('.flag', 'x') as f:
            f.close()
        exit()
if not os.path.exists(os.getcwd()+'/.nameCache'):
    try:
        print('Name cache does not exist, creating now')
        with open('.nameCache', 'x') as f:
            f.close()
        uid = pwd.getpwnam(os.getlogin()).pw_uid
        gid = grp.getgrnam('root').gr_gid
        #os.chmod(os.getcwd()+'/.nameCache', 773)
        os.chown(os.getcwd()+'/.nameCache', uid, gid)
        if pwd.getpwuid(os.stat(os.getcwd()+'/.passCache').st_uid).pw_name == uid and pwd.getpwuid(os.stat(os.getcwd()+'/.passCache').st_gid).pw_name == gid and oct(os.stat(os.getcwd()+'/.passCache').st_mode)[-3]+oct(os.stat(os.getcwd()+'/.passCache').st_mode)[-2]+oct(os.stat(os.getcwd()+'/.passCache').st_mode)[-1] == '770':
            print('Name cache created successfully')
        else:
            print('Name cache permissions corrupted')
    except PermissionError:
        print('Operation Failed, run as root through terminal for initial setup')
        with open('.flag', 'x') as f:
            f.close()
        exit()
    

def enter():
    global ent_pass
    global inp
    inp = ent_pass.get()
    root.destroy()

def passwordBox(text):
    global ent_pass
    global root
    root = tk.Tk()

    lbl_buffer = tk.Label(height=2, text=text, bg='white')
    lbl_buffer.pack()

    ent_pass = tk.Entry(width=25, show='●')
    ent_pass.pack()

    btn_enter = tk.Button(width=20, height=1, text='Enter', command=enter)
    btn_enter.pack()

    ent_pass.focus()

    root.title = 'Enter Password'
    root.configure(bg='white')
    root.geometry('300x100')
    root.mainloop()

    return inp

backend = default_backend()
salt = b'Z\xd1\xb5\xed\xef\xcbdi\x96\xf5\x1f\x0c$\x86\xeb\xcf'

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=backend
)

if len(argv) <= 1:
    function = input('> ')
    function = '-' + function 
    if len(function.lower()) > 2:
        function = '-' + function
    argv.append(function.lower())
    if function.lower() in ['-n', '-r', '--new', '--read']:
        argv.append(input('name: '))

if (len(argv) > 1 and argv[1].lower() in ['-n', '--new']):
    inp = bytes(passwordBox('Master Password: ').encode())
    key = base64.urlsafe_b64encode(kdf.derive(inp))

    f = Fernet(key)
    newPass = passwordBox('Password: ')
    encPass = f.encrypt(newPass.encode())
    decPass = str(f.decrypt(encPass))[2:-1]
    
    with open('.passCache', 'ab') as passCache:
        passCache.write(encPass)
        passCache.write(bytes('__newline__'.encode()))
        
        passCache.close()

    with open('.nameCache', 'a') as nameCache:
        nameCache.write(f'{argv[2]}\n')
        
        nameCache.close()

elif (len(argv) > 1 and argv[1].lower() in ['-r', '--read']):
    with open('.passCache', 'rb') as passCache:
        passwordsRaw = passCache.read()
        passwordsRaw = str(passwordsRaw)[2:-1].split('__newline__')
        passwordsRaw.remove('')
        passwordsRaw = [bytes(i.encode()) for i in passwordsRaw]
        passCache.close()

    with open('.nameCache', 'r') as nameCache:
        names = nameCache.readlines()
        for i in range(len(names)):
            names[i] = names[i].replace('\n', '')
        nameCache.close()

    for i in names:
        if i == argv[2]:
            inp = bytes(passwordBox('Master Password: ').encode())
            key = base64.urlsafe_b64encode(kdf.derive(inp))
            f = Fernet(key)
            decPass = str(f.decrypt(passwordsRaw[names.index(i)]))
    clipCache = paste()
    copy(str(decPass)[2:-1])
    print('copied password for 10 seconds')
    sleep(10)
    for i in range(30):
        copy(i)
        sleep(.02)
    sleep(.05)
    copy(clipCache)
    print('restored clipboard')

elif (len(argv) > 1 and argv[1].lower() in ['-l', '--list']):
    with open('.nameCache', 'r') as nameCache:
        names = nameCache.readlines()
        for i in range(len(names)):
            names[i] = names[i].replace('\n', '')
        nameCache.close()

    print('Accounts:')
    if names:
        print(', '.join(names))
    else:
        print('None')

elif (len(argv) > 1 and argv[1].lower() in ['-t', '--truncate']):
    print('truncating password history')
    with open('.passCache', 'w') as passCache:
        passCache.truncate()
        passCache.close()
    with open('.nameCache', 'w') as nameCache:
        nameCache.truncate()
        nameCache.close()
else:
    print('Usage:')
    print('python main.py {option} [args]')
    print('If you are using COPM from IDLE respond to the prompt (> ) using the following commands, but excluding the - or --, and do not include args.')
    print('')
    print('Options:')
    print('-l --list              List registered accounts.')
    print('-t --truncate          Remove all accounts and passwords.')
    print('-n --new               Create a new account under [arg].')
    print('-r --read              Retrieve the password ender account [arg].')
    print('')
