# filefinder
filefinder-github
The scripts VM_Search.py and LAN_Search.py can be interchangeably used to perform search operations on both Cloud VMs and LANs. Only the name of variables and strings or only the strings need to be changed accordingly. These 2 scripts use public SSH key to make a secure connection to the remote system.
The PVKey_Search script performs all the same operations for both VMs and LANs except it uses private key for making the connection.
The scripts first make a secure connection to the remote system using SSH, then search for files and processes based on the input given by the user, then displays all the results categorically and prompts the user to select the path for saving the results in a text file.
User can be prompted to input from more no. of choices for searching files by adding strings and append commands for extensions. for eg. pkl, h5, cfg, nc, etc.
