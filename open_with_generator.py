
import os

def print_intro():
    print('========================================')
    print('Program to context menu generator v1.0.0')
    print('========================================')
    print('')

def create_directory(app_name):
    open_with_dir = f'open_with_{"_".join(app_name.split()).lower()}'
    while os.path.exists(open_with_dir): 
        print("Directory already exists, try a different app name")
        app_name = input('Enter app name, example:\nAppName\n')
        open_with_dir = f'open_with_{"_".join(app_name.split()).lower()}'
    os.mkdir(open_with_dir)
    return open_with_dir

def convert_path(path):
    # Replace single backslashes with double backslashes
    new_path = path.replace("\\", "\\\\")
    # Add double quotes around the path
    new_path = f'\\"{new_path}\\"'
    return new_path

def generate_setup_content(app_name, app_path, registry_keys):
    setup_file = ''
    setup_template = {
        'file': r'''
[HKEY_CLASSES_ROOT\*\shell\OpenWith{app_name}]
@="Open with {app_name}"
"Icon"="{app_path}"

[HKEY_CLASSES_ROOT\*\shell\OpenWith{app_name}\command]
@="{app_path}" "%1"
''',
        'directory': r'''
[HKEY_CLASSES_ROOT\Directory\shell\OpenWith{app_name}]
@="Open with {app_name}"
"Icon"="{app_path}"

[HKEY_CLASSES_ROOT\Directory\shell\OpenWith{app_name}\command]
@="{app_path}" "%1"
''',
        'directory_background': r'''
[HKEY_CLASSES_ROOT\Directory\background\shell\OpenWith{app_name}]
@="Open with {app_name}"
"Icon"="{app_path}"

[HKEY_CLASSES_ROOT\Directory\background\shell\OpenWith{app_name}\command]
@="{app_path}" "%V"
'''
    }
    app_path = convert_path(app_path)

    if registry_keys['file'].lower() == "y":
        setup_file += setup_template['file'].format(app_name=app_name, app_path=app_path)
    if registry_keys['directory'].lower() == "y":
        setup_file += setup_template['directory'].format(app_name=app_name, app_path=app_path)
    if registry_keys['directory_background'].lower() == "y":
        setup_file += setup_template['directory_background'].format(app_name=app_name, app_path=app_path)
    return setup_file

def generate_uninstall_content(app_name):
    return fr'''
@echo off

reg delete HKEY_CLASSES_ROOT\Directory\background\shell\OpenWith{app_name} /f
reg delete HKEY_CLASSES_ROOT\*\shell\OpenWith{app_name} /f
reg delete HKEY_CLASSES_ROOT\Directory\shell\OpenWith{app_name} /f
'''

def main():
    print_intro()
    app_name = input('Enter app name, example: AppName\n')
    app_path = input('\nEnter app path, example: C:\\Program Files\\AppName\\app.exe\n')
    directory = create_directory(app_name)
    print(f'\nDirectory {directory} created successfully!')

    print('\nDo you want your app to be present in context menu when right clicking:')
    registry_keys = {
        "file": input('file (y/n): '),
        "directory": input('directory (y/n): '),
        "directory_background": input('directory background(y/n): ')
    }

    setup_file = generate_setup_content(app_name, app_path, registry_keys)
    uninstall_file = generate_uninstall_content(app_name)

    with open(f'{directory}/setup.reg', 'w') as f:
        f.write(setup_file)
    print('\nFile setup.reg created successfully!')
    with open(f'{directory}/remove.bat', 'w') as f:
        f.write(uninstall_file)
    print('File remove.bat created successfully!')
    input('\nDONE!\npress enter to close this window\n')

if __name__ == "__main__":
    main()
