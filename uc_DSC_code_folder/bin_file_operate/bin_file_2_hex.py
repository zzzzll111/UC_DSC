import os

# Function to convert files in folders to hexadecimal and write to file
def folders_to_hex(folders, output_file_path):
    try:
        # Open output file in write mode
        with open(output_file_path, 'w') as output_file:
            # Process each folder
            for folder_path in folders:
                # Ensure the folder exists
                if not os.path.exists(folder_path):
                    print(f"文件夹不存在: {folder_path}")
                    continue

                # List files in the folder
                files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

                # Process each file
                for file in files:
                    file_path = os.path.join(folder_path, file)
                    file_to_hex(file_path, output_file)

        print(f"转换完成。十六进制数据已保存到文件: {output_file_path}")

    except Exception as e:
        print(f"转换过程中发生错误: {str(e)}")


# Function to convert file to hexadecimal and write to file
def file_to_hex(file_path, output_file):
    try:
        # Open the input file in binary mode
        with open(file_path, 'rb') as f:
            # Read the entire file contents
            file_content = f.read()
            # Convert bytes to hexadecimal string with '0x' prefix
            hex_content = '0x' + file_content.hex()

            # Write filename and hexadecimal content to output file
            output_file.write(f"{os.path.basename(file_path)}\n")
            output_file.write(f"{hex_content}\n\n")  # Ensure blank line between files
    except Exception as e:
        print(f"处理文件 {file_path} 时发生错误: {str(e)}")



