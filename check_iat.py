import sys
sys.path.append('scripts')
import pefile

def get_iat_order(filepath):
    pe = pefile.PE(filepath)
    pe.parse_data_directories()
    imports = []
    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            imports.append(entry.dll.decode('utf-8'))
    return imports

print("Original:")
print(get_iat_order('resources/th06.exe'))
print("\nRebuilt:")
print(get_iat_order('build/th06.exe'))
