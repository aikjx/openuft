"""Runner: remove stdout redirect and execute charge_quant_attack.py"""
import sys, os

# Read the script
with open('charge_quant_attack.py', encoding='utf-8') as f:
    code = f.read()

# Remove the stdout redirect
code = code.replace(
    "sys.stdout = open('charge_quant_attack.txt', 'w', encoding='utf-8')\n",
    ''
)

# Write clean version
with open('cq_clean.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Written cq_clean.py, now executing...")
