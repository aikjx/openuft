import os
import re

# Define the base directory
base_dir = r"d:\a10\aikjx\code\my_lib\utf\10-统一场论核心公式\可视化"

# List of directories to process
dirs_to_process = [
    "01-时空同一化方程",
    "02三维螺旋时空方程",
    "04引力场定义方程",
    "05静止动量方程",
    "06运动动量方程",
    "07宇宙大统一方程",
    "08三维空间波动方程",
    "09引力场与旋转速度关系",
    "10电场定义方程",
    "11磁场定义方程",
    "12电磁场能量方程",
    "13能量方程",
    "14动量能量方程",
    "15时空波动方程",
    "16时间的本质方程",
    "17电荷定义方程"
]

# Function to update a single Python file
def update_file(file_path):
    print(f"Processing: {file_path}")
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if the file has savefig calls
    if 'savefig' not in content:
        print(f"  No savefig calls found, skipping")
        return
    
    # Step 1: Add os import if not present
    if 'import os' not in content:
        # Find the import section and add os import
        import_lines = re.findall(r'^import.*$|^from.*$', content, re.MULTILINE)
        if import_lines:
            first_import = content.find(import_lines[0])
            content = content[:first_import] + 'import os\n' + content[first_import:]
        else:
            # If no imports, add at the beginning
            content = 'import os\n' + content
    
    # Step 2: Add directory creation code before savefig calls
    # Find all savefig lines
    savefig_lines = re.findall(r'\.savefig\(.*\)', content)
    if not savefig_lines:
        print(f"  No savefig calls found after checking, skipping")
        return
    
    # Add directory creation before the first savefig call
    first_savefig_pos = content.find(savefig_lines[0])
    # Find the beginning of the function containing the savefig call
    # Look for the nearest function definition above
    lines = content[:first_savefig_pos].split('\n')
    for i in range(len(lines)-1, -1, -1):
        if lines[i].strip().startswith('def '):
            # Insert after the function definition
            insert_pos = content.find(lines[i]) + len(lines[i]) + 1
            break
    else:
        # If no function found, insert at the beginning of the file
        insert_pos = 0
    
    # Create the directory creation code
    dir_code = '''    # Ensure img directory exists
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    '''
    
    # Insert the directory creation code
    content = content[:insert_pos] + dir_code + content[insert_pos:]
    
    # Step 3: Update savefig paths to use relative paths
    # First, find all savefig calls
    savefig_matches = re.finditer(r'(\.savefig\()([^,]+)(,.*?\))', content)
    for match in savefig_matches:
        full_call = match.group(0)
        filename_part = match.group(2)
        # Remove quotes and whitespace
        filename = filename_part.strip().strip('"').strip("'")
        # Get just the filename without path
        basename = os.path.basename(filename)
        # Create new filename part with relative path
        new_filename_part = f"'./img/{basename}'"
        # Replace in the content
        content = content.replace(filename_part, new_filename_part)
    
    # Step 4: Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Updated successfully")

# Process each directory
for dir_name in dirs_to_process:
    dir_path = os.path.join(base_dir, dir_name)
    print(f"\n=== Processing directory: {dir_name} ===")
    
    # Find all Python files in the directory
    python_files = [f for f in os.listdir(dir_path) if f.endswith('.py')]
    
    if not python_files:
        print(f"  No Python files found in {dir_name}")
        continue
    
    for py_file in python_files:
        file_path = os.path.join(dir_path, py_file)
        update_file(file_path)

print("\n=== All files processed ===")
