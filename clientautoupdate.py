import os

os.rename("new_client.py", "client.py")
print(" Client updated")
os.system("python client.py")

exit()