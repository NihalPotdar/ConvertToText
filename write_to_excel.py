import pandas as pd

def create_dataframe_from_list(lst):
    return pd.DataFrame(lst)

def write(file_name,big_list,*args):
    cols = []

    '''
    for key in args:
        if isinstance(key, list):
            big_list.append(key)

        if isinstance(key, str):
            cols.append(key)
    '''
    df = pd.DataFrame(big_list)
    df.to_csv(file_name, mode='a', index = False, header=None)

if __name__ == "__main__":
    write('pandas_simple.csv', [[8,9,10], [3,4,5]], 'test1', 'test2')