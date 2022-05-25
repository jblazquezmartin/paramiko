import paramiko
import time
import sys
import logging
import os
import re


# Prepare logger
logger = logging.getLogger('IPandVlan')
logHandler = logging.FileHandler('IPandVlan.log')
logFormatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logHandler.setFormatter(logFormatter)
logger.addHandler(logHandler)
logger.setLevel(logging.DEBUG)   # Set logging level of script
# logging.getLogger("paramiko").setLevel(logging.DEBUG) # Set logging level of paramiko backend

# Set key variables
hosts = ['x.x.x.x','x.x.x.x']   # List of SBCs
username = 'xxxxxx'
password='xxxxxx'



def execute(channel, cmd):
    try:
        cmd = cmd.strip('\n')
        channel.send(cmd + '\n' )

        buff=''
        while not buff.endswith('# ') and not buff.endswith('> '):
            respuesta = channel.recv(9999).decode("utf-8")
            buff += respuesta
        return buff
    except socket.timeout:
        logger.error ('Unable to send/Receive data before socket timeout.')

    except:
        logger.error ('Unknown error occured while trying to execute command.')

    return None
   
        


def connectSSH(host):
    i = 1
    while True:
        logger.info('Trying to connect to ' + host + ' (' + str(i) + '/3)')

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host,username=username, password=password)
            logger.info('Connected to ' + host)

            return ssh
        except paramiko.AuthenticationException:
            logger.error('Authentication failed when connecting to ' + host)
            return None

        except:
            logger.warning('Could not SSH to ' + host + ', wait and try again.')
            i += 1
            time.sleep(2)

        # If we could not connect within time limit
        if i == 2:
            logger.error('Could not connect to ' + host  + '. Giving up.')
            return None



def closeConnections():
    
    try:
        ssh.close()
        logger.info('SSH connection closed.')
    except:
        logger.warning('Unable to close SSH connection, was is opened?')

# Starting Execution here
try:
    # Start loop through list of all hosts
    for host in hosts:
        # Try to connect via SSH to host
        ssh = connectSSH(host)
        

        # If the returned connection is None, skip host and move to next
        if ssh is None:
            logger.warning('Skipping ' + host + ', moving to next host.')
            continue

        # Invoke interactive shell to host
        channel = ssh.invoke_shell()
        # Try to execute display cfg version command
        logger.info('Vlan and IP´s in ' + host )
        resp = execute(channel, 'show virtual-interfaces')
        resp = execute(channel, 'show virtual-interfaces')
        logger.info( host +'  '+ resp )
        #print(resp1)
        if resp is None:
            logger.warning('Executing command on ' + host + ' failed, moving to next host.')
            closeConnections()
            continue

        try:
            currentRev = re.search('%vlan%', resp).group(0)
            logger.info('Current vlan' + host + ' is ' + currentRev)
        except AttributeError:
            logger.error('Unexpected response:\n' + resp)
            logger.warning('Unable to get config revision from ' + host + ', moving to next host.')
            closeConnections()
            continue
        closeConnections()
        
        

        
except Exception as e:
    logger.critical(e)        
