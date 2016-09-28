/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Users;

import java.util.ArrayList;

/**
 *
 * @author xguest
 */
public class UserManager {
    ArrayList<User> users;

    public UserManager() {
        users=new ArrayList<User>();
    }
    
    public boolean addUser(User usr){
        for(User tempUser: users){
            if(tempUser.haveSameAttributes(usr))
                return false;
        }
        users.add(usr);        
        return true;
    }   
}
