import json

def remove_duplicate_stimuli(json_data):
    unique_stimuli = []
    seen_combinations = set()

    for stimulus in json_data:
        key = (stimulus["conj1"], stimulus["conj2"], stimulus["predicate"])
        if key not in seen_combinations:
            seen_combinations.add(key)
            unique_stimuli.append(stimulus)

    return unique_stimuli

def replace_copula_with_placeholder(json_data):
    for stimulus in json_data:
        copula = " "+stimulus["copula"]+" "
        stimulus["sentence"] = stimulus["sentence"].replace(copula, " %% ")
        stimulus["text"] = stimulus["sentence"]

def main():
    # Update the file path to point to your actual JSON file
    json_file_path = "stimuli.json"

    try:
        with open(json_file_path, "r") as file:
            all_stimuli = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
        return
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {json_file_path}")
        return

    unique_stimuli = remove_duplicate_stimuli(all_stimuli)
    replace_copula_with_placeholder(unique_stimuli)

    # Writing the updated unique stimuli to a new file named "unique_stimuli.json"
    with open("unique_stimuli.json", "w") as file:
        json.dump(unique_stimuli, file, indent=2)

if __name__ == "__main__":
    main()
