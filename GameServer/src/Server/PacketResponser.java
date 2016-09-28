/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Server;


import java.io.*;
import java.net.*;
import Data.*;
import Users.*;

public class PacketResponser implements Runnable{    
    UserManager userManager;
    DatagramSocket socket;
    byte[] receivedData;
    int packetLength;
    int packetPort;
    InetAddress packetAdress;

    public PacketResponser(UserManager userManager, DatagramSocket socket, DatagramPacket packet) {
        this.userManager=userManager;
        this.socket=socket;
        this.receivedData=packet.getData();
        this.packetLength=packet.getLength();
        this.packetPort=packet.getPort();
        this.packetAdress=packet.getAddress();
    }
    
    @Override
    public void run() {        
        PacketData data = new PacketData(receivedData,packetLength);
        PacketData response = new PacketData();

        switch(data.getStatus()){
            case 1://Handshake
                System.out.println(data.getMsg()+" Connected from "+packetAdress.getHostName());
                //adding user to DB
                boolean userAddingResult=userManager.addUser(new User(packetPort,packetAdress.getHostName(),data.getMsg()));
                if(userAddingResult)
                    response.setMsg("Hello new user.");
                else
                    response.setMsg("Welcome back "+data.getMsg()+"!");
                
                //Let them shake
                response.setStatus(1);         
            break;
            case 2://The Main case
               
            break;
            case 0://other
                
            break;
        }
        
        try {//response to Client
            DatagramPacket dp = new DatagramPacket(response.getData() ,  response.getData().length , packetAdress ,packetPort);
            socket.send(dp);
        }catch (IOException e){
            System.err.println(e);
        }
    }  
}
