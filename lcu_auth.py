import psutil

def get_lcu_credentials():
    for proc in psutil.process_iter(['name', 'cmdline']):
        if proc.info['name'] == 'LeagueClientUx.exe':
            port = None
            token = None

            for arg in proc.info['cmdline']:
                if arg.startswith('--app-port='):
                    port = arg.split('=')[1]
                elif arg.startswith('--remoting-auth-token='):
                    token = arg.split('=')[1]

            if port and token:
                return port, token

    raise RuntimeError("League Client not running")
    