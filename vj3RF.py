import re
import datetime
import os
import pandas as pd
import hashlib
import magic
import mimetypes


log_path = "C:/Users/A507/mskocic/setupapi.dev2.log"
regex = r"^>>>  \[Device Install.*#(Disk&Ven_[A-Za-z0-9]+)&(Prod_([\w\s\S]+?))&(Rev_([\w\s\S]+?))#([\w\s\S]+?)#.*\]"
usb_devices_list = []


# Read the contents of the setupapi.dev.log file
with open(log_path, "r") as log_file:
    # Store information about each USB device in a dictionary
    for line in log_file:
        match = re.match(regex, line)
        if match:
            vendor_id = match.group(1)
            product_id = match.group(2)
            serial_number = match.group(6)
            instance_id = product_id + serial_number
            line = next(log_file)
            event_line = line.split("t")
            event_time = event_line[3]
            usb_devices = {
                "device_vendor_id": vendor_id,
                "device_product_id": product_id,
                "device_instance_id": instance_id,
                "serial_number": serial_number,
                "event_time": event_time,
            }
            usb_devices_list.append(usb_devices)
for device in usb_devices_list:
    print(device)


# specify the directory path where the files are located
dir_path = "E:\\"

# create an empty list to store the file names
file_names = []
file_extension = []
md5s = []
sha1s = []
sha256s = []
magic_numbers = []
extension_matches = []


hash_print = "c15e32d27635f248c1c8b66bb012850e5b342119"

obj = magic.Magic(mime=True)


# iterate through all files in the directory
for file in os.listdir(dir_path):
    # check if the file is a regular file (i.e., not a directory)
    if os.path.isfile(os.path.join(dir_path, file)):
        # if so, add the file name to the list
        file_names.append(file)
        name, extension = os.path.splitext(file)
        file_extension.append(extension)

        md5s = hashlib.md5(file.encode()).hexdigest()
        sha1s = hashlib.sha1(file.encode()).hexdigest()
        sha256s = hashlib.sha256(file.encode()).hexdigest()

        magic_number = obj.from_file(os.path.join(dir_path, file))
        magic_numbers.append(magic_number)

        # check if the magic number contains the file extension
        if extension.lower() == "":
            extension_matches.append(False)
        elif (
            mimetypes.guess_type("test" + extension.lower())[0] in magic_number.lower()
        ):
            extension_matches.append(True)
        else:
            extension_matches.append(False)


# create a Pandas dataframe with the file names
df = pd.DataFrame(
    {
        "file_name": file_names,
        "extension": file_extension,
        "MD5": md5s,
        "SHA1": sha1s,
        "SHA256": sha256s,
        "magic numbers": magic_numbers,
        "extension matches": extension_matches,
    }
)


# print the dataframe
print(df)