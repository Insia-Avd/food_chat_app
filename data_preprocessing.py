import pandas as pd
import ast

def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)

    df['ingredients'] = df['ingredients'].apply(ast.literal_eval)
    df['nutritions'] = df['nutritions'].apply(ast.literal_eval)
    df['Times'] = df['Times'].apply(ast.literal_eval)

    def make_search_text(row):
        parts = [
            str(row['name']),
            str(row['course']),
            str(row['cusine']),
            str(row['keyword']),
            str(row['summary']),
            ' '.join(row['ingredients']),
            ' '.join([f"{k} {v}" for k, v in row['nutritions'].items()]),
            ' '.join([f"{k} {v}" for k, v in row['Times'].items()]),
        ]
        return ' '.join(parts).lower()

    df['search_text'] = df.apply(make_search_text, axis=1)
    return df

def get_recipe_details(row):
    # Accept Series or dict
    if isinstance(row, dict):
        d = row
    else:
        d = row.to_dict()
    ingredients = ", ".join(d['ingredients'])
    nutritions = "\n".join([f"{k}: {v}" for k, v in d['nutritions'].items()])
    times = "\n".join([f"{k}: {v}" for k, v in d['Times'].items()])
    return {
        'name': d['name'],
        'course': d['course'],
        'cuisine': d['cusine'],
        'keyword': d['keyword'],
        'summary': d['summary'],
        'ingredients': ingredients,
        'nutritions': nutritions,
        'times': times,
        'imgurl': d['imgurl']
    }
