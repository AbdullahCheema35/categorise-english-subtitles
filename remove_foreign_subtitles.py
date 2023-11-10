import os
import argparse
from langdetect import detect

def is_english(text):
    try:
        # Try to detect the language of the text
        language = detect(text)
        # Return True if the detected language is English
        return language == 'en'
    except:
        # If an error occurs during language detection, assume it's not English
        return False

def check_files_in_folder(directory_path, foreign_folder_name):
    # Create a new folder for foreign subtitles
    foreign_folder_path = os.path.join(directory_path, foreign_folder_name)

    total_files = 0
    english_files = 0
    foreign_files = 0

    # Loop through each file in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if os.path.isdir(file_path) and filename != foreign_folder_name:
            ret_total_files, ret_english_files, ret_foreign_files = check_files_in_folder(file_path, foreign_folder_name)
            total_files, english_files, foreign_files = ret_total_files+total_files, ret_english_files+english_files, ret_foreign_files+foreign_files
        # Check if it's a file and not a directory
        elif os.path.isfile(file_path) and (filename.endswith('.vtt') or filename.endswith('.srt')):
            total_files += 1
            
            try:
                # Read the content of the file
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                is_file_ok = True   # Read the contents of the file, without error
            except:
                # Error during reading contents of the file; this aint correct english subtitles file
                is_file_ok = False

            # Check if the content contains English letters
            if is_file_ok and is_english(content) and (content.find('thumbnails.jpg#xywh=')==-1):   # Couldn't find the specified substring in the content string
                english_files += 1
                # print(f'English subtitles found in: {filename}')
            else:
                foreign_files += 1
                # Create a new folder for foreign files
                os.makedirs(foreign_folder_path, exist_ok=True)
                # If not, move the file to the 'foreign_subtitles' folder
                foreign_file_path = os.path.join(foreign_folder_path, filename)
                os.rename(file_path, foreign_file_path)
                # print(f'Removed non-English subtitles file: {filename}')
    return total_files, english_files, foreign_files


def main():
    parser = argparse.ArgumentParser(description='Process subtitle files and separate English and non-English files.')
    parser.add_argument('directory_path', nargs='?', default='.', help='Path to the directory containing subtitle files (default: current directory)')

    args = parser.parse_args()
    directory_path = args.directory_path

    print(f'Processing files in directory: {directory_path}',end='\n\n')

    foreign_folder_name = 'foreign_subtitles'

    total_files, english_files, foreign_files = check_files_in_folder(directory_path, foreign_folder_name)    

    print(f'Total files: {total_files}')
    print(f'English files: {english_files}')
    print(f'Foreign files: {foreign_files}')

if __name__ == "__main__":
    main()
