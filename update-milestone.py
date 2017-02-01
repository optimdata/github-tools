import os
from dateutil.parser import parse as parse_date
from github import Github
import argparse


def comma_split(t):
    return t.split(',')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Github tool')
    parser.add_argument('-d', dest='date', type=parse_date, help='Date of the milestone', required=True)
    parser.add_argument('-m', dest='milestone', help='Name of the milestone', required=True)
    parser.add_argument('-r', dest='repos', type=comma_split, help='Comma separated list of repositories', required=True)
    args = parser.parse_args()

    g = Github(os.getenv('GITHUB_USER'), os.getenv('GITHUB_PASSWORD'))

    repos = [repo for repo in g.get_user().get_repos() if repo.full_name in args.repos]

    print('Got %s repos' % len(repos))

    for repo in repos:
        milestones = [milestone for milestone in repo.get_milestones() if milestone.title == args.milestone]
        if milestones:
            milestone = milestones[0]
        else:
            milestone = repo.create_milestone(title=args.milestone)
        milestone.edit(title=milestone.title, due_on=args.date)
        print('Updated %s:%s. Set due date to %s' % (repo.name, milestone.title, args.date))
