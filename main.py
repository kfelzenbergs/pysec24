import paramiko
import json


# define a list of servers
servers = [
    "p15v",
    "x1",
]

header = """
    --- OS Version "crawler" ---
    Author: Kristaps
    Release date: 23.11.2024
    Course: Pitons drošības testētājiem
"""

results = []
server_data_template = {
    "HOST": "",
    "VERSION": "",
    "VERSION_CODENAME": ""
}


# connect to each server
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


for server in servers:
    # print("-"*50)
    ssh.connect(
        hostname=server,
        username="user",
        password="datasec24"
    )

    # get os version
    command = "cat /etc/*-release | grep VERSION"
    stdin, stdout, stderr = ssh.exec_command(command)
    stdin.close()
    result = stdout.readlines()

    server_data = {}
    for line in result:
        fields = line.strip().split("=")
        server_data[fields[0]] = fields[1]

    
    server_data["HOST"] = server
    

    # get running processes
    command = "ps axfu"
    stdin, stdout, stderr = ssh.exec_command(command)
    stdin.close()
    process_list = stdout.readlines()

    server_data["process_count"] = len(process_list)
    # print(server, server_data)
    results.append(server_data)
    # print(results)


print(json.dumps(results))
