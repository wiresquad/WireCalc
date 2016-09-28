/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package gameclient;

import Data.PacketData;
import java.io.*;
import java.net.*;
 
public class GameClient{
    final static int PORT = 8080;
    final static String IP = "localhost";
    static boolean logged = false;
    static DatagramSocket sock = null;
    
    public static void main(String args[]){
    	byte[] req;
    	BufferedReader cin = new BufferedReader(new InputStreamReader(System.in));
        try{
            System.out.println("Name:");
            String name = (String)cin.readLine();
            sock = new DatagramSocket();
            while(true){
                PacketData request = new PacketData();
                PacketData data;
                
            	if(logged){
                    req = cin.readLine().getBytes();
            	}else{//Lets handshake
                    request.setStatus(1);
                    request.setMsg(name);
            	}
 
            	//send request
                DatagramPacket  dp = new DatagramPacket(request.getData() , request.getData().length , InetAddress.getByName(IP) , PORT);
                sock.send(dp);
 
 
                //buffer to receive incoming data
                byte[] buffer = new byte[65536];
                DatagramPacket reply = new DatagramPacket(buffer, buffer.length);
                sock.receive(reply);

                data = new PacketData(reply.getData(),reply.getLength());
                
                switch(data.getStatus()){
                    case 1://Handshake
                        logged = true;
                        System.out.println(data.getMsg());
                    break;
                    case 2://The Main case
                        
                    break;
                    case 0://other

                    break;
                }
            }
        }catch(IOException e){
            System.err.println("IOException " + e);
        }
    }
}
