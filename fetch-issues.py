from datetime import date
import os
import re
from github import Github
import argparse


def comma_split(t):
    return t.split(',')

CATEGORIES = {
    'majors': {'label': 'Major features', 'marketing': True},
    'minors': {'label': 'Minor features', 'marketing': True},
    'bugs': {'label': 'Bug fixes', 'marketing': True},
    'internals': {'label': 'Internal tickets', 'marketing': True},
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Github tool')
    parser.add_argument('-m', dest='milestone', help='Name of the milestone', required=True)
    parser.add_argument('-r', dest='repos', type=comma_split, help='Comma separated list of repositories', required=True)
    args = parser.parse_args()

    if os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN'):
        g = Github(os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN'))
    else:
        g = Github(os.getenv('GITHUB_USER'), os.getenv('GITHUB_PASSWORD'))

    repos = [repo for repo in g.get_user().get_repos() if repo.full_name in args.repos]

    issues = {category: [] for category in CATEGORIES}
    print('### %s' % args.milestone)
    print('')
    print('*%s*' % date.today().strftime('%B %d %Y'))
    print('')
    print('**InUse** and **InLab** platforms have been upgraded to the version %s' % args.milestone)
    print('')
    for repo in repos:
        milestones = [milestone for milestone in repo.get_milestones(state='all') if milestone.title == args.milestone]
        if not milestones:
            continue
        milestone = milestones[0]
        for issue in repo.get_issues(milestone=milestone, state='all'):
            if '/pull/' not in issue.html_url:
                labels = [label.name for label in issue.labels]
                if 'structure' in labels:
                    issues['internals'].append(issue)
                elif 'bug' in labels:
                    issues['bugs'].append(issue)
                elif 'enhancement' in labels:
                    issues['minors'].append(issue)
                elif 'feature' in labels:
                    issues['majors'].append(issue)
                else:
                    raise ValueError('Cannot find category for %s' % issue)

    for category in ('majors', 'minors', 'bugs', 'internals'):
        if not issues[category]:
            continue

        print('#### %s' % CATEGORIES[category]['label'])
        print('')
        for issue in issues[category]:
            print('- [%s #%s](%s)' % (issue.title, issue.number, issue.html_url))
            if CATEGORIES[category]['marketing']:
                for comment in issue.get_comments():
                    if re.match('[#]+ Marketing[\r\n]+', comment.body):
                        print('')
                        print(re.sub('[#]+ Marketing[\r\n]+', '', comment.body.encode('utf8')))
                        print('')
                        break
        print('')
