import os
import sys
import shutil
import requests

install_path = 'C:/monolith'

# format download size
def sizeof_fmt(num, suffix="B"):
    for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Y{suffix}"

# download file from web url
def download(name, path, url):
    with open(f'{path}/{name}', 'wb') as file:
        response = requests.get(url, allow_redirects=True, stream=True)
        size = response.headers.get('content-length')

        if size is None:
            print(f'  downloading {name}...')
            file.write(response.content)

        else:
            size = int(size)
            print(f'  downloading {name}... ({sizeof_fmt(int(size))})')
            progress = 0
            for data in response.iter_content(chunk_size=4096):
                progress += len(data)
                file.write(data)
                done = int(50 * progress / size)

                sys.stdout.write(f"\r  [{'=' * done}{' ' * (50 - done)}] {int(progress / size * 100)}% ")
                sys.stdout.flush()
            print()

if __name__ == "__main__":
    print()

    if os.path.exists(install_path):
        overwrite = input('Previous monolith installation was found. overwrite? (Y/n): ')

        if overwrite == '' or overwrite == 'y' or overwrite == 'Y':
            shutil.rmtree(install_path)

        else:
            print('Operation cancelled. Terminating.')
            sys.exit()


    if not sys.argv[1]:
        print('No tag specified!')
        sys.exit()

    tag = sys.argv[1]

    print('Installing monolith in C:/ ...')
    download('monolith.zip', f'{install_path}/..', f'https://github.com/luftaquila/monolith/archive/refs/tags/{tag}.zip')

    print('Unpacking monolith...')
    shutil.unpack_archive(f'{install_path}.zip', f'{install_path}/..')
    os.rename(f'{install_path}-{tag[1:]}', install_path)
    os.remove(f'{install_path}.zip')

    print('done!')