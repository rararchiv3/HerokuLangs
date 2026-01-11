import os
import re

root_dir = '/home/rararch/Документы/hlangs/exteraEmoji'

emoji_pattern = re.compile(r'<emoji document_id=["\']?(\d+)["\']?>(.*?)</emoji>')

def process_line(line):
    val_part = ""
    if ':' in line:
        try:
            val_part = line.split(':', 1)[1].strip()
        except IndexError:
            pass
    
    is_double_quoted = val_part.startswith('"')
    
    def emoji_repl(m):
        doc_id = m.group(1)
        content = m.group(2)
        if is_double_quoted:
            return f"<a href='tg://emoji?id={doc_id}'>{content}</a>"
        else:
            return f'<a href="tg://emoji?id={doc_id}">{content}</a>'

    line = emoji_pattern.sub(emoji_repl, line)
    
    return line

for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.yml'):
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except Exception:
                continue
            
            new_lines = [process_line(line) for line in lines]
            
            if new_lines != lines:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
