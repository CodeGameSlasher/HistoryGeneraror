import requests

url = 'http://github.com/CodeGameSlasher/HistoryGenerator'
file_url = 'https://github.com/CodeGameSlasher/HistoryGenerator/raw/refs/heads/main/src'

def download_file(filename: str = 'words.txt'):
    response = requests.get(f'{file_url}/{filename}')
    with open(f'src/{filename}', 'wb') as file:
        file.write(response.content)

def download_repo():
    response = requests.get(f'{url}/archive/refs/heads/main.zip')
    if response.status_code == 200:
        print('Скачивание репозитория...')
        with open('update.zip', 'wb') as archive:
            archive.write(response.content)
        print('Готово!')
    else:
        print('Репозиторий не найден.')


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        print(f'Скачивание {filename}...')
        download_file(filename)
        print('Готово!')
    else:
        print('Скачивание словаря...')
        download_file()
        print('Готово!')