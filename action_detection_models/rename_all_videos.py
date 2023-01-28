# importing os module
import os

# Function to rename multiple files
def main():
    folder = r"GMS\baggage_handling"
    for count, filename in enumerate(os.listdir(folder)):
        dst = f"baggage_handling_{str(count)}.mp4"
        src = f"{folder}/{filename}"  # foldername/filename, if .py file is outside folder
        dst = f"{folder}/{dst}"
        # rename() function will
        # rename all the files
        os.rename(src, dst)

# Driver Code
if __name__ == '__main__':
    # Calling main() function
    main()