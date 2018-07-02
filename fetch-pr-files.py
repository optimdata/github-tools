import os
from github import Github
import argparse


def comma_split(t):
    return t.split(',')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Github tool')
    parser.add_argument('-p', dest='pull', type=int, help='Id of the pull request', required=True)
    parser.add_argument('-o', dest='organization', help='Organization name', required=False)
    parser.add_argument('-r', dest='repo', help='Repository', required=True)
    args = parser.parse_args()

    if os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN'):
        g = Github(os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN'))
    else:
        g = Github(os.getenv('GITHUB_USER'), os.getenv('GITHUB_PASSWORD'))

    if args.organization:
        repo = g.get_organization(args.organization).get_repo(args.repo)
    else:
        repo = g.get_user().get_repo(args.repo)

    pull = repo.get_pull(args.pull)
    print('# %s ' % pull)
    print('')
    print('## Files')
    print('')
    for f in pull.get_files():
        print('- [ ] %s' % f.filename)
