import json
import shutil
import os
import datetime
import subprocess

def load_configuration():
    with open('assets/configuration.json', 'r') as file:
        return json.load(file)


def save_configuration(configuration):
    with open('assets/configuration.json', 'w') as file:
        json.dump(configuration, file, indent=4)


def parse_version(version_string):
    return [int(component) for component in version_string.split('.')]


def format_version(version_list):
    return '.'.join(map(str, version_list))


def cleanup_temporary_files():
    if os.path.exists('temporary'):
        shutil.rmtree('temporary')


def clear_binary_folder():
    if os.path.exists('binary'):
        shutil.rmtree('binary')
    os.makedirs('binary', exist_ok=True)


def save_crash_log(error_output, build_type):
    os.makedirs('binary', exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    crash_filename = f'binary/crash_{timestamp}.txt'
    with open(crash_filename, 'w') as crash_file:
        crash_file.write("If you believe this is a software related issue, please report it at: https://github.com/shrezird/Bloxel/issues/new\n")
        crash_file.write("=" * 80 + "\n")
        crash_file.write(f"Build Mode: {build_type}\n")
        crash_file.write(f"Timestamp: {datetime.datetime.now()}\n")
        crash_file.write("=" * 80 + "\n")
        crash_file.write("Build Error Output:\n")
        crash_file.write("=" * 80 + "\n")
        crash_file.write(error_output)


def update_version(configuration, build_type):
    current_version = parse_version(configuration['product_version'])
    release_version, hotfix_version, developer_version = current_version
    current_file_version = [int(component.strip()) for component in configuration['file_version'].split(',')]
    build_count = current_file_version[0] + 1
    is_release_build = 1 if build_type == 'release' else 0
    is_hotfix_build = 1 if build_type == 'hotfix' else 0
    is_developer_build = 1 if build_type == 'developer' else 0
    if build_type == 'developer':
        developer_version += 1
    elif build_type == 'release':
        release_version += 1
        hotfix_version = 0
        developer_version = 0
    elif build_type == 'hotfix':
        hotfix_version += 1
        developer_version = 0
    updated_product_version = [release_version, hotfix_version, developer_version]
    configuration['product_version'] = format_version(updated_product_version)
    configuration['file_version'] = f"{build_count}, {is_release_build}, {is_hotfix_build}, {is_developer_build}"
    return configuration


def create_version_file(configuration):
    file_version = configuration['file_version']
    version_content = f'''VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=({file_version})
    ),
    kids=[
        StringFileInfo([
            StringTable(
                '040904B0',
                [
                    StringStruct('FileDescription', '{configuration["description"]}'),
                    StringStruct('ProductName', '{configuration["name"]}'),
                    StringStruct('ProductVersion', '{configuration["product_version"]}'),
                    StringStruct('LegalCopyright', '{configuration["copyright"]}')
                ]
            )
        ]),
        VarFileInfo([VarStruct('Translation', [1033, 1200])])
    ]
)'''
    
    with open('temporary/engine/version.txt', 'w') as version_file:
        version_file.write(version_content)


def copy_engine_and_icon(build_type):
    os.makedirs('temporary', exist_ok=True)
    engine_source_path = '../engine'
    engine_destination_path = 'temporary/engine'
    if os.path.exists(engine_source_path):
        if os.path.exists(engine_destination_path):
            shutil.rmtree(engine_destination_path)
        shutil.copytree(engine_source_path, engine_destination_path)
        if build_type in ['release', 'hotfix']:
            icon_source_path = 'assets/icon_release.ico'
            icon_filename = 'icon_release.ico'
        else:
            icon_source_path = 'assets/icon_developer.ico'
            icon_filename = 'icon_developer.ico'
        icon_destination_path = f'{engine_destination_path}/{icon_filename}'
        shutil.copy2(icon_source_path, icon_destination_path)
        return True
    else:
        return False


def run_build_command(configuration, build_type):
    if build_type in ['release', 'hotfix']:
        command = configuration['release_and_hotfix']
    else:
        command = configuration['developer']
    print(f"\n{'=' * 80}")
    print("BUILDER - BUILDING BINARY PLEASE WAIT...")
    print("\nWarning: Build process may take a few minutes, do not close this window!")
    print(f"{'=' * 80}")
    engine_directory = 'temporary/engine'
    original_directory = os.getcwd()
    os.chdir(engine_directory)
    build_result = subprocess.run(command, shell=True, capture_output=True, text=True)
    os.chdir(original_directory)
    if build_result.returncode == 0:
        distribution_folder = f'{engine_directory}/dist'
        main_executable_path = f'{distribution_folder}/main.exe'
        if os.path.exists(main_executable_path):
            bloxel_executable_path = f'{distribution_folder}/Bloxel.exe'
            shutil.move(main_executable_path, bloxel_executable_path)
            final_executable_path = 'binary/Bloxel.exe'
            shutil.copy2(bloxel_executable_path, final_executable_path)
            return True
        else:
            return False
    else:
        crash_output = f"{build_result.stdout}\n{build_result.stderr}".strip()
        save_crash_log(crash_output, build_type)
        return False


def display_help():
    print("\n" + "=" * 80)
    print("BUILDER - HELP")
    print()
    print("release    - Builds a fully featured binary intended for public distribution.")
    print()
    print("hotfix     - Builds a binary containing targeted fixes for issues found in a")
    print("             previous public distribution.")
    print()
    print("developer  - Builds a binary with console output enabled, intended for")
    print("             internal testing of unreleased features.")
    print("=" * 80)


def get_build_type():
    while True:
        user_choice = input("\nMode: ").strip().lower()
        if user_choice in ['developer', 'release', 'hotfix']:
            return user_choice
        elif user_choice == 'help':
            display_help()
        else:
            print("\n" + "=" * 80)
            print("Available modes: help, release, hotfix, developer")
            print("=" * 80)


def process_build(build_type):
    clear_binary_folder()
    configuration = load_configuration()
    original_configuration = configuration.copy()
    previous_version = configuration['product_version']
    configuration = update_version(configuration, build_type)
    save_configuration(configuration)
    if not copy_engine_and_icon(build_type):
        save_configuration(original_configuration)
        print(f"\n{'=' * 80}")
        print("BUILDER - BUILD FAILED!")
        print("\nWarning: 'engine' folder is missing outside current folder! Cleaning up...")
        print(f"{'=' * 80}")
        cleanup_temporary_files()
        print("BUILDER - PRESS ENTER TO EXIT...")
        print("=" * 80)
        input()
        return False
    create_version_file(configuration)
    if not run_build_command(configuration, build_type):
        save_configuration(original_configuration)
        print(f"\n{'=' * 80}")
        print("BUILDER - BUILD FAILED!")
        print("\nWarning: Build process failed, check crash log in binary folder! Cleaning up...")
        print(f"{'=' * 80}")
        cleanup_temporary_files()
        print("BUILDER - PRESS ENTER TO EXIT...")
        print("=" * 80)
        input()
        return False
    print(f"\n{'=' * 80}")
    print("BUILDER - BUILD COMPLETED SUCCESSFULLY!")
    print(f"\nBuild Type: {build_type}")
    print(f"Product Version: {previous_version} → {configuration['product_version']}")
    print(f"File Version: {configuration['file_version']}")
    print(f"{'=' * 80}")
    cleanup_temporary_files()
    return True


def main():
    print("=" * 80)
    print("BUILDER - A SEMI-AUTOMATED BINARY BUILDER FOR BLOXEL")
    print("\nReport any issues at: https://github.com/shrezird/Bloxel/issues/new")
    print("=" * 80)
    print("Available modes: help, release, hotfix, developer")
    print("=" * 80)
    while True:
        selected_build_type = get_build_type()
        if not process_build(selected_build_type):
            break
        print("BUILDER - PRESS ENTER TO EXIT...")
        print("=" * 80)
        input()
        break


if __name__ == "__main__":
    main()