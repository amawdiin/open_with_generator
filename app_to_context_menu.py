import os
from collections import defaultdict

def print_intro():
    print('========================================')
    print('Program to context menu generator v1.0.0')
    print('========================================')
    print('')

def create_directory(APP_NAME):
    open_with_dir = f'open_with_{"_".join(APP_NAME.split()).lower()}'
    while os.path.exists(open_with_dir): 
        print("Directory already exists, try a different app name")
        APP_NAME = input('Enter app name, example:\nAppName\n')
        open_with_dir = f'open_with_{"_".join(APP_NAME.split()).lower()}'
    os.mkdir(open_with_dir)
    return open_with_dir

def replace_and_write(APP_NAME, APP_PATH, registry_keys):
    # Replace occurrences of 'APP_NAME' and 'APP_PATH' with the provided variables
    output_string = registry_keys.replace('APP_NAME', APP_NAME).replace('APP_PATH', APP_PATH)

    # Write the output string to 'setup.reg'
    with open('setup.reg', 'w') as f:
        f.write(output_string)

def convert_path(path):
    # Replace single backslashes with double backslashes
    new_path = path.replace("\\", "\\\\")
    # Add double quotes around the path
    new_path = f'\\"{new_path}\\"'
    return new_path

def generate_setup_content(settings):
    setup_file = ''
    setup_template = defaultdict()
    setup_template['file'] = r'''

[HKEY_CLASSES_ROOT\*\shell\OpenWithAPP_NAME]
@="Open with APP_NAME"
"Icon"="APP_PATH"

[HKEY_CLASSES_ROOT\*\shell\OpenWithAPP_NAME\command]
@="\"APP_PATH\" \"%1\""
    '''
    setup_template['directory'] = r'''

[HKEY_CLASSES_ROOT\Directory\shell\OpenWithAPP_NAME]
@="Open with APP_NAME"
"Icon"="APP_PATH"

[HKEY_CLASSES_ROOT\Directory\shell\OpenWithAPP_NAME\command]
@="\"APP_PATH\" \"%1\""
    '''
    setup_template['directory_background'] = r'''

[HKEY_CLASSES_ROOT\Directory\background\shell\OpenWithAPP_NAME]
@="Open with APP_NAME"
"Icon"="APP_PATH"

[HKEY_CLASSES_ROOT\Directory\background\shell\OpenWithAPP_NAME\command]
@="\"APP_PATH\" \"%V\""
    '''
    settings['APP_PATH'] = convert_path(settings['APP_PATH'])

    if settings['file'].lower() != "n":
        setup_template['file'] = setup_template['file'].replace('APP_NAME', settings['APP_NAME'])
        setup_template['file'] = setup_template['file'].replace('APP_PATH', settings['APP_PATH'])
        setup_file += setup_template['file']
    elif settings['directory'].lower() != "n":
        setup_template['directory'] = setup_template['directory'].replace('APP_NAME', settings['APP_NAME'])
        setup_template['directory'] = setup_template['directory'].replace('APP_PATH', settings['APP_PATH'])
        setup_file += setup_template['file']
    elif settings['directory_background'].lower() != "n":
        setup_template['directory_background'] = setup_template['directory_background'].replace('APP_NAME', settings['APP_NAME'])
        setup_template['directory_background'] = setup_template['directory_background'].replace('APP_PATH', settings['APP_PATH'])
        setup_file += setup_template['file']
    return setup_file

def generate_uninstall_content(settings):
    return r'''
@echo off

reg delete HKEY_CLASSES_ROOT\Directory\background\shell\OpenWithAPP_NAME /f
reg delete HKEY_CLASSES_ROOT\*\shell\OpenWithAPP_NAME /f
reg delete HKEY_CLASSES_ROOT\Directory\shell\OpenWithAPP_NAME /f
    '''.replace("APP_NAME", settings['APP_NAME'])

def main():
    print_intro()
    settings = defaultdict()
    settings['APP_NAME'] = input('Enter app name, example: AppName\n')
    settings['APP_PATH'] = input('\nEnter app path, example: C:\\Program Files\\AppName\\app.exe\n')
    directory = create_directory(settings['APP_NAME'])
    print(f'Directory {directory} created successfully!')

    print('Do you want your app to be present in context menu when right clicking:')
    settings["file"] = input('file (y/n): ')
    settings["directory"] = input('directory (y/n): ')
    settings["directory_background"] = input('directory background(y/n): ')

    setup_file = generate_setup_content(settings)
    uninstall_file = generate_uninstall_content(settings)

    with open(f'{directory}/setup.reg', 'w') as f:
        f.write(setup_file)
    print('File setup.reg created successfully!')
    with open(f'{directory}/remove.bat', 'w') as f:
        f.write(uninstall_file)
    print('File remove.bat created successfully!')
    input('\nDONE!\npress enter to close this window\n')

if __name__ == "__main__":
    main()
