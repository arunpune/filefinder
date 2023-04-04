# importing modules
import os
import time


print("***************************")
print("Welcome to FileFinder Tool!")
print("***************************")


# creating variables to store inputs
extensions = input("Enter the file extensions to search for (comma-separated) (For example: .xlsx, .xls): ").split(",")
directory = input("Enter the directory or network to search (For example: C:/Users/Username): ")


print("Searching for files with extensions {} in directory/network {}...".format(extensions, directory))
print()


# creating a list of results
results = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(tuple(extensions)):
            file_path = os.path.join(root, file)
            created_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(file_path)))
            modified_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(file_path)))
            file_size = os.path.getsize(file_path)
            results.append((file_path, created_time, modified_time, file_size))
            

print("***************results***************")

# counting number of results
filecount = len(results)


# displaying the results
print("total no. of files with extensions {} is {}".format(extensions, filecount))
for result in results:
    print("File: {}, Created Time: {}, Modified Time: {}, File Size: {} bytes".format(result[0], result[1], result[2], result[3]))


while True:
    input("Press Enter to exit...")
    break
