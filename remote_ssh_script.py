#!/usr/bin/env python3
"""
A simple SSH connection script using paramiko.
"""

import paramiko
import getpass


def connect_ssh(host, port, username):
    """
    Connect to a remote host via SSH.
    """
    try:
        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to remote host
        password = getpass.getpass("Enter password for {}@{}: ".format(username, host))
        client.connect(host, port, username, password)
        
        print("✅ Successfully connected to {}@{}:{}".format(username, host, port))
        
        return client
        
    except Exception as e:
        print("❌ Connection failed: {}".format(str(e)))
        return None


def execute_command(client, command):
    """
    Execute a command on the remote host.
    """
    try:
        stdin, stdout, stderr = client.exec_command(command)
        
        print("Output:")
        for line in stdout:
            print(line.strip())
            
        if stderr:
            print("Error:")
            for line in stderr:
                print(line.strip())
                
        return stdout, stderr
        
    except Exception as e:
        print("❌ Command failed: {}".format(str(e)))
        return None, None


def main():
    # Connection parameters (update with your information)
    HOST = "192.168.1.100"
    PORT = 22
    USERNAME = getpass.getuser()
    
    # Connect to remote host
    client = connect_ssh(HOST, PORT, USERNAME)
    
    if client:
        # Execute commands
        execute_command(client, "uname -a")
        execute_command(client, "whoami")
        
        # Close connection
        client.close()
        print("\n✅ Connection closed")


if __name__ == "__main__":
    main()