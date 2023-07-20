from lib.writing.visitors.PDFAccessorVisitor import PDFAccessorVisitor
from lib.utils.normalize_filename import normalize_filename
from lib.utils.get_learningTracks_json import get_learningTracks_json
from lib.utils.get_learningTrack_json import get_learningTrack_json
from lib.utils.learningTrack_from_json import learningTrack_from_json
from lib.utils.get_project_root import get_project_root
from lib.writing.objects.LearningTrackAccessor import LearningTrackAccessor


def process_multiple(owner: str, bearer_token: str):
    
    page = 1
    page_size = 100
    learning_tracks = []
    out_dirpath = get_project_root()
    out_dirpath = out_dirpath / 'out_bulk'
    #time
    # start_time = time.time()
    while True:
        learning_tracks_json = get_learningTracks_json(page, page_size, owner, bearer_token)
        for lt_json in learning_tracks_json:
            try:
              fname = normalize_filename(f'{lt_json["name"]}({lt_json["id"]}).pdf')
              fname = str(out_dirpath / fname )
              # print(fname)
              lt = learningTrack_from_json(lt_json)
              accessor = LearningTrackAccessor(lt)
              accessorVisitor_pdf = PDFAccessorVisitor(fname)
              accessor.accept(accessorVisitor_pdf)
            except Exception as e:
              # Catch any errors and continue processing other learning tracks
              print(e)
              print(f"ERROR: Fault while processing learning track {lt_json['name']}({lt_json['id']})")

        if len(learning_tracks) < page_size:
            break

        page += 1

    # end_time = time.time()
    # print(f"Processed {page_size * (page - 1) + len(learning_tracks)} learning tracks in {end_time - start_time} seconds")
    # print(f"Average time per learning track: {(end_time - start_time) / (page_size * (page - 1) + len(learning_tracks))} seconds") 

def process_single_azure(api_url: str, bearer_token: str):
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
      File stream of the pdf file
    """
    
    lt_json = get_learningTrack_json(api_url, bearer_token)

    lt = learningTrack_from_json(lt_json)

    accessor = LearningTrackAccessor(lt)
    accessorVisitor_pdf = PDFAccessorVisitor('filler.pdf')
    accessor.accept(accessorVisitor_pdf)
    return accessorVisitor_pdf.file_writer.get_file_stream()


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
    lt_json = get_learningTrack_json(api_url, bearer_token)
    
    #root dir
    out_dirpath = get_project_root()
    out_dirpath = out_dirpath / 'out'

    fname = normalize_filename(f'{lt_json["name"]}({lt_json["id"]}).pdf') # What if name has /, \, ., etc.?
    fname = str(out_dirpath / fname ) 

    lt = learningTrack_from_json(lt_json)

    print("writing learning track to pdf file...")
    print(fname)
    accessor = LearningTrackAccessor(lt)
    accessorVisitor_pdf = PDFAccessorVisitor(fname)
    accessor.accept(accessorVisitor_pdf)
    print("done!")
    return fname