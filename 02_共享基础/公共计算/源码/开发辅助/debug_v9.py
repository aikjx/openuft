import glob, sys, traceback, io, contextlib, os

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Find the file using glob (Grep found it, so glob should too)
uft_dir = r'd:\a10\aikjx\code\my_lib\uft'
pattern = os.path.join(uft_dir, '*v9*质量谱*.py')
files = glob.glob(pattern)

output_lines = []
output_lines.append(f'Glob pattern: {pattern}')
output_lines.append(f'Files found: {files}')

# Try using a broader approach
all_py_in_uft = glob.glob(os.path.join(uft_dir, '*.py'))
output_lines.append(f'All .py in utf: {all_py_in_uft}')

# Maybe the file is in a subdir? Let's walk with limited depth
def walk_limited(top, max_depth=2):
    results = []
    top = os.path.abspath(top)
    for root, dirs, fnames in os.walk(top):
        depth = root[len(top):].count(os.sep)
        if depth < max_depth:
            for fn in fnames:
                if fn.endswith('.py') and 'v9' in fn:
                    results.append(os.path.join(root, fn))
    return results

walk_files = walk_limited(uft_dir, max_depth=3)
output_lines.append(f'Walk found: {walk_files}')

# Write debug output
with open(r'd:\a10\aikjx\code\my_lib\debug_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))
print('Debug output written')
