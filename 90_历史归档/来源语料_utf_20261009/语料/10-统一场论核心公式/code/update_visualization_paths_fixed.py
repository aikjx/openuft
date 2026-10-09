import os
import re

# Define the base directory - 使用正确的目录结构
base_dir = r"d:\a10\aikjx\code\my_lib\utf\10-统一场论核心公式\公式验证论文"

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
    
    # Step 1: Fix any matplotlib import syntax errors
    content = content.replace('matplotlib\\.pyplot', 'matplotlib.pyplot')
    
    # Step 2: Add os import at the beginning if not present
    if 'import os' not in content:
        # Add os import after other imports
        lines = content.split('\n')
        # Find the last import line
        last_import = -1
        for i, line in enumerate(lines):
            if line.strip().startswith(('import', 'from')) and '#' not in line.split()[0]:
                last_import = i
        
        if last_import >= 0:
            # Insert after last import
            lines.insert(last_import + 1, 'import os')
        else:
            # No imports found, add at beginning
            lines.insert(0, 'import os')
        
        content = '\n'.join(lines)
    
    # Step 3: Find where to insert directory creation code
    # Look for the main block or the function containing savefig
    lines = content.split('\n')
    insert_pos = None
    
    # Look for if __name__ == "__main__": block
    for i, line in enumerate(lines):
        if line.strip().startswith('if __name__ == "__main__":'):
            insert_pos = i + 1
            break
    
    # If no main block found, look for any function containing savefig
    if insert_pos is None:
        savefig_line = None
        for i, line in enumerate(lines):
            if '.savefig(' in line:
                savefig_line = i
                break
        
        if savefig_line is not None:
            # Find the function containing this line
            for i in range(savefig_line - 1, -1, -1):
                if lines[i].strip().startswith('def '):
                    # Insert at the beginning of this function
                    insert_pos = i + 1
                    break
    
    # If still no insert position found, insert at beginning of file
    if insert_pos is None:
        insert_pos = 1  # After imports
    
    # Step 4: Insert directory creation code if not already present
    dir_code = '''# Ensure img directory exists
img_dir = './img'
if not os.path.exists(img_dir):
    os.makedirs(img_dir)'''
    
    if dir_code not in content:
        lines.insert(insert_pos, dir_code)
        content = '\n'.join(lines)
    
    # Step 5: Update all savefig paths to use relative paths
    # Process each line
    new_lines = []
    for line in lines:
        if '.savefig(' in line:
            # Find the filename part
            match = re.search(r'\.savefig\(([^,]+),', line)
            if match:
                filename_part = match.group(1)
                filename = filename_part.strip().strip('"').strip("'")
                basename = os.path.basename(filename)
                # Replace with relative path
                new_filename = f'\'./img/{basename}\''
                new_line = line.replace(filename_part, new_filename)
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    content = '\n'.join(new_lines)
    
    # Step 6: Write the updated content back to the file
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
