
import instaloader
import ins_db
from time import sleep
import time
from random import randint
import os
import instaloader_firefox_login
import pandas as pd
from ast import literal_eval



class InsDL:

    def __init__(self) -> None:
        """
        Parameters:
        self.target (str): target you'd like to check 
        self.login_username (str): The Instagram login account which should already be saved in the session file

        """
        self.target = "pikaland.au"
        self.login_username = "pikaland.au"
        
    def get_dont_follow_back(self) -> set:
        """
        Summary of the Function:
        Get a set of followers and a set of followings, then return a set of those followings who didn't
        follow back.

        Returns:
        following_dont_follow_back (set)
        
        """

        start_time = time.time()
        followings_set = set()

        for index, followee in enumerate(self.profile.get_followees()):
            if index%37 == 0:
                sleep(randint(4, 7))
                followings_set.add(followee.username)
                
            else:
                followings_set.add(followee.username)
                
        print(f"\nTotal amount of followings: {len(followings_set)}")
        
        followers_set = set()
        for index, follower in enumerate(self.profile.get_followers()):
            if index%37 == 0:
                sleep(randint(4, 7))
                followers_set.add(follower.username)
                
            else:
                followers_set.add(follower.username)
                
        print(f"\nTotal amount of followers: {len(followers_set)}\n")

        exception_set = set(ins_db.common_info_database["target"][self.target]['exception_set'])

        following_follow_back = followings_set & followers_set
        following_follow_back.update(exception_set)

        following_dont_follow_back = followings_set - following_follow_back
        number_of_following_dont_follow_back = len(following_dont_follow_back)
        end_time = time.time()
        total_time = round(end_time - start_time)

        print(f"""##############################\n
Username: {self.target}              

Followee doesn't follow back:
        
{following_dont_follow_back}
        
Total amount of don't follow back: {number_of_following_dont_follow_back}\n
##############################""")
        
        if total_time > 60:
            print(f"\nTotal Processing time: {round((end_time - start_time)/60)} mins {round(end_time - start_time)%60} secs\n")
        else:
            print(f"\nTotal Processing time: {round(end_time - start_time)} secs\n")

        return following_dont_follow_back
        
    def get_user_profile(self) -> None:
        """
        Summary of the Function:
        Get the profile information of the user account

        """
        try:
            self.profile_dict = {}
            self.profile = instaloader.Profile.from_username(DL.context, self.target)
            self.profile_dict['profile.username'] = self.username = self.profile.username
            self.profile_dict['profile.userid'] = self.profile.userid
            self.profile_dict['profile.full_name'] = self.profile.full_name
            self.profile_dict['profile.followers'] = self.profile.followers
            self.profile_dict['profile.followees'] = self.profile.followees
            self.profile_dict['profile.biography'] = self.profile.biography
            self.profile_dict['profile.profile_pic_url'] = self.profile.profile_pic_url
            return self.profile_dict
            
        except instaloader.exceptions.ProfileNotExistsException:
            print(f'Profile "{self.target}" does not exist.')
            exit()

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            exit()

    def input_from_csv(self) -> set:
        """
        Summary of the Function:
        Input the CSV file, 'updated_dont_follow_back.csv'.
        Which includes a list of remaining followings didn't follow back that haven't been removed

        Returns:
        following_dont_follow_back (set)
        
        """

        if not os.path.exists(os.path.join(os.getcwd(), 'updated_dont_follow_back.csv')):
            self.df = pd.DataFrame(pd.DataFrame(), columns=['target_user', 'dont_follow_back_list', 'amount'])
            self.df.to_csv('updated_dont_follow_back.csv', index=False)
        
        else:
            self.df = pd.read_csv('updated_dont_follow_back.csv')

            if self.target in self.df['target_user'].values:
                original_dont_follow_back_set = set(literal_eval(list(self.df[self.df['target_user'] == self.target]['dont_follow_back_list'])[0]))
                return original_dont_follow_back_set
        return set()

    def output_to_csv(self, updated_dont_follow_back_list) -> None:
        """
        Summary of the Function:
        Output the updated list to the CSV file, 'updated_dont_follow_back.csv'.

        Parameters:
        updated_dont_follow_back_list (list)
        
        """
        df_outer_list = []
        df_inner_list = []

        df_inner_list.append(self.target)
        df_inner_list.append(updated_dont_follow_back_list)
        df_inner_list.append(len(updated_dont_follow_back_list))
        df_outer_list.append(df_inner_list)

        
        if self.target in self.df['target_user'].values:

            self.df.loc[self.df['target_user'] == self.target, 'dont_follow_back_list'] = str(updated_dont_follow_back_list)
            self.df.loc[self.df['target_user'] == self.target, 'amount'] = len(updated_dont_follow_back_list)
            self.df.to_csv('updated_dont_follow_back.csv', index=False)

        else:
            self.df = pd.DataFrame(df_outer_list, columns=['target_user', 'dont_follow_back_list', 'amount'])
        
            self.df.to_csv('updated_dont_follow_back.csv', mode = 'a', index=False, header=False)
        
DL = instaloader.Instaloader()

def main():
    Insdl = InsDL()
    def dont_follow_back_run():
        """
        Summary of the Function:
        1. Get the profile information of the targeted user
        2. login an instagram account
        3. Input CSV file
        4. Get the most updated list of followings didn't follow back
        5. Updated the list and output it to the CSV file

        """

        Insdl.get_user_profile()
        DL.load_session_from_file(Insdl.login_username)

        print(f"""##############################\n
Admin is Running: {Insdl.login_username}\n
Target account is Running: {Insdl.target}\n
##############################""")
        
        original_dont_follow_back_set = Insdl.input_from_csv()
        new_dont_follow_back_set = Insdl.get_dont_follow_back() #example: 1, 2, 3, 4, 5, 6, 9
        new_dont_follow_back_user_group = list(new_dont_follow_back_set - original_dont_follow_back_set) #  (1, 2, 3, 7, 8) - (1, 2, 3, 4, 5, 6, 9) = (7, 8)
        updated_original_dont_follow_back_set = new_dont_follow_back_set & original_dont_follow_back_set #2, 3, 1 or 2, 1, 3 and etc...
        updated_original_dont_follow_back_list = list(updated_original_dont_follow_back_set)

        if new_dont_follow_back_user_group: # if there is a new dont follow back user
            updated_original_dont_follow_back_list.extend(new_dont_follow_back_user_group)

        if len(updated_original_dont_follow_back_list) > 0:
            Insdl.output_to_csv(updated_original_dont_follow_back_list)
        else:
            print("Script didn't run properly")
        
    dont_follow_back_run()

if __name__=='__main__':
    main()





   

        



