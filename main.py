import argparse, os
from dotenv import load_dotenv
from lib.utils.Authenticator import Authenticator
from lib.utils.EnvUtils import get_lt_api_url

from lib.utils.processing import process_single, process_multiple

def main():
    args = parse_cli_args()

    load_dotenv()

    username = args.username if args.username else os.getenv("USERNAME")
    password = args.password if args.password else os.getenv("PASSWORD")
    Authenticator(username, password) # init singleton Authenticator instance
    bearer_token = Authenticator.get_instance().get_bearer_token()

    owner = args.owner if args.owner else os.getenv("OWNER")

    if owner:
        process_multiple(owner, bearer_token)
    else:
        api_url = get_lt_api_url(args.learning_track_url) if args.learning_track_url else get_lt_api_url(os.getenv("URL"))
        process_single(api_url, bearer_token)        


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='Username for API authentication')
    parser.add_argument('-p', '--password', help='Password for API authentication')
    # parser.add_argument('-bt', '--bearer_token', help='Alternative for username and password')
    parser.add_argument('-url', '--learning_track_url', help='URL of the learning track in your library (used if --owner is not specified)')
    parser.add_argument('-o', '--owner', help='For processing multiple learning tracks, specify the owner of the learning tracks you want to access. Options are Own, School, Other. Default is Own.')
    return parser.parse_args()    


if __name__ == '__main__':
    main()