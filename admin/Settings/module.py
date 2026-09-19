from firstRun import get_absolute_path

file_path = get_absolute_path()

log_settings_path = f'{file_path}\\Settings\\log\\'


def url_in_raw(url: str) -> str:
    return url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")


filename_settings: str = f'{file_path}\\Settings\\UpdateProgram\\UpdateData\\settingsProgram.json'
filename_url: str = f'{file_path}\\Settings\\UpdateProgram\\UpdateData\\update_url_file.json'

file_path_settings_page: str = f'{file_path}\\Settings\\SettingsPage\\settings_page.json'

version_url: str = url_in_raw('https://github.com/RustFarmer/Test/blob/main/settingsProgram.json')

git_hab_url = 'https://github.com'

file_data_url = url_in_raw('https://github.com/RustFarmer/Test/blob/main/update_url_file.json')
