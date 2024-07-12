import re

def read_ass_file(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    return lines

def write_ass_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8-sig') as f:
        f.writelines(lines)

def process_events(events):
    processed_events = []
    for i, event in enumerate(events):
        current_line = events[i]
        
        if i > 0:
            previous_line = events[i - 1]
        else:
            previous_line = 'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,...\n'

        if i < len(events) - 1:
            next_line = events[i + 1]
        else:
            next_line = 'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,...\n'

        # Extract the text part of each event
        current_text = re.search(r'(?<=,)[^,]*$', current_line).group().strip()
        previous_text = re.search(r'(?<=,)[^,]*$', previous_line).group().strip()
        next_text = re.search(r'(?<=,)[^,]*$', next_line).group().strip()

        # Construct the new line with previous and next texts
        new_text = f"{previous_text} {current_text} {next_text}"
        new_line = re.sub(r'(?<=,)[^,]*$', new_text, current_line)

        processed_events.append(new_line)
    
    return processed_events

def transform_ass(input_path, output_path):
    lines = read_ass_file(input_path)
    
    # Separate the lines into sections
    header_lines = []
    event_lines = []
    events_section = False

    for line in lines:
        if "[Events]" in line:
            events_section = True
        if events_section and line.startswith("Dialogue:"):
            event_lines.append(line)
        else:
            header_lines.append(line)

    processed_events = process_events(event_lines)
    output_lines = header_lines + processed_events
    
    write_ass_file(output_path, output_lines)


input_path = 'input.ass'
output_path = 'output.ass'
transform_ass(input_path, output_path)