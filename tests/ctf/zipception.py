import os
import zipfile
import tempfile
import shutil
import sys

def extract_nested_zip_iterative(initial_zip_path, extraction_path):
    """
    Iteratively extract a deeply nested zip file without recursion
    """
    current_zip = initial_zip_path
    depth = 0
    
    while True:
        depth += 1
        print(f"Extracting level {depth}: {os.path.basename(current_zip)}")
        
        # Create a temporary directory for this extraction
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Extract the current zip file
            with zipfile.ZipFile(current_zip, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Get the list of extracted files
            extracted_files = os.listdir(temp_dir)
            
            # If no files were extracted, we're done
            if len(extracted_files) == 0:
                print(f"No files found at level {depth}. Extraction complete.")
                break
                
            # Look for the next zip file
            next_zip_found = False
            for file_name in extracted_files:
                file_path = os.path.join(temp_dir, file_name)
                if zipfile.is_zipfile(file_path):
                    # Clean up previous temp dir if not the first iteration
                    if depth > 1:
                        prev_temp_dir = os.path.dirname(current_zip)
                        if prev_temp_dir.startswith(tempfile.gettempdir()):
                            shutil.rmtree(prev_temp_dir)
                    
                    # Update current zip for next iteration
                    current_zip = file_path
                    next_zip_found = True
                    break
            
            # If no zip file was found, we've reached the final content
            if not next_zip_found:
                print(f"No more zip files found at level {depth}. Extraction complete.")
                # Copy final files to output directory
                for item in extracted_files:
                    source = os.path.join(temp_dir, item)
                    dest = os.path.join(extraction_path, item)
                    if os.path.isdir(source):
                        shutil.copytree(source, dest)
                    else:
                        shutil.copy2(source, dest)
                break
                
        except Exception as e:
            print(f"Error at depth {depth}: {str(e)}")
            raise
            
    # Clean up any remaining temp directories
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    return extraction_path

def main():
    # Path to the file with .zip extension
    file_path = r"E:\codes\drone program\tests\flag3000.zip"
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return
    
    # Check if it's a zip file
    if not zipfile.is_zipfile(file_path):
        print(f"Error: The file {file_path} is not a valid zip file.")
        return
    
    # Create a directory for the final output
    output_dir = "final_extracted_content"
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract all nested zip files
    try:
        result_path = extract_nested_zip_iterative(file_path, output_dir)
        print(f"\nExtraction complete! Final content is in: {result_path}")
        
        # List and display the final file(s)
        print("\nExtracted files:")
        files_found = False
        for item in os.listdir(result_path):
            files_found = True
            item_path = os.path.join(result_path, item)
            if os.path.isfile(item_path):
                file_size = os.path.getsize(item_path)
                print(f"Found file: {item} ({file_size} bytes)")
                
                # Try to read as text first
                try:
                    with open(item_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print("\nContent:")
                        print("=" * 40)
                        print(content)
                        print("=" * 40)
                except UnicodeDecodeError:
                    print(f"File appears to be binary. Cannot display content.")
                    # Try to read as binary (first 100 bytes as hex)
                    try:
                        with open(item_path, 'rb') as f:
                            binary_content = f.read(100)
                            hex_content = ' '.join(f'{b:02x}' for b in binary_content)
                            print(f"First 100 bytes (hex): {hex_content}")
                    except Exception as e:
                        print(f"Could not read binary content: {e}")
                except Exception as e:
                    print(f"Error reading file: {e}")
            else:
                print(f"Found directory: {item}")
        
        if not files_found:
            print("No files were found after extraction. The zip files might be empty.")
    
    except Exception as e:
        print(f"Failed to extract nested zip files: {str(e)}")

if __name__ == "__main__":
    main()