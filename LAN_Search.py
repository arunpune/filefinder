import platform
import paramiko
import tkinter as tk
from tkinter import filedialog

ssh_keyfile = input("Enter the path to the private key file: ")

# Create an SSH client object
ssh = paramiko.SSHClient()

# Automatically add the remote host key
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Load the private key file
key = paramiko.RSAKey.from_private_key_file(ssh_keyfile)

# Prompt the user to enter the IP addresses to search
print("Enter the IP addresses of the systems to search, separated by commas(for example: 192.168.1.100, 192.168.1.101, 192.168.1.102):")
ip_addresses_input = input()
ip_addresses = [address.strip() for address in ip_addresses_input.split(',')]

for ip_address in ip_addresses:
    ssh_username = input("Enter the SSH username for {}: ".format(ip_address))
    print(f'Connecting to {ip_address}...')
    # Connect to the VM using SSH and authenticate using public key
    ssh.connect(ip_address, username=ssh_username, pkey=key)
    print(f'Connected to {ip_address}.\n')

# Detect the current operating system and execute platform-specific code
    if platform.system() == 'Windows':
    # Windows-specific code here
        process_cmd = 'tasklist /FI "IMAGENAME eq {process_name}"'
    else:
    # Linux-specific code here
        process_cmd = 'ps aux | grep {process_name}'

# Prompt the user to enter the path to search for files (linux or windows specific)
    search_path = input("Enter the path to search for files: ")

# Prompt the user to select which types of model files to search for
    print("Which types of model files would you like to search for?")
    print("1. TensorFlow (.pb)")
    print("2. PyTorch (.pt)")
    print("3. ONNX (.onnx)")
    model_choices = input("Enter your choice(s), separated by commas: ")
    model_extensions = []
    if '1' in model_choices:
        model_extensions.append('pb')
    if '2' in model_choices:
        model_extensions.append('pt')
    if '3' in model_choices:
        model_extensions.append('onnx')

# Prompt the user to enter which processes to search for
    process_choices = input("Which processes would you like to search for? Enter the name(s) or keyword(s), separated by commas: ")
    process_keywords = process_choices.split(',')
    
# Search for files with the selected extensions in the model directory
    print(f'Searching for model files on {ip_address}...')
    extensions = (model_extensions)
    find_command_template = f'find {search_path} -type f \( -name "*.{extensions}" \) 2>/dev/null'
    for extension in extensions:
        find_command = find_command_template.format(search_path=search_path, extension=extension)
        stdin, stdout, stderr = ssh.exec_command(find_command)
        model_files = stdout.read().decode().strip().split('\n')
        if len(model_files) > 0:
            print(f'The following {extension} model files were found on {ip_address}:')
            for f in model_files:
                print(f)
        else:
            print(f'No {extension} model files were found on {ip_address}.')
        
        # Search for running processes with the selected keywords
    print(f'Searching for processes on {ip_address}...')
    for keyword in process_keywords:
        process_cmd = process_cmd.replace('{process_name}', keyword)
        stdin, stdout, stderr = ssh.exec_command(process_cmd)
        processes = stdout.read().decode().strip().split('\n')
        if len(processes) > 0:
            print(f'The following processes were found on {ip_address} matching the keyword "{keyword}":')
            for p in processes:
                print(p)
        else:
            print(f'No processes were found on {ip_address} matching the keyword "{keyword}".')

    # Saving search results
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text files', '*.txt')])
    if not file_path:
        print('Output file path not specified.')
    else:
        with open(file_path, 'w') as t:
            t.write("These are the results for search on {}.\n\n".format(ip_address))
            t.write(f)
            t.write('\n')
            t.write(p)
    print(f'The results have been saved to {file_path}.')
        
    # Close the SSH connection
    ssh.close()

while True:
    input("Press Enter to exit...")
    break