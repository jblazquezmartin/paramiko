import paramiko
import time



count=int()
buff_string=str()
equipo=str()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('x.x.x.x', port=22,username='xxxxx', password='xxxxxx')
shell=ssh.invoke_shell()

shell.send('show virtual-interfaces' + '\n')
time.sleep(1)
while shell.recv_ready() == True: 

    buff_string += str(shell.recv(9999),'utf-8',errors='ignore')


print('\n'+'La Primera Salida es:')
print(buff_string +'\n' )
