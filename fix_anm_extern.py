externs = """
extern VertexTex1Xyzrwh g_PrimitivesToDrawVertexBuf[4];
extern VertexTex1DiffuseXyzrwh g_PrimitivesToDrawNoVertexBuf[4];
extern VertexTex1DiffuseXyz g_PrimitivesToDrawUnknown[4];
extern AnmManager *g_AnmManager;
"""

for fname in ['src/AnmVm.cpp', 'src/AnmDisp.cpp']:
    with open(fname, 'r') as f:
        lines = f.readlines()
    for i, l in enumerate(lines):
        if l.startswith('namespace th06'):
            lines.insert(i+2, externs)
            break
    with open(fname, 'w') as f:
        f.writelines(lines)
