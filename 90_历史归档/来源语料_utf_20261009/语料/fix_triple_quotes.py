"""Fix unclosed triple quotes in the analysis script."""
import sys

filepath = '顶尖论文α推导_全维分析.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Count open and close triple-quotes
lines = content.split('\n')
opens = []
closes = []
in_triple = False
triple_start = -1

for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith("print('''") and not in_triple:
        opens.append(i)
        in_triple = True
        triple_start = i
    elif stripped == "''')" and in_triple:
        closes.append(i)
        in_triple = False

print(f"Open triple quotes at lines: {[x+1 for x in opens]}")
print(f"Close triple quotes at lines: {[x+1 for x in closes]}")

# Find unclosed opens
# They should alternate: open, close, open, close...
# If there are more opens than closes, some are unclosed
if len(opens) > len(closes):
    print(f"\nUnclosed triple quotes: {len(opens) - len(closes)}")
    # The issue is likely that the print(''' at line 232 (index 231) 
    # was not properly closed after our replacement
    # Let's find the specific one
    
    # Find the gap
    for j in range(min(len(opens), len(closes))):
        if opens[j] > closes[j]:
            print(f"  Open at {opens[j]+1} is not properly closed before next open")
    
    # For the last unclosed one, we need to add closing
    # The last open is not closed
    # Find where it should be closed
    
    # Strategy: find the print(''' that starts Part 4 (around line 232)
    # and close it before the Part 5 section starts
    for open_line in opens:
        if open_line > 200 and open_line < 280:  # Part 4 section
            # Find the next line that has a print statement or comment
            # that should come after the triple-quote block
            # The triple quote should close before "# 精确计算"
            for k in range(open_line + 1, len(lines)):
                if lines[k].strip().startswith('# 精确计算'):
                    # Insert closing '''') before this line
                    indent = '    '  # match the indentation
                    new_line = indent + "''')"
                    lines.insert(k, new_line)
                    print(f"  Inserted closing at line {k+1} (0-indexed: {k})")
                    break
            break

with open(filepath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("\nFixed! Saved updated file.")