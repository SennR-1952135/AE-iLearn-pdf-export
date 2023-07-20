import sys, json, argparse, os, pathlib, time
import requests
from dotenv import load_dotenv
from lib.utils.normalize_filename import normalize_filename
from lib.utils.Authenticator import Authenticator
from lib.utils.EnvUtils import get_lt_api_url, get_env_url
from lib.utils.augment_learningTrack_json import augment_learningTrack_json
from lib.utils.DBIDTransformer import DBIDTransformer
from lib.parsing.LearningTrack import learningtrack_from_json
from lib.writing.objects.LearningTrackAccessor import LearningTrackAccessor
from lib.writing.visitors.PDFAccessorVisitor import PDFAccessorVisitor

def main():
    args = parse_cli_args()

    load_dotenv()

    username = args.username if args.username else os.getenv("USERNAME")
    password = args.password if args.password else os.getenv("PASSWORD")
    bearer_token = authenticate_user(username, password)

    owner = args.owner if args.owner else os.getenv("OWNER")

    if owner:
        process_multiple(owner, bearer_token)
    else:
        api_url = get_lt_api_url(args.learning_track_url) if args.learning_track_url else get_lt_api_url(os.getenv("URL"))
        process_single(api_url, bearer_token)     
      

def process_multiple(owner: str, bearer_token: str):
    
    page = 1
    page_size = 100
    learning_tracks = []
    out_dirpath = pathlib.Path(__file__).parent.parent.absolute()
    out_dirpath = out_dirpath / 'out_bulk'
    #time
    # start_time = time.time()
    while True:
        learning_tracks = get_learning_tracks(page, page_size, owner, bearer_token)
        for lt_json in learning_tracks:
            try:
              fname = normalize_filename(f'{lt_json["name"]}({lt_json["id"]}).pdf')
              fname = str(out_dirpath / fname )
              # print(fname)
              lt = lt_from_json(lt_json)
              accessor = LearningTrackAccessor(lt)
              accessorVisitor_pdf = PDFAccessorVisitor(fname)
              accessor.accept(accessorVisitor_pdf)
            except Exception as e:
              print(e)
              print(f"ERROR: Fault while processing learning track {lt_json['name']}({lt_json['id']})")

        if len(learning_tracks) < page_size:
            break
        # if page * page_size >= 100:
        #     break
        page += 1

    # end_time = time.time()
    # print(f"Processed {page_size * (page - 1) + len(learning_tracks)} learning tracks in {end_time - start_time} seconds")
    # print(f"Average time per learning track: {(end_time - start_time) / (page_size * (page - 1) + len(learning_tracks))} seconds") 

def process_single(api_url: str, bearer_token: str):
    """ Process a single learning track (given by url) and write it to a pdf file
    Parameters
    ----------
    api_url : str
        The url of the learning track to process
    bearer_token : str
        The bearer token to use for authentication
    
    Returns
    -------
    str
        The path to the pdf file that was written
    """
    lt_json = get_learning_track_json(bearer_token, api_url)
    
    out_dirpath = pathlib.Path(__file__).parent.parent.absolute()
    out_dirpath = out_dirpath / 'out'

    fname = normalize_filename(f'{lt_json["name"]}({lt_json["id"]}).pdf')
    fname = str(out_dirpath / fname ) # TODO: what if name has /, \, ., etc.?

    # # write response json to file
    # with open(str(out_dirpath) + '/response-lt.json', 'w') as outfile:
    #     json.dump(lt_json, outfile)

    lt = lt_from_json(lt_json)

    # # write lt to files
    # print("writing learning track to json file...")
    # with open(str(out_dirpath / 'output-lt.json'), 'w') as outfile:
    #     json.dump(asdict(lt), outfile)
    # print("done!")
    print("writing learning track to pdf file...")
    print(fname)
    accessor = LearningTrackAccessor(lt)
    accessorVisitor_pdf = PDFAccessorVisitor(fname)
    accessor.accept(accessorVisitor_pdf)
    print("done!")
    return fname
    
def lt_from_json(lt_json: dict):
    augment_learningTrack_json(lt_json)
    transformer = DBIDTransformer() # TODO is this necessary?
    transformer.json(lt_json)
    # parse learning track to object LearningTrack object
    lt = learningtrack_from_json(lt_json)
    return lt

def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='Username for API authentication')
    parser.add_argument('-p', '--password', help='Password for API authentication')
    # parser.add_argument('-bt', '--bearer_token', help='Alternative for username and password')
    parser.add_argument('-url', '--learning_track_url', help='URL of the learning track in your library (used if --owner is not specified)')
    parser.add_argument('-o', '--owner', help='For processing multiple learning tracks, specify the owner of the learning tracks you want to access. Options are Own, School, Other. Default is Own.')
    return parser.parse_args()    

def authenticate_user(username, password) -> str:
    """Authenticate user with username and password, instantiates Singleton Authenticator class

    Returns
    -------
    str: bearer_token
    """
    if username and password:
      print("Authenticating with username and password...")
      bearer_token = Authenticator(username, password).get_bearer_token() # Instantiate Authenticator class and call get_bearer_token method
      print("Authentication successful!")
      return bearer_token
    else:
        print("ERROR: No username and password provided")
        sys.exit(1)
        # bearer_token = args.bearer_token if args.bearer_token else os.getenv("BEARER_TOKEN")
    
def get_learning_track_json(bearer_token, api_url):    
    print("processing url: ", api_url)

    headers = {
        'Authorization': 'Bearer ' + bearer_token,
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code != 200:
        raise Exception("Failed to get learning track json (status code: " + str(response.status_code) + ")" )

    return response.json()

def get_learning_tracks(pageNumber: int = 1, pageSize: int = 50, owner: str = 'Own', bearer_token: str = None):
    """
    Parameters
    ----------
    owner: 'Own', 'School', 'Other'
      The owner(s) of the learning tracks you want to access, default is 'Own'.
    """
    if not bearer_token:
        bearer_token = Authenticator.get_instance().get_bearer_token()
    
    payload = {
        'LearningActivityTypes': [],
        # 'LearningMaterialOwners': ["Own", "School", "Other"],
        # 'LearningMaterialOwners': ["Own"],
        'LearningMaterialOwners': [owner],
        'OrderBy': "Descending",
        'Page': pageNumber,
        'PageSize': pageSize,
        # 'Page': 1,
        # 'PageSize': 5,
        'PublicationStatus': [],
        'Q': [],
        'SkosGroups': [],
        'SortBy': "Date",
        'Tools': [],
        'Types': ["learningTrack"]
    }

    headers = {
        'Authorization': 'Bearer ' + bearer_token,
    }

    api_url = get_env_url() + '/api/learningmaterials/query'

    res = requests.post(api_url, headers=headers, json=payload)

    return res.json()['items']

if __name__ == '__main__':
    main()