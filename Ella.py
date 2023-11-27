import re

def process_xml_as_text(file_path):
    try:
        # Try opening the file with a different encoding if the default one doesn't work
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Use regular expressions to find all occurrences of TimePlayed and Deaths
        time_played_values = re.findall(r'TimePlayed="(\d+)"', content)
        deaths_values = re.findall(r'Deaths="(\d+)"', content)

        # Convert the found values to integers and sum them up
        total_time_played = sum(map(int, time_played_values))
        total_deaths = sum(map(int, deaths_values))

    except UnicodeDecodeError:
        try:
            # If utf-8 doesn't work, try a different encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                content = file.read()
                time_played_values = re.findall(r'TimePlayed="(\d+)"', content)
                deaths_values = re.findall(r'Deaths="(\d+)"', content)
                total_time_played = sum(map(int, time_played_values))
                total_deaths = sum(map(int, deaths_values))

        except Exception as e:
            print(f"Error processing file with latin-1 encoding: {e}")
            total_time_played, total_deaths = 0, 0

    except Exception as e:
        print(f"Error processing file: {e}")
        total_time_played, total_deaths = 0, 0

    return total_time_played, total_deaths

# Example usage:
time_played, deaths = process_xml_as_text('0.celeste')
print(f"Total Time Played: {time_played}, Total Deaths: {deaths}")