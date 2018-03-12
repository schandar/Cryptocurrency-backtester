import pandas as pd
import datetime

def create_initial_board():
    '''
    Call function only once in python3. Use to create and store
    empty CSV file with appropriate headers.

    Inputs: None
    Returns: None
    '''
    initial_board_df = pd.DataFrame(columns = ["Username", \
        "Strategies", "Absolute Returns", "Relative Resturns", \
        "Sharpe Ratio", "Portfolio"])
    initial_board_df.to_csv("leaderboard.csv", index=False)

def edit_board(new_entry):
    '''
    Edit leaderboard based on Sharpe ratio. Strategies yielding
    top 5 Sharpe ratios will be displayed in leaderboard.

    Inputs: list containing the results of a user's query

    Output: a list of 5 lists containing the best strategies
    attempted on the site to date.
    '''
    leaderboard = pd.read_csv("leaderboard.csv")
    lb_columns = leaderboard.columns.values.tolist()
    new_row = pd.DataFrame(new_entry, columns = lb_columns)
    leaderboard = pd.concat([leaderboard, new_row])
    leaderboard = leaderboard.drop_duplicates('Sharpe Ratio')
    leaderboard = leaderboard.sort_values(by='Sharpe Ratio', ascending=0)
    if leaderboard.shape[0] > 5:
        leaderboard = leaderboard[:-1]
    table = leaderboard.values.tolist()
    leaderboard.to_csv("leaderboard.csv", index=False)
    return table

'''
THIS CODE WAS NOTE USED

class Leaderboard: 
    def __init__(self):
       
        self.size = 10
        self.min_duration = datetime.timedelta(30)
        # requires strategy to run for over 30 days
        self.board = pd.DataFrame(columns=
                     ["Username", "Strategies", "Absolute Returns", "Relative Returns", "Sharpe Ratio", "Portfolio"])

    def edit_board(self, new_entry):
       
        start_date = datetime.datetime.strptime(new_entry[1]["start_date"], '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(new_entry[1]["end_date"], '%Y-%m-%d').date()
        duration = end_date - start_date
        if duration < self.min_duration:
            return False

        self.board.loc[len(self.board)] = new_entry
        self.board.sort_values(by="Sharpe Ratio", ascending=False, inplace=True)
        self.board.reset_index(drop=True, inplace=True)

        if len(self.board) >= self.size:
            self.board = self.board[:self.size]

        self.board.to_csv("leaderboard.csv", index=True, header=self.board.columns)

def make_table(file):

    leaderboard = Leaderboard()
    try:
        leaderboard.board = pd.read_csv("leaderboard.csv", index_col = 0)
    except:
        pass
    
    leaderboard.edit_board(new_entry)

    return leaderboard.board
'''
