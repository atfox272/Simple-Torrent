import os
import shutil


def file_split(file_path: str, chunk_size: int):
    def split_file_to_chunks(file_path: str, chunk_size: int):
        try:
            with open(file_path, "rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break  # Đã đọc hết tệp
                    yield chunk
        except FileNotFoundError:
            print(f"Can not find: {file_path}")

    # def save_chunks_to_directory(chunks: list, output_directory: str, file_name: str, file_exten: str):
    #     try:
    #         os.makedirs(output_directory, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại
    #         for i, chunk in enumerate(chunks):
    #             output_file = os.path.join(output_directory, f"{file_name}_{file_exten}_{i}.bin")
    #             with open(output_file, "wb") as out_f:
    #                 out_f.write(chunk)
    #             print(f"Chunk created {i}: {output_file}")
    #     except Exception as e:
    #         print(f"Chunks saving error {e}")

    # # Get the file name without extension
    # file_name, file_exten = os.path.splitext(os.path.basename(file_path)) #Take input file's name and extension
    # file_name = file_name.replace('.', '_')  # Replace '.' in file name with '_'
    # file_exten = file_exten.replace('.', '')  # Remove '.' from file extension

    chunks = list(split_file_to_chunks(file_path, chunk_size))
    # save_chunks_to_directory(chunks, f"{file_name}_{file_exten}", file_name, file_exten)
    pieces_folder = 'pieces_folder'

    # if not os.path.exists(pieces_folder):
    #     os.makedirs(pieces_folder)

    base_name = os.path.basename(file_path)

    file_name, file_exten = os.path.splitext(base_name)

    file_exten = file_exten.replace('.', '')

    new_folder_name = f"{file_name}_{file_exten}"

    new_folder_path = os.path.join(pieces_folder, new_folder_name)
    # Check if the new folder exists, if not, create it
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    print('hehehehh', os.path.exists(new_folder_path))

    # Move the chunk files to the new folder
    # for i in range(len(chunks)):
    #     chunk_file = f"{file_name}_{file_exten}_{i}.bin"
    #     os.rename(chunk_file, new_folder_path)

    for i, chunk in enumerate(chunks):
        chunk_file_path = os.path.join(new_folder_path, f"{file_name}_{file_exten}_{i}.bin")
        with open(chunk_file_path, 'wb') as chunk_file:
            chunk_file.write(chunk)

    return len(chunks)  # Return the number of chunks


def reassemble_file(chunk_path, output_path):
    # Get the list of all chunk files
    chunk_files = [os.path.join(chunk_path, f) for f in os.listdir(chunk_path) if
                   os.path.isfile(os.path.join(chunk_path, f))]

    # Sort files, maybe not necessary
    chunk_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

    # Get file path
    folder_name = os.path.basename(chunk_path)
    file_path = folder_name[:folder_name.rfind('_')] + '.' + folder_name[folder_name.rfind('_') + 1:]

    # Create a file path in the output directory with the original file name and extension
    output_file_path = os.path.join(output_path, file_path)

    # Remove first '/' character
    output_file_path = output_file_path[1:]

    # Create a new file
    open(output_file_path, 'a')

    with open(output_file_path, 'wb') as output_file:
        for chunk_file in chunk_files:
            with open(chunk_file, 'rb') as cf:
                output_file.write(cf.read())
    # print(f"The original file has been reassembled and saved as {output_file_path}")


# reassemble_file("/path/to/chunk/files", "/path/to/output/file")

# Ví dụ sử dụng
# if __name__ == "__main__":
#     input_file = "input123.txt"  # Full path to the file, plz use '\\' instead of '\' :( this language is shite
#     chunk_size = 50 * 1024  # Kích thước chunk mong muốn (tùy chỉnh)
#
#     # pieces_folder = 'pieces_folder'
#
#     # if not os.path.exists(pieces_folder):
#     #     os.makedirs(pieces_folder)
#
#     # dest_path = os.path.join(pieces_folder, os.path.basename(input_file))
#
#     # shutil.copyfile(input_file, dest_path)
#
#     # base_name = os.path.basename(input_file)
#     # file_name, file_exten = os.path.splitext(base_name)
#     # file_exten = file_exten.replace('.','')
#
#     # # Create a new folder
#     # new_folder_name = f"{file_name}_{file_exten.lstrip('.')}"
#     # new_folder_path = os.path.join(pieces_folder, new_folder_name)
#
#     # # Check existing
#     # if not os.path.exists(new_folder_path):
#     #     os.makedirs(new_folder_path)
#
#     # # Split file into chunks
#     # chunk_size = 50 * 1024 # Just for example
#     num_chunks = file_split(input_file, chunk_size)
#
#     # for i in range(num_chunks):
#     #     chunk_file = f"{file_name}_{file_exten}_{i}.bin"
#     #     #shutil.move(os.path.join(os.getcwd(), chunk_file),new_folder_path)
#     #     os.rename(chunk_file,new_folder_path)
# # print(f"Number of chunks created: {num_chunks}")
#
# # reassemble_file("input136_txt", "C:\\Users\\84869\\OneDrive\\Desktop\\Work\\1. MMT\\Assignment")