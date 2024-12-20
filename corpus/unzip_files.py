import os
import gzip
import bz2
from pathlib import Path


def unzip_files(corpus_dir: str) -> None:
    """
    Unzip all .gz and .bz2 files from the zipped directory to the unzipped directory.
    
    Args:
        corpus_dir (str): Path to the corpus directory
    """
    # Setup directories
    zipped_dir = os.path.join(corpus_dir, 'zipped')
    unzipped_dir = os.path.join(corpus_dir, 'unzipped')
    os.makedirs(unzipped_dir, exist_ok=True)
    
    # Process each .gz and .bz2 file in the zipped directory
    for file in os.listdir(zipped_dir):
        if not file.endswith(('.gz', '.bz2')):
            continue

        print(f"Working on {file}...")
            
        compressed_path = os.path.join(zipped_dir, file)
        # Remove .gz or .bz2 extension
        output_filename = file[:-3] if file.endswith('.gz') else file[:-4]
        output_path = os.path.join(unzipped_dir, output_filename)
        
        # Skip if already unzipped
        if os.path.exists(output_path):
            print(f"Skipping {file} (already unzipped)")
            continue
            
        # Unzip the file based on its extension
        try:
            if file.endswith('.gz'):
                with gzip.open(compressed_path, 'rb') as f_in:
                    with open(output_path, 'wb') as f_out:
                        f_out.write(f_in.read())
            else:  # .bz2 file
                with bz2.open(compressed_path, 'rb') as f_in:
                    with open(output_path, 'wb') as f_out:
                        f_out.write(f_in.read())
            print(f"Successfully unzipped {file}")
        except Exception as e:
            print(f"Error processing {file}: {str(e)}")


if __name__ == "__main__":
    # Get the absolute path to the corpus directory
    corpus_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Starting corpus processing...")
    print(f"Corpus directory: {corpus_dir}")
    
    # Unzip all files from zipped to unzipped directory
    print("\nUnzipping files...")
    unzip_files(corpus_dir)
    print("\nDone!")