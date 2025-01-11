import pandas as pd
from app.schemas.enum import Tag

excel_data = pd.ExcelFile("texts.xlsx")

# Parse and clean the data
def extract_data(sheet_name: str):
    df = excel_data.parse(sheet_name)
    
    # Clean the dataframe by renaming columns
    df = df.rename(columns={
        'V-Map Basic B-1': 'id',
        'Unnamed: 1': 'name',
        'Unnamed: 2': 'tag',
        'Unnamed: 3': 'k_description'
    })
    
    # Drop unnecessary columns
    df = df[['id', 'name', 'tag', 'k_description']]
    
    # Convert DataFrame to List[Dict]
    data = df.to_dict(orient='records')
    return data

# Extract data from each sheet
all_data = {}
for sheet_name in excel_data.sheet_names:
    all_data[sheet_name] = extract_data(sheet_name) # type: ignore

# Combine all sheets into a single list
combined_data = [entry for sheet_data in all_data.values() for entry in sheet_data]

# print(combined_data)
from app.schemas.problem import Text
def map_tag(tag_str: str) -> Tag:
    tag_mapping = {
        "v.": Tag.VERB,
        "n.": Tag.NOUN,
        "adj.": Tag.ADJECTIVE,
        "adv.": Tag.ADVERB,
        "pron.": Tag.PRONOUN,
        "prep.": Tag.PREPOSITION,
        "conj.": Tag.CONJUNCTION,
        "interj.": Tag.INTERJECTION,
    }
    # 태그 매핑에 없거나 nan이면 UNDECIDED 반환
    return tag_mapping.get(tag_str, Tag.UNDECIDED)
from sqlmodel import Session, insert, select

stmts = []
for i, data in enumerate(combined_data):
    if type(data['name']) != str:
        continue
    
    if 'Word' in data['name']:
        continue

    
    text = Text(id=i, name=data['name'], tag=map_tag(data['tag']), k_description=data['k_description'])

    stmt = insert(Text).values(id=i, name=data['name'], tag=map_tag(data['tag']), k_description=data['k_description'])
    
    stmts.append(stmt)


from app.core.db import engine
print(stmts)

try:
    with Session(engine) as s:
        for st in stmts:
            s.exec(st)
        s.commit()
        
        res=s.exec(select(Text)).fetchall()
except Exception as e:
    raise(e)

print(res)