import re

with open('piloto-a/src/stores/analytics.ts', 'r') as f:
    content = f.read()

# Replace the whole EVENT_SCHEMAS block with a commented version
block_start_index = content.find('const EVENT_SCHEMAS')
if block_start_index != -1:
    block_end_index = content.find('}', block_start_index)
    if block_end_index != -1:
        block = content[block_start_index:block_end_index+1]
        commented_block = '\n'.join(['// ' + line for line in block.split('\n')])
        content = content[:block_start_index] + commented_block + content[block_end_index+1:]

with open('piloto-a/src/stores/analytics.ts', 'w') as f:
    f.write(content)
