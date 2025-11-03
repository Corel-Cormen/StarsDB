import subprocess

command = [
    "python",
    "MySqlImport/import_xml_to_db.py",
    r"C:\Users\User\PycharmProjects\StarsDB\3rdparty\scrapper\ScrapData_100_thousand"
]

repeat_count = 10

for i in range(repeat_count):
    print(f"Starting the import {i + 1}/{repeat_count}...")

    result = subprocess.run(command)

    if result.returncode == 0:
        print(f"Import {i + 1} successfully completed.\n")
    else:
        print(f"Error while importing {i + 1}. Exit code: {result.returncode}\n")
        break

print("All imports completed.")
