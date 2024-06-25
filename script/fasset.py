import os
import zipfile
import shutil
import sys

def get_unique_filename(dest_dir, base_filename):
    base, ext = os.path.splitext(base_filename)
    counter = 1
    unique_filename = base_filename
    while os.path.exists(os.path.join(dest_dir, unique_filename)):
        unique_filename = f"{base}_{counter}{ext}"
        counter += 1
    return unique_filename

def organize_images_in_directory(directory):
    output_dir = os.path.join(directory, "output")
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Temporary directory to extract files
    temp_dir = os.path.join(output_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Process each zip file in the directory
    for file in os.listdir(directory):
        if file.endswith(".zip"):
            zip_path = os.path.join(directory, file)
            zip_base_name = os.path.splitext(file)[0]
            
            # Extract the zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Process each file in the temp directory
            for filename in os.listdir(temp_dir):
                src_path = os.path.join(temp_dir, filename)
                
                if "@2x" in filename:
                    dest_dir = os.path.join(output_dir, "2.0x")
                elif "@3x" in filename:
                    dest_dir = os.path.join(output_dir, "3.0x")
                else:
                    dest_dir = output_dir
                
                new_filename = zip_base_name + os.path.splitext(filename)[1]
                os.makedirs(dest_dir, exist_ok=True)
                unique_filename = get_unique_filename(dest_dir, new_filename)
                dest_path = os.path.join(dest_dir, unique_filename)
                
                # Move the file to the appropriate directory
                shutil.move(src_path, dest_path)
    
    # Clean up temporary directory
    shutil.rmtree(temp_dir)

def main():
    if len(sys.argv) != 2:
        print("Usage: python organize_images.py <working_directory>")
        sys.exit(1)
    
    working_directory = sys.argv[1]
    
    if not os.path.isdir(working_directory):
        print(f"The provided directory does not exist: {working_directory}")
        sys.exit(1)
    
    organize_images_in_directory(working_directory)

if __name__ == "__main__":
    main()
