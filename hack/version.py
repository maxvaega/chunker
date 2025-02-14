'''
This file is used to get the version of the package pinecone
it was modified from the original version in order to circumvent a bug when pyinstaller could not bundle the __version__ file

Instructions:
1. find and note down the pinecone version:

bash:
    pip show pinecone-client

2. find and note down the path the version.py file in your python environment:

python:
    import pinecone
    import os
    print(os.path.join(os.path.dirname(pinecone.__file__), "utils/version.py"))

3. edit the file as below:
replace the line: Path(file).parent.parent.joinpath("version").read_text().strip()
with the version from step 1

my folder was: /opt/miniconda3/envs/chunker/lib/python3.12/site-packages/pinecone/utils/version.py
    
'''




from pathlib import Path


def get_version():
    # return Path(__file__).parent.parent.joinpath("__version__").read_text().strip()
    return "5.0.1"


__version__ = get_version()
