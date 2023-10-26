# Boring generic file filter
I'm tired of messy file and folder names, inconsistent file extensions, etc.

# Paths
- src -> absolute path of your top level folder (recursive file search happens here)
- dst -> currently not used, plugin to process, rename files to your desired directory

# Filters
There are currently 3 filter classes implemented.

- FileName
- FolderNames
- Extension

The classes can handle multplie arguments.
The classes can be connected arbitrarily with the binary operators (&, |, ~)

Not tested on Windows and Mac
