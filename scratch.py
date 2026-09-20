import sys
sys.path.append('scripts')
import pefile

def get_data_section(pe):
    for sec in pe.sections:
        if sec.Name.strip(b'\x00') == b'.data':
            return sec
    return None

def dump_initialized_globals(filename):
    pe = pefile.PE(filename)
    start_rva = 0x76000
    pointers = []
    for i in range(100):
        ptr = pe.get_dword_at_rva(start_rva + i * 4)
        if ptr != 0:
            pointers.append(ptr)
        if i > 0 and ptr == 0 and pe.get_dword_at_rva(start_rva + (i-1) * 4) == 0:
            break
            
    # Now for each pointer, disassemble to find the global variable it initializes
    # We look for "mov ecx, <addr>" which is B9 <addr>
    
    globals_init = []
    for ptr in pointers:
        # read some bytes at the pointer
        rva = ptr - pe.OPTIONAL_HEADER.ImageBase
        data = pe.get_data(rva, 0x20)
        # find B9 ?? ?? ?? ??
        # B9 is mov ecx, imm32
        for i in range(len(data)-4):
            if data[i] == 0xB9:
                imm = data[i+1] | (data[i+2]<<8) | (data[i+3]<<16) | (data[i+4]<<24)
                globals_init.append(imm)
                break
    return globals_init

orig = dump_initialized_globals('resources/東方紅魔郷.exe')
built = dump_initialized_globals('build/th06.exe')

print("Original count:", len(orig))
print("Built count:", len(built))

# compare
orig_set = set(orig)
built_set = set(built)

print("In original but not in built:")
for g in orig:
    if g not in built_set:
        print(hex(g))

print("In built but not in original:")
for g in built:
    if g not in orig_set:
        print(hex(g))
