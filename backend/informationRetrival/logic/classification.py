from pathlib import Path
from pickle import load


def get_classification_story_for_query(query: str) -> str:
    cwd = Path(__file__).parent.resolve()
    pickle_file_path = cwd / Path('classification_pickle.pkl')
    with open(pickle_file_path, 'rb') as f:
        p = load(f)

    y_pred = [int(y['label'].split('_')[1]) for y in p([' '.join(query[0])])]
    names = ['داستان دوازده رخ', 'داستان اکوان دیو',
             'داستان رستم و اسفندیار', 'داستان سیاوش']
    return names[y_pred[0]]
