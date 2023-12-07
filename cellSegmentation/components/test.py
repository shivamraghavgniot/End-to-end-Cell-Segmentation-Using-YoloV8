import shutil,os 
# shutil.rmtree("data.yaml", ignore_errors=True)
# os.remove("data.yaml")
# Create the target directory if it doesn't exist
source_directory = "cellSegmentation"
target_directory = "test"
# os.makedirs(target_directory, exist_ok=True)

if not os.path.exists(target_directory):
    # Copy the entire directory
    shutil.copytree(source_directory, target_directory)
else:
    shutil.rmtree(target_directory)
    shutil.copytree(source_directory, target_directory)
    # Handle the case when the target directory already exists
    # print(f"The target directory '{target_directory}' already exists.")