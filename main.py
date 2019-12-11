from lib.utils.utils import load_configure, load_rss, save_to_json

def get_github_releases():
    repositories = load_configure('releases')
    latest_releases = []
    for repo in repositories:
        url = 'https://github.com/{}/releases'.format(repo['repository'])
        release_notes = load_rss('{}.atom'.format(url))
        latest_release_entry = release_notes['feed']['entry'][0]
        latest_release = {
            'name': repo['name'],
            'url':  '{}/{}'.format(url, latest_release_entry['title']),
            'updated': latest_release_entry['updated'],
            'version': latest_release_entry['title'],
            'note': latest_release_entry['content']['#text']
        }
        latest_releases.append(latest_release)

    save_to_json('output', 'github-releases',latest_releases)

if __name__ == "__main__":
    get_github_releases()
