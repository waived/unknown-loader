┐ ┌  ┬─┐  ┐┌─  ┬─┐  ┌─┐  ┐ ┌  ┬─┐
│ │  │ │  ├┴┐  │ │  │ │  │││  │ │
└─┘  ┘ ┘  ┴ ┴  ┘ ┘  └─┘  └┴┘  ┘ ┘

Unknown Loader is C2 demonstration in Python that conducts silent file uploads+execution.

It manages to run C, PY, SH, and ELF files, but can be modified to handle more file operations.

The C2/CNC (command-and-control) infrastructure is based on the standard client-server model, and
can handle multiple concurrent connections. No encryption/encoding is used for this POC.

C2 FEATURES:
    CLEAR ---
    Refreshes the terminal environment.

    EXIT ---
    Cleanly exits Unknown Loader, ending the TCP-listener, heartbeat (keep-alive) routine,
    TCP broadcast routine, and unbinding the socket,

BACKDOOR FEATURES:
    DISCONNECT ---
    Forces all backdoors to disconnect from C2. client.py backdoor remains intact.

    RECONNECT ---
    Forces a TCP-reset from all backdoor connections to the C2.

    UNINSTALL ---
    Termination of connection to the C2 + self-destruct. Process hangs in memory for a while.

    EXEC ---
    Downloads file to infected device from URL and executes.

    PERSIST ---
    Attempt to modify local-user cron tab and add backdoor startup entry.

AUTHOR'S NOTE:
    The client.py backdoor has versbose output. This helps with debugging and making
    sense of what is going on. Of course, this feature also helped with developement.
    This can be removed without issue. Additionally, many authors comments are put into
    both the server and the client. These can also be removed. 

    Furthermore, in the client.py backdoor, the IP of the C2 server is '0.0.0.0'
    The port is set to 4444. Both will need to be modified to support your own C2.

LEGAL: 
    By downloading/running this script, you consent to the included LEGAL.txt agreement.

TIP: This loader is meant for UNIX/LINUX device platforms. It is ineffective on Windows
     environments unless proper changes are made.
