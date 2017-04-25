from github import Github
from argparse import ArgumentParser
import sys, json

class MergeFreezer(object):
    def __init__(self, ghtoken, repos_list, freeze_context, freeze_desc, unfreeze_desc):
        self.__ghtoken = ghtoken
        self.__repo_list = repos_list
        self.__gh = Github(ghtoken)
        self.__freeze_context = freeze_context
        self.__freeze_desc = freeze_desc
        self.__unfreeze_desc = unfreeze_desc

    def get_repo_open_prs(self, repo):
        return self.__gh.get_repo(repo).get_pulls(state="open")

    def freeze_pr(self, pr):
        commit = pr.get_commits().reversed[0]
        commit.create_status(state="failure", \
                            description=self.__freeze_desc, \
                            context=self.__freeze_context)

    def freeze_prs(self, pr_list):
        for pr in pr_list:
            if not self.is_frozen(pr):
                self.freeze_pr(pr)

    def freeze_all_prs(self):
        for repo in self.__repo_list():
            repo_open_prs = self.get_repo_open_prs(repo)
            self.freeze_prs(repo_open_prs)

    def unfreeze_pr(self, pr):
        commit = pr.get_commits().reversed[0]
        commit.create_status(state="success", \
                    description=self.__freeze_desc, \
                    context=self.__unfreeze_context)

    def unfreeze_prs(self, pr_list):
        for pr in pr_list:
            if self.is_frozen(pr):
                self.unfreeze_pr(pr)

    def unfreeze_all_prs(self):
        for repo in self.__repo_list():
            repo_open_prs = self.get_repo_open_prs(repo)
            self.unfreeze_prs(repo_open_prs)

    def is_frozen(self, pr):
        commit = pr.get_commits().reversed[0]
        statuses = commit.get_statuses()
        for status in statuses:
            if status.context == self.__freeze_context:
                if status.description == self.__freeze_desc and status.state == "failure":
                    return True
                elif status.description == self.__unfreeze_desc and status.state == "success":
                    return False
                else:
                    print "Commit status in wrong format!"
                    sys.exit(1)
            else:
                continue
        return False

def parse_args(args):
    parser = ArgumentParser()
    parser.add_argument("--ghtoken",
                        help="Github token that have commit status set permission.",
                        required=True,
                        action="store")
    parser.add_argument("--manifest-file",
                        help="The file path of manifest which is the repo information source",
                        required=True,
                        action="store")
    parser.add_argument("--freeze-context",
                        help="The context of freeze pr commit status",
                        required=True,
                        action="store")
    parser.add_argument("--freeze-desc",
                        help="The description of freeze pr commit status",
                        required=True,
                        action="store")
    parser.add_argument("--unfreeze-desc",
                        help="The description of unfreeze pr commit status",
                        required=True,
                        action="store")

    parsed_args = parser.parse_args(args)
    return parsed_args

def main():
    with open('manifest.json') as manifest:
        manifest_dict = json.load(manifest)
    for repo_info in manifest_dict["repositories"]:
        repo_url = repo_info["repository"]
        repo = 
    parsed_args = parse_args(sys.argv[1:])

if __name__ == "__main__":
    main()
    sys.exit(0)