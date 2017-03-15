# Github tools

Github is great but some features are missing when it comes to project which involves several repositories. Some of the tools in this repository will help this.

## Installation

```bash
$> pip install -r requirements.txt
```

Then you have to setup two self-explanatories environment variables: `GITHUB_USER` and `GITHUB_PASSWORD`.

## Update milestone

The goal of this script is to synchronize milestone due date between several repositories. Let's say you have two repos `foo` and `bar`, a milestone `0.1.0` scheduled for 2017/02/02

```bash
$> python update-milestone.py -m 0.1.0 -d 20170202 -r foo,bar
```

## Fetch issues

The goal of this script is to fetch issues from several repositories under the same milestone (identified by name). It will output issues grouped by repo in a markdown syntax:

```bash
$> python fetch-issues.py -m 0.1.0 -d 20170202 -r foo,bar

# foo

- [Fix this #1](https://github.com/myorganization/foo/issues/1)
- [Implement this #2](https://github.com/myorganization/foo/issues/2)

# bar

- [Fix that #1](https://github.com/myorganization/bar/issues/1)
- [Implement that #2](https://github.com/myorganization/bar/issues/2)
```

## Fetch PR files

The goal of this script is to fetch files modified in a pull request and display it in a list

```bash
$> python fetch-pr-files.py -o myorganization -r myrepo -p 1

# PullRequest(title="First PR", number=1)

## Files

models.py
views.py
