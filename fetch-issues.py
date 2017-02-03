import os
from github import Github
import argparse


def comma_split(t):
    return t.split(',')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Github tool')
    parser.add_argument('-m', dest='milestone', help='Name of the milestone', required=True)
    parser.add_argument('-r', dest='repos', type=comma_split, help='Comma separated list of repositories', required=True)
    args = parser.parse_args()

    g = Github(os.getenv('GITHUB_USER'), os.getenv('GITHUB_PASSWORD'))

    repos = [repo for repo in g.get_user().get_repos() if repo.full_name in args.repos]

    print('Got %s repos' % len(repos))

    for repo in repos:
        print('# %s ' % repo.name)
        print()
        milestones = [milestone for milestone in repo.get_milestones() if milestone.title == args.milestone]
        if not milestones:
            continue
        milestone = milestones[0]
        issues = repo.get_issues(milestone=milestone, state='all')
        for issue in issues:
            if '/pull/' not in issue.html_url:
                print('- [%s #%s](%s)' % (issue.title, issue.number, issue.html_url))
        print()
