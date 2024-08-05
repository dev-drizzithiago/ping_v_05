from subprocess import run, PIPE

while True:
    valor_ping = run('ping ' + '192.168.0.1 ' + '-n 5 -w 1 ', stdout=PIPE)
    print(valor_ping.returncode)

    if valor_ping.returncode == 1:
        break
