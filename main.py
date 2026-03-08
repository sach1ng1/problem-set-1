'''
You will run this problem set from main.py so set things up accordingly
'''

import src.transform_load as trl

# Call functions / instanciate objects from the two analysis .py files
def main():
        """
        main function calls functions from the extract and tranform_load files
        """        
        # Call functions from extract.py
        tr_df,wth_df=trl.read_df() 

        # Call functions from transform_load.py
        new_tr_df, new_wth_df= trl.clean_df(tr_df, wth_df)   
        new_tr_wth_df=trl.merge_filter_df(new_tr_df, new_wth_df)
        trl.create_viz(new_tr_wth_df)


if __name__ == "__main__":
    main()