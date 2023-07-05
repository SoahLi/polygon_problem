import subprocess
def killall():
    print("hello")
    command = "killall Python"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        print("Command executed successfully.")
        print("Output:", output.decode())
    else:
        print("Error:", error.decode())
killall()