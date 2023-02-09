import os

os.rename("new_client.py", "client.py")
os.system("python client.py")
print("Updated")

exit()