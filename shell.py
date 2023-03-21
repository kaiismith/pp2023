import subprocess

while True:
    command = input("$ ")
    if not command:
        continue
    if ">" in command:
        output_redirect = command.split(">")[1].strip()
        command = command.split(">")[0].strip()
        with open(output_redirect, "w") as f:
            subprocess.run(command, shell=True, stdout=f)
    elif "<" in command:
        input_redirect = command.split("<")[1].strip()
        command = command.split("<")[0].strip()
        with open(input_redirect, "r") as f:
            subprocess.run(command, shell=True, stdin=f)
    elif "|" in command:
        commands = command.split("|")
        p = None
        for cmd in commands:
            cmd = cmd.strip()
            if not p:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            else:
                p = subprocess.Popen(cmd, shell=True, stdin=p.stdout, stdout=subprocess.PIPE)
        print(p.communicate()[0].decode())
    else:
        subprocess.run(command, shell=True)