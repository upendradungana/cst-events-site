import json
from datetime import date
from pathlib import Path

def load_events(path):
    # Reads the JSON file and parses the event data
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data["events"]

def upcoming(events, today):
    # Filters out past events and sorts the remaining ones by date
    future = [e for e in events if e["date"] > today]
    return sorted(future, key=lambda e: e["date"])

def render(events):
    # Generates HTML list items dynamically
    items = "\n".join(
        f'    <li><strong>{e["date"]}</strong> - {e["title"]} '
        f'<em>({e["venue"]})</em></li>'
        for e in events
    )
    return (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '  <meta charset="utf-8">\n'
        '  <title>ACM Club at CST - Events</title>\n'
        '</head>\n'
        '<body>\n'
        '  <h1>Upcoming events</h1>\n'
        '  <ul>\n'
        f'{items}\n'
        '  </ul>\n'
        '</body>\n'
        '</html>\n'
    )

def main():
    # Set the input path for event data
    json_path = "events.json"
    
    # Check if the events file exists to prevent a crash
    if not Path(json_path).exists():
        print(f"Error: {json_path} not found. Please create it first.")
        return

    events = upcoming(load_events(json_path), date.today().isoformat())
    
    # Create the output directory and write the generated HTML file safely
    Path("dist").mkdir(exist_ok=True)
    Path("dist/index.html").write_text(render(events), encoding="utf-8")
    print(f"Success: Wrote dist/index.html with {len(events)} upcoming events.")

if __name__ == "__main__":
    main()
