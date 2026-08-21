import base64

# 1. Convert images to Base64 and chunk them
def get_dax_chunks(filepath, var_name):
    with open(filepath, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode('utf-8')
    chunk_size = 30000
    chunks = [b64[i:i+chunk_size] for i in range(0, len(b64), chunk_size)]
    dax_str = f'VAR {var_name} =\n'
    dax_str += ' & \n'.join([f'    "{chunk}"' for chunk in chunks])
    return dax_str

print("Encoding images...")
petra_dax = get_dax_chunks('C:/Users/a.alves/Downloads/ICE_ULTRA/Mockup/PETRA ULTRA.png', 'PetraBase64')
ice_dax = get_dax_chunks('C:/Users/a.alves/Downloads/ICE_ULTRA/Mockup/BEB MIST CRY ICE LIM LIMAO LN 275ML B.png', 'IceBase64')

# 2. Open TMDL file
tmdl_path = 'C:/Users/a.alves/Downloads/ICE_ULTRA/ICE_ULTRA.SemanticModel/definition/tables/Medidas_Ranking.tmdl'
with open(tmdl_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 3. Locate the measure definition
target_index = -1
for idx, line in enumerate(lines):
    if 'measure Ranking_Sellers_HTML =' in line:
        target_index = idx
        break

if target_index == -1:
    print("Error: Could not find Ranking_Sellers_HTML measure!")
    exit(1)

# Format the base64 chunks with three tabs indentation for TMDL
formatted_b64 = ""
for line in (petra_dax + "\n\n" + ice_dax).splitlines():
    formatted_b64 += "\t\t\t" + line + "\n"

# Insert the base64 variables right after the measure name line
lines.insert(target_index + 1, formatted_b64 + "\n")

# Reassemble the file content
new_content = "".join(lines)

# Replace the file:/// references with base64 data URIs (just in case they weren't replaced)
old_images = 'VAR IceImg = "file:///C:/Users/a.alves/Downloads/ICE_ULTRA/Mockup/BEB MIST CRY ICE CAJU ICE LN 275ML - SUADA A.png"\n\t\t\tVAR PetraImg = "file:///C:/Users/a.alves/Downloads/ICE_ULTRA/Mockup/PETRA ULTRA.png"'
new_images = 'VAR IceImg = "data:image/png;base64," & IceBase64\n\t\t\tVAR PetraImg = "data:image/png;base64," & PetraBase64'

new_content = new_content.replace(old_images, new_images)

# Write back to file
with open(tmdl_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Patch applied successfully!")
