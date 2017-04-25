from github import Github
from argparse import ArgumentParser

with open('manifest.json') as manifest:    
    manifest_dict = json.load(manifest)

class MergeFreezer(object):
    def __init__(self, ghtoken, repos_list):
        self.__ghtoken = ghtoken
        self.__repo_list = repos_list
        self.__gh = Github(ghtoken)

    def get_repo_open_prs(self, repo):
        return self.__gh.get_repo(repo).get_pulls(state="open")

    def get_all_open_prs(self):
        for repo in self.__repo_list():
            

    def freeze_pr(self, pr):
        pass

    def freeze_prs(self, pr_list):
        pass

    def freeze_all_prs(self):
        pass

    def unfreeze_pr(self, pr):
        pass

    def unfreeze_prs(self, pr_list):
        pass

    def unfreeze_all_prs(self):
        pass


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

    parsed_args = parser.parse_args(args)
    return parsed_args

def main():
    parsed_args = parse_args(sys.argv[1:])

if __name__ == "__main__":
    main()
    sys.exit(0)