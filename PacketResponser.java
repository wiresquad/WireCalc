/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Server;

import java.io.*;
import java.net.*;
import UsersPackage.*;
import java.util.logging.Level;
import java.util.logging.Logger;

public class PacketResponser implements Runnable{
    
    UserManager userManager;
    DatagramSocket socket;
    byte[] data;
    int packetLength;
    int packetPort;
    String packetAdress;

    public PacketResponser(UserManager userManager, DatagramSocket socket, DatagramPacket packet) {
        this.userManager=userManager;
        this.socket=socket;
        
        data=packet.getData();
        packetLength=packet.getLength();
        packetPort=packet.getPort();
        packetAdress=packet.getAddress().getHostName();
    }
    
    
    @Override
    public void run() {

        byte[] resp;
        String s = new String(data, 0, packetLength);

        // Main switch case
        if(s.startsWith("Itro:")){
            boolean ans=userManager.addUser(new User(packetPort,packetAdress,s.substring(5)));
            if(ans){
                resp=("Answ:"+s.substring(5)).getBytes();
            }
            else{
                resp=("Idinaxui:"+s.substring(5)).getBytes();
            }
        }
        else{
            resp=("sxva dataa").getBytes();
        }
        
        
        try {
            DatagramPacket dp = new DatagramPacket(resp , resp.length , InetAddress.getByName(packetAdress) ,packetPort);
            socket.send(dp);
        } 
        catch (IOException ex) {
            Logger.getLogger(PacketResponser.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    
}
