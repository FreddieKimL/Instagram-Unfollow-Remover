import pyautogui as pya
from time import sleep
from random import randint
import time
import pandas as pd
from ast import literal_eval
import os



class FolRemover:

    def __init__(self) -> None:
         """
        Parameters:
        self.acc_username  (str): login username
        self.acc_pwd (str): login password
        self.del_lower_limit (int): the max amount of targets to be remained in the list e.g. 80
        self.del_upper_limit (int): the max amount of removal each time e.g. 100

        For example, 
        This time, the script will remove up to 100 targets from the list, unless 80 targets are remained in the list, script will stop.

        """
         self.moveing_time = randint(650, 800)/1000
         self.landing_time = randint(360, 380)/100
         self.write_time = randint(10, 18)/1000
         self.acc_username = ""
         self.acc_pwd = ""
         self.del_lower_limit = 88
         self.del_upper_limit = 96

    def check_login_status(self) -> bool:
        """
        Summary of the Function:
        Check whether the instagram account have logged in or not.

        Returns:
        True (bool): Haven't logged in 
        False (bool): Logged in
        
        """
        pya.hotkey("win", "r")
        pya.write(f"https://www.instagram.com/")
        pya.hotkey("enter")
        sleep(self.landing_time)
        status = pya.locateOnScreen("login_username.png", confidence=0.7)
        if status != None:
            return True
        else:
             return False
         
    def login(self) -> None:
        """
        Summary of the Function:
        Log in the Instagram account automatically

        Parameters:
        self.acc_username  (str): login username
        self.acc_pwd (str): login password
        
        Returns:
        True (bool): Haven't logged in 
        False (bool): Logged in
        
        """
        
        x, y = pya.locateCenterOnScreen("login_username.png", confidence=0.7)
        pya.moveTo(x, y, self.moveing_time)
        pya.click()
        pya.write(self.acc_username , interval=(self.write_time*10))

        x, y = pya.locateCenterOnScreen("login_pwd.png", confidence=0.6)
        pya.moveTo(x, y, self.moveing_time)
        pya.click()
        pya.write(self.acc_pwd, interval=(self.write_time*10))

        sleep(0.8)

        x, y = pya.locateCenterOnScreen("login_btn.png", confidence=0.6)
        pya.hotkey("enter")
        sleep(self.landing_time + 1)

        info_btn_loc = pya.locateOnScreen("save_login_info.png", confidence=0.65)

        x, y = pya.locateCenterOnScreen("save_login_info.png", confidence=0.65)
        pya.moveTo(x, y + info_btn_loc[3]/10*4, self.moveing_time)
        pya.click()

        sleep(self.landing_time)

    def output_to_csv(self) -> None:
        """
        Summary of the Function:
        Output the list of remaining followings didn't follow back haven't been removed to 'updated_dont_follow_back.csv'

        """

        self.df.loc[self.df['target_user'] == self.target_user, 'dont_follow_back_list'] = str(self.update_dont_follow_back_list)
        self.df.loc[self.df['target_user'] == self.target_user, 'amount'] = len(self.update_dont_follow_back_list)
        self.df.to_csv(self.imported_file, index=False)
         
    def input_from_csv(self) -> None:
        """
        Summary of the Function:
        Input the CSV file 'updated_dont_follow_back.csv'
        The list of followings didn't follow back

        """
        self.imported_file = 'updated_dont_follow_back.csv'
        if not os.path.exists(os.path.join(os.getcwd(), self.imported_file)):
            print(f'''---------------------------------------------\n
imported file: {self.imported_file} not found.
\n---------------------------------------------''')
            exit()
             
        self.df = pd.read_csv(self.imported_file)
        target_user_list = self.df["target_user"].to_list()
        
        if self.acc_username in target_user_list:
            self.target_user = self.acc_username 
            self.amount = self.df.loc[self.df["target_user"] == self.target_user, 'amount']
            df_object_dont_follow_back_list = self.df.loc[self.df["target_user"] == self.target_user, 'dont_follow_back_list']
            str_of_dont_follow_back_list = list(df_object_dont_follow_back_list)[0]
            self.dont_follow_back_list = literal_eval(str_of_dont_follow_back_list)
            self.delete_remaining_amount =  len(self.dont_follow_back_list)
        else:
            print('No valid target user found!')
            exit()

    def rm_dont_follow_back(self, index, target, del_user_list) -> list:
        """
        Summary of the Function:
        Remove the following didn't follow back

        Parameters:
        index (int): The number of user removed
        target (str): targeted user being removed
        del_user_list (list): A list of user has been removed
        
        Returns:
        del_user_list (set)

        """

        dont_follow_btn_loc = pya.locateOnScreen("dont_follow_btn.png", confidence=0.5)
        x, y = pya.locateCenterOnScreen("dont_follow_btn.png", confidence=0.5)
        pya.moveTo(x - dont_follow_btn_loc[3]/10*13, y, self.moveing_time)
        pya.click()

        sleep(0.7)

        dont_follow_btn_text_loc = pya.locateOnScreen("dont_follow_btn_text.png", confidence=0.5)
        x, y = pya.locateCenterOnScreen("dont_follow_btn_text.png", confidence=0.5)
        pya.moveTo(x, y + dont_follow_btn_text_loc[3]/10*4, self.moveing_time)
        pya.click()

        sleep(1)

        pya.hotkey("ctrl", "l")

        del_user_list.append(target)
        print(f'{index + 1}: {target} deleted')

        return del_user_list
         
    def dont_follow_container(self) -> list:
        """
        Summary of the Function:
        A container to count and control how many targets are being removed each time, based on the upper limit and lower limit.

        Parameters:
        self.del_lower_limit (int): the max amount of targets to be remained in the list e.g. 80
        self.del_upper_limit (int): the max amount of removal each time e.g. 100

        For example, 
        This time, the script will remove up to 100 targets from the list, unless 80 targets are remained in the list, script will stop.

        Returns:
        self.update_dont_follow_back_list (list)

        """
        start_time = time.time()
        del_user_list = []
        problem_target_list = []
        problem_amount = 0
        print(f'\nTotal delete remaining amount: {self.delete_remaining_amount}\n')
        pya.hotkey("ctrl", "l")
        for index, target in enumerate(self.dont_follow_back_list[:(self.delete_remaining_amount  - self.del_lower_limit)]):

            if index == self.del_upper_limit:
                    print('\nCurrent delete amount has reach the upper limit')
                    index -= 1
                    break
            
            elif index == 38:
                print("Cooling down for 5 Secs")
                for sec in range(1, 6)[::-1]:
                    print(f"{sec}...")
                    sleep(1)
            
            elif index == 68:
                print("Cooling down for 5 Secs")
                for sec in range(1, 6)[::-1]:
                    print(f"{sec}...")
                    sleep(1)

            try:
                pya.write(f"https://www.instagram.com/{target}/", interval=self.write_time)
                pya.hotkey("enter")
                sleep(self.landing_time)
                del_user_list = self.rm_dont_follow_back(index, target, del_user_list)
                
            
            except TypeError:
                print(f"Script is running too fast, affected target: {target} ")
                sleep(5)
                try:
                    del_user_list = self.rm_dont_follow_back(index, target, del_user_list)

                except TypeError:
                     print(f"Affected target: {target} is recorded and skipped ")
                     problem_target_list.append(target)
                     problem_amount += 1
                     pya.hotkey("ctrl", "l")

        pya.hotkey("ctrl", "w")
                
        remaining_amount = self.delete_remaining_amount  - (index + 1 - problem_amount)
        print(f'\nThe remaining users: {remaining_amount}')
        print(f'\nProblem List: {problem_target_list}')

        end_time = time.time()
        total_time = round(end_time - start_time)

        if total_time > 60:
                print(f"\nTotal Processing time: {round((end_time - start_time)/60)} mins {round(end_time - start_time)%60} secs\n")
        else:
                print(f"\nTotal Processing time: {round(end_time - start_time)} secs\n")

        self.update_dont_follow_back_list = [user for user in self.dont_follow_back_list if user not in del_user_list]
        
        return self.update_dont_follow_back_list


def main():
    Frm = FolRemover()

    def run_remover():
        """
        Summary of the Function:
        Step 1. Input CSV file to get the targets list
        Step 2. Check the login status
        Step 3. remove the targets from the list
        Step 4. Output the remaining back to the CSV file
        
        """

        Frm.input_from_csv()
        if Frm.delete_remaining_amount > Frm.del_lower_limit:
            login_status = Frm.check_login_status()
            if login_status == True:
                print("\n----------------------Preparing to log in the account----------------------\n")
                Frm.login()
            else:
                print("\n----------------------Account has been logged in----------------------\n")

            Frm.dont_follow_container()
            Frm.output_to_csv()
        else:
             print(f'\nTotal Remaining users are less than or equal to {Frm.del_lower_limit}: {Frm.delete_remaining_amount}\n')
             print('----------------------Script is shut down----------------------\n')
             
        
    run_remover()

if __name__=='__main__':
    main()



