import os
import json

class ModeConfigurator:
    def __init__(self, modes_file, working_directory):
        self.modes_file = modes_file
        self.working_directory = working_directory
        self.modes = self.load_modes_from_file()

    def load_modes_from_file(self, key="interaction_modes"):
        with open(self.modes_file, 'r') as file:
            return json.load(file)[key]

#TODO: is this needed? #logging

    def create_mode_directory(self, mode_data):
        modes_directory = os.path.dirname(self.modes_file)
        mode = mode_data['current_mode']
        mode_directory = os.path.join(modes_directory, mode)
        
        if not os.path.exists(mode_directory):
            os.makedirs(mode_directory)
            print(f"Directory for mode {mode} created.")
        else:
            print(f"Directory for mode {mode} already exists.")
        
        return mode_directory

    def set_mode_data(self, mode):
        mode_data = self.modes.get(mode)
        if not mode_data:
            print(f"Invalid mode: {mode}")
            return

        mode_path = os.path.join(self.working_directory, 'current_mode.json')
        with open(mode_path, 'w') as file:
            json.dump(mode_data, file)
        print(f"Mode {mode} has been set!")

    def configure_mode(self):
        try:
            print("\nMode:\n")
            mode_names = list(self.modes.keys())
            for idx, mode in enumerate(mode_names, start=1):
                description = self.modes[mode]["description"]
                print(f"{idx}: {mode} - {description}")

            total_modes = len(self.modes)
            selection = int(input(f"\nEnter the mode number (1-{total_modes}): "))

            if 1 <= selection <= total_modes:
                mode = mode_names[selection-1]  # adjust index for 0-based list
                mode_data = self.modes[mode]
                mode_directory = self.create_mode_directory(mode_data)
                self.set_mode_data(mode)
                # print(f"Data for mode {mode} has been set in directory {mode_directory}.")
            else:
                print("Invalid selection!")

        except KeyboardInterrupt:
            print("\nExiting...")

def main():
    modes_path = os.getcwd()+'/config/files/interaction_modes.json'
    working_directory = os.getcwd()+'/config/files/working'
    configurator = ModeConfigurator(modes_path, working_directory)
    configurator.configure_mode()

if __name__ == "__main__":
    main()
