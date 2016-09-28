/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Users;

/**
 *
 * @author xguest
 */
public class User {
   
    public int port;
    public String ip;
    public String name;

    public User(int port, String ip, String name){
        this.port=port;
        this.name=name;
        this.ip=ip;
    }   
    
    public boolean haveSameAttributes(User usr){
        
        return this.port==usr.port;    
    }
    
}
